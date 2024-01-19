from django.shortcuts import render
from appUser.models import Profile
from django.contrib.auth.decorators import login_required


def indexPage(request):
   context = {}
   return render(request, "index.html", context)

@login_required(login_url="loginPage")
def browseindexPage(request):
   profile = Profile.objects.get(user=request.user, islogin=True)
   
   context = {
      "profile":profile,
   }
   return render(request, "browse-index.html", context)
   

def error_404(request):
   return render(request, "error/error404.html")
