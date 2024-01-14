from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

def profilePage(request):
   context = {}
   return render(request, "profile.html", context)
   
def hesapPage(request):
   context = {}
   return render(request, "hesap.html", context)
   
def loginPage(request):
   
   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      rememberme = request.POST.get("rememberme")
      
      user = authenticate(username=username, password=password)
      if user:
         login(request,user)

         if rememberme:
            request.session.set_expiry(604800) # 1 hafta beni hatırla 
         
         return redirect("profilePage")
      else:
         messages.error(request, "Kullancı adı veya şifre yanlış!")
         
   
   context = {}
   return render(request, "user/login.html", context)
   
def registerPage(request):
   context = {}
   
   if request.method == "POST":
      fname = request.POST.get("fname")
      lname = request.POST.get("lname")
      username = request.POST.get("username")
      email = request.POST.get("email")
      password1 = request.POST.get("password1")
      password2 = request.POST.get("password2")
      
      site = request.POST.get("check-site")
      kvkk = request.POST.get("check-kvkk")
      
      if fname and lname and username and email and password1 and site and kvkk:
         if password1 == password2:
            if not User.objects.filter(username=username).exists():
               if not User.objects.filter(email=email).exists():
                  num_bool = up_bool = False
                  # Password control
                  for k in password1: # => asDqwe
                     if k.isnumeric(): num_bool = True
                     if k.isupper(): up_bool = True
                     
                  if len(password1)>=8 and num_bool and up_bool:
                     # Kayıt Edilebilir.
                     user = User.objects.create_user(first_name=fname, last_name=lname, username=username, email=email, password=password1)
                     user.save()
                     return redirect("loginPage")
                  else:
                     messages.error(request, "Şifrenizin 8 veya daha uzun olması gerekir.")
                     messages.error(request, "Şifrenizde en az bir rakam olması gerekir.")
                     messages.error(request, "Şifrenizde en az bir büyük harf olması gerekir.")
               else:
                  messages.error(request, "Bu email zaten kullanılıyor !")
            else:
               messages.error(request, "Kullanıcı adı daha önceden alınmış !")
         else:
            messages.error(request, "Şifreler aynı değil!")
      else:
         messages.warning(request, "Boş bırakılan yerleri lütfen doldurunuz...")            
         context.update({
            "fname":fname,"lname":lname,"username":username,"email":email
         })     
                  
   
   return render(request, "user/register.html", context)