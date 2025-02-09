from django.http import HttpResponse

def my_view(request):
    print(request.get_host())  # 打印解析的 Host
    return HttpResponse("Hello, world!")
# ...existing code...
