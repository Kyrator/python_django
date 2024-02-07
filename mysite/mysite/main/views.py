from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
        }
        return render(request, 'main/index.html', context=context)
