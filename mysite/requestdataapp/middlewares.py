import time

from django.http import HttpRequest
from django.shortcuts import render


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.requests_time = {}
        self.response_count = 0
        self.exception_count = 0

    def __call__(self, request: HttpRequest):
        time_delay = 10
        if not self.requests_time:
            print("Это первый request после перезапуска сервера, словарь еще пуст.")
        else:
            if (round(time.time()) * 1) - self.requests_time['time'] < time_delay \
                    and self.requests_time['ip_address'] == request.META.get('REMOTE_ADDR'):
                print("Прошло меньше 10 секунд для повторного запроса с вашего IP адреса.")
                return render(request, "requestdataapp/error-request.html")
        self.requests_time = {'time': round(time.time()) * 1, 'ip_address': request.META.get('REMOTE_ADDR')}

        self.requests_count += 1
        print("requests count", )
        response = self.get_response(request)
        self.response_count += 1
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
