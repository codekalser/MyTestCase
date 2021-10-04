from django.shortcuts import render
import base64
import hashlib
import hmac
import os
import time
from rest_framework import permissions, status, authentication, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .config_aws import (
    AWS_UPLOAD_BUCKET,
    AWS_UPLOAD_REGION,
    AWS_UPLOAD_ACCESS_KEY_ID,
    AWS_UPLOAD_SECRET_KEY
)
from .models import FileItem, DataSampleView
from rest_pandas import PandasSimpleView
import pandas as pd
import csv
import io
from django.contrib import messages


def DataSampleView_upload(request):    # declaring template
    template = "DataSampleView_upload.html"
    data = DataSampleView.objects.all()# prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be 51 columns',
        'DataSample': data
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for col in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = DataSampleView.objects.update_or_create(
                col0=col[0], col1=col[1], col2=col[2],
                col3=col[3], col4=col[4], col5=col[5],
                col6=col[6], col7=col[7], col8=col[8],
                col9=col[9], col10=col[10], col11=col[11],
                col12=col[12], col13=col[13], col14=col[14],
                col15=col[15], col16=col[16], col17=col[17],
                col18=col[18], col19=col[19], col20=col[20],
                col21=col[21], col22=col[22], col23=col[23],
                col24=col[24], col25=col[25], col26=col[26],
                col27=col[27], col28=col[28], col29=col[29],
                col30=col[30], col31=col[31], col32=col[32],
                col33=col[33], col34=col[34], col35=col[35],
                col36=col[36], col37=col[37], col38=col[38],
                col39=col[39], col40=col[40], col41=col[41],
                col42=col[42], col43=col[43], col44=col[44],
                col45=col[45], col46=col[46], col47=col[47],
                col48=col[48], col49=col[49],col50=col[50],
                )
    context = {}
    return render(request, template, context)


class TimeSeriesView(PandasSimpleView):
    def get_data(self, request, *args, **kwargs):
        return pd.read_csv('data.csv')


class FilePolicyAPI(APIView):
    """
    This view is to get the AWS Upload Policy for our s3 bucket.
    What we do here is first create a FileItem object instance in our
    Django backend. This is to include the FileItem instance in the path
    we will use within our bucket as you'll see below.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        """
        The initial post request includes the filename
        and auth credientails. In our case, we'll use
        Session Authentication but any auth should work.
        """
        filename_req = request.data.get('filename')
        if not filename_req:
            return Response({"message": "A filename is required"}, status=status.HTTP_400_BAD_REQUEST)
        policy_expires = int(time.time() + 5000)
        user = request.user
        username_str = str(request.user.username)
        """
        Below we create the Django object. We'll use this
        in our upload path to AWS. 

        Example:
        To-be-uploaded file's name: Some Random File.mp4
        Eventual Path on S3: <bucket>/username/2312/2312.mp4
        """
        file_obj = FileItem.objects.create(user=user, name=filename_req)
        file_obj_id = file_obj.id
        upload_start_path = "{username}/{file_obj_id}/".format(
            username=username_str,
            file_obj_id=file_obj_id
        )
        _, file_extension = os.path.splitext(filename_req)
        filename_final = "{file_obj_id}{file_extension}".format(
            file_obj_id=file_obj_id,
            file_extension=file_extension

        )
        """
        Eventual file_upload_path includes the renamed file to the 
        Django-stored FileItem instance ID. Renaming the file is 
        done to prevent issues with user generated formatted names.
        """
        final_upload_path = "{upload_start_path}{filename_final}".format(
            upload_start_path=upload_start_path,
            filename_final=filename_final,
        )
        if filename_req and file_extension:
            """
            Save the eventual path to the Django-stored FileItem instance
            """
            file_obj.path = final_upload_path
            file_obj.save()

        policy_document_context = {
            "expire": policy_expires,
            "bucket_name": AWS_UPLOAD_BUCKET,
            "key_name": "",
            "acl_name": "private",
            "content_name": "",
            "content_length": 524288000,
            "upload_start_path": upload_start_path,

        }
        policy_document = """
        {"expiration": "2019-01-01T00:00:00Z",
          "conditions": [ 
            {"bucket": "%(bucket_name)s"}, 
            ["starts-with", "$key", "%(upload_start_path)s"],
            {"acl": "%(acl_name)s"},

            ["starts-with", "$Content-Type", "%(content_name)s"],
            ["starts-with", "$filename", ""],
            ["content-length-range", 0, %(content_length)d]
          ]
        }
        """ % policy_document_context
        aws_secret = str.encode(AWS_UPLOAD_SECRET_KEY)
        policy_document_str_encoded = str.encode(policy_document.replace(" ", ""))
        url = 'https://{bucket}.s3-{region}.amazonaws.com/'.format(
            bucket=AWS_UPLOAD_BUCKET,
            region=AWS_UPLOAD_REGION
        )
        policy = base64.b64encode(policy_document_str_encoded)
        signature = base64.b64encode(hmac.new(aws_secret, policy, hashlib.sha1).digest())
        data = {
            "policy": policy,
            "signature": signature,
            "key": AWS_UPLOAD_ACCESS_KEY_ID,
            "file_bucket_path": upload_start_path,
            "file_id": file_obj_id,
            "filename": filename_final,
            "url": url,
            "username": username_str,
        }
        return Response(data, status=status.HTTP_200_OK)


class FileUploadCompleteHandler(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        file_id = request.POST.get('file')
        size = request.POST.get('fileSize')
        data = {}
        type_ = request.POST.get('fileType')
        if file_id:
            obj = FileItem.objects.get(id=int(file_id))
            obj.size = int(size)
            obj.uploaded = True
            obj.type = type_
            obj.save()
            data['id'] = obj.id
            data['saved'] = True
        return Response(data, status=status.HTTP_200_OK)