
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from MyTestApp.views import FilePolicyAPI, FileUploadCompleteHandler, DataSampleView_upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DataSampleView_upload, name="DataSampleView_upload"), # 1st endpoint
    # TODO 2nd endpoint
    # TODO configure config_aws.py to correct access
    url(r'^api/files/complete/$', FileUploadCompleteHandler.as_view(), name='upload-complete'),
    url(r'^api/files/policy/$', FilePolicyAPI.as_view(), name='upload-policy'),
]
