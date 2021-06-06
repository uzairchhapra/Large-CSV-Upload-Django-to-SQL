from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    # path("", views.index, name="index"),
    path('', views.ChunkedUploadDemo.as_view(), name='chunked_upload'),
    path('api/chunked_upload_complete/', views.MyChunkedUploadCompleteView.as_view(),
         name='api_chunked_upload_complete'),
    path('api/chunked_upload/', views.MyChunkedUploadView.as_view(),
         name='api_chunked_upload'),
    path('getData/<tableName>/<columName>/<value>',
         views.getData, name="getData"),
    path('loadTables/<fileName>', views.loadTables, name="loadTables"),
]
