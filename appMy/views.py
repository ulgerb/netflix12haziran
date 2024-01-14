from django.shortcuts import render

# Create your views here.


def indexPage(request):
   context = {}
   return render(request, "index.html", context)
   
def browseindexPage(request):
   context = {}
   return render(request, "browse-index.html", context)
   


