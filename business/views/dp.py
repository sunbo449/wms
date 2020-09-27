from django.shortcuts import render, redirect

def data_report(request):
    return render(request, 'data_report.html')
