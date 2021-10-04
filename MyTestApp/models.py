from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class DataSampleView(models.Model):
    col0 = models.CharField(max_length=30)
    col1 = models.CharField(max_length=30)
    col2 = models.CharField(max_length=30)
    col3 = models.CharField(max_length=30)
    col4 = models.CharField(max_length=30)
    col5 = models.CharField(max_length=30)
    col6 = models.CharField(max_length=30)
    col7 = models.CharField(max_length=30)
    col8 = models.CharField(max_length=30)
    col9 = models.CharField(max_length=30)
    col10 = models.CharField(max_length=30)
    col11 = models.CharField(max_length=30)
    col12 = models.CharField(max_length=30)
    col13 = models.CharField(max_length=30)
    col14 = models.CharField(max_length=30)
    col15 = models.CharField(max_length=30)
    col16 = models.CharField(max_length=30)
    col17 = models.CharField(max_length=30)
    col18 = models.CharField(max_length=30)
    col19 = models.CharField(max_length=30)
    col20 = models.CharField(max_length=30)
    col21 = models.CharField(max_length=30)
    col22 = models.CharField(max_length=30)
    col23 = models.CharField(max_length=30)
    col24 = models.CharField(max_length=30)
    col25 = models.CharField(max_length=30)
    col26 = models.CharField(max_length=30)
    col27 = models.CharField(max_length=30)
    col28 = models.CharField(max_length=30)
    col29 = models.CharField(max_length=30)
    col30 = models.CharField(max_length=30)
    col31 = models.CharField(max_length=30)
    col32 = models.CharField(max_length=30)
    col33 = models.CharField(max_length=30)
    col34 = models.CharField(max_length=30)
    col35 = models.CharField(max_length=30)
    col36 = models.CharField(max_length=30)
    col37 = models.CharField(max_length=30)
    col38 = models.CharField(max_length=30)
    col39 = models.CharField(max_length=30)
    col40 = models.CharField(max_length=30)
    col41 = models.CharField(max_length=30)
    col42 = models.CharField(max_length=30)
    col43 = models.CharField(max_length=30)
    col44 = models.CharField(max_length=30)
    col45 = models.CharField(max_length=30)
    col46 = models.CharField(max_length=30)
    col47 = models.CharField(max_length=30)
    col48 = models.CharField(max_length=30)
    col49 = models.CharField(max_length=30)
    col50 = models.CharField(max_length=30)

    def __str__(self):
        return self.col1

    class Meta:
        verbose_name = 'Столбец'
        verbose_name_plural = 'Столбцы'


class FileItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)
    path = models.TextField(blank=True, null=True)
    size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    @property
    def title(self):
        return str(self.name)
