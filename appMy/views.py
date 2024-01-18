from django.shortcuts import render
from appUser.models import Profile
# Create your views here.


def indexPage(request):
   context = {}
   return render(request, "index.html", context)
   
def browseindexPage(request):
   profile = Profile.objects.get(user=request.user, islogin=True)
   
   
   context = {
      "profile":profile,
   }
   return render(request, "browse-index.html", context)
   


