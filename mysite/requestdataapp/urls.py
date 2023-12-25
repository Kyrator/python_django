from django.urls import path
from .views import handle_file_upload, process_get_view, user_form

app_name = "requestdataapp"

urlpatterns = [
    path("get/", process_get_view, name="get-view"),
    path("bio/", user_form, name="user_form"),
    path("upload/", handle_file_upload, name="upload-file"),
    path("error/", handle_file_upload, name="error-request"),
]
