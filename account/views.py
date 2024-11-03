from django.shortcuts import render



#  login
def login(request):
    return render(request, 'account/login.html', {})