from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    """Проверяет не превышает ли 1 мб размер файла сохраняет в папку upload"""
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        max_file_size_mb = 1
        myfile_size_mb = round((myfile.size/1024)/1024, 2)
        if myfile.size > max_file_size_mb * 1024 ** 2:
            error_message = ("Размер файла не должен привышать {size} Мб<br>Ваш размер {file_size_mb} Мб"
                             .format(size=max_file_size_mb,
                                     file_size_mb=myfile_size_mb,))
            return HttpResponse(error_message, status=400)
        fs = FileSystemStorage(location='upload/')
        filename = fs.save(myfile.name, myfile)
        print("Файл сохранен", filename)

    return render(request, "requestdataapp/upload-file.html")


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, "requestdataapp/user-bio-form.html")