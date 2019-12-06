from django.shortcuts import render

def gen_base(request):
    return render(request, 'index2.html')