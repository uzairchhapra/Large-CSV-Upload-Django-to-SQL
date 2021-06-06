from django.shortcuts import render
from django.views.generic.base import TemplateView
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import MyChunkedUpload
import pandas as pd
from django.core.files.storage import default_storage
from pandas.io import sql
from sqlalchemy import create_engine
from django.http import HttpResponse, JsonResponse
import requests
from .database_connection import getEngine
from django.views.decorators.csrf import csrf_exempt
import re
import os
import json

# Create your views here.


@csrf_exempt
def getData(request, tableName, columName, value):
    if request.method == 'GET':
        query = f"SELECT * FROM {tableName} WHERE {columName}={value}"
        # Use optional Parameter 'chunksize'
        df = pd.read_sql(sql=query, con=getEngine())
        data = df.to_json()
        return HttpResponse(data, content_type="application/json")


@csrf_exempt
def loadTables(request, fileName):
    tableName = re.sub('[^A-Za-z0-9]+', '', f'zeza_{fileName}')

    if request.method == 'PUT':
        # try:
        df = pd.read_csv(f'./media/{fileName}')
        # Use optional Parameter 'chunksize'
        df.to_sql(con=getEngine(), name=tableName, if_exists='replace')
        # Delete after Inserting
        if os.path.exists(f'./media/{fileName}'):
            os.remove(f'./media/{fileName}')
    return JsonResponse({'tableName': f'{tableName}'})


class ChunkedUploadDemo(TemplateView):
    template_name = 'uploaddata/uploadpage.html'


class MyChunkedUploadView(ChunkedUploadView):

    model = MyChunkedUpload
    field_name = 'the_file'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):

    model = MyChunkedUpload
    tableName = ''

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        file_name = default_storage.save(uploaded_file.name, uploaded_file)
        res = requests.put(
            f'{request.scheme}://{request.get_host()}/loadTables/{file_name}')
        self.tableName = json.loads(res.text)['tableName']
        return res

    def get_response_data(self, chunked_upload, request):
        return {'message': f"SUCCESS! File Name:'{chunked_upload.filename}', Table Name: '{self.tableName}', Size: {chunked_upload.offset} bytes!"}
