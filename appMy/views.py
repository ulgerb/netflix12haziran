from django.shortcuts import render

# Create your views here.


def indexPage(request):
   context = {}
   return render(request, "index.html", context)
   
def browseindexPage(request):
   context = {}
   return render(request, "browse-index.html", context)
   
def profilePage(request):
   context = {}
   return render(request, "profile.html", context)
   
def hesapPage(request):
   context = {}
   return render(request, "hesap.html", context)
   
def loginPage(request):
   context = {}
   return render(request, "user/login.html", context)
   
def registerPage(request):
   context = {}
   return render(request, "user/register.html", context)

