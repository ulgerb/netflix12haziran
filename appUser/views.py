from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from appUser.models import *
from django.core.mail import send_mail
from netflix12haziran.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required # decorator giriş yapmayanları kısıtla



def emailmessagePage(request):

   user_list = User.objects.values("email")
   user_email_list = []
   
   for i in user_list:
      user_email_list.append(i["email"])
         
   if request.method == "POST":
      title = request.POST.get("title")
      text = request.POST.get("text")

      emailmessage = Emailmessage(title=title, text=text)
      emailmessage.save() # SQL kaydını yapıyor
      
      for i in user_email_list:
         send_mail(
            title,
            text,
            EMAIL_HOST_USER,
            [i],
            fail_silently=False,
         )

      
   
   context = {}
   return render(request, "emailmessage.html",context)

@login_required(login_url="loginPage")
def profilePage(request):
   context = {}
   
   profile_list = Profile.objects.filter(user=request.user, isview=True)
   profile_delete_list = Profile.objects.filter(user=request.user, isview=False)
   # olan profile adı varsa ve silinmişse tekrar eski profilini getirmek istemisin yoksa yenisimi oluşsun
   if request.method == "POST":
      submit = request.POST.get("submit")
      title = request.POST.get("title")
      image = request.FILES.get("image")
      
      if submit == "profileCreate": 
         if len(profile_list) < 4:
            if title and image:
               if profile_delete_list.filter(title=title).exists(): # Silinen Profil olup olmadığını tespit et
                  context.update({"is_delete_title":True ,"title":title, "image":image})
                  profile = Profile(title=title, image=image, user=request.user,isview=False, isnew=True) # aynı isme sahip yeni profil
                  profile.save()
               else:
                  profile = Profile(title=title, image=image, user=request.user)
                  profile.save()
                  return redirect("profilePage")
            else:
               messages.warning(request, "Boş bırakılan yerler var")
      elif submit == "newProfileCreate":
         profildelete = profile_delete_list.get(title=title, isnew=False) # aynı isme sahip eski profil
         profildelete.delete()
         profile = Profile.objects.get(user=request.user, isnew=True) # yeni oluşturduğumuz profili getir
         profile.isnew = False
         profile.isview = True
         profile.save()
         return redirect("profilePage")

      elif submit == "oldProfileCreate":
         profil = Profile.objects.get(title=title, isnew=True)
         profil.delete()
         profildelete = profile_delete_list.get(title=title, isnew=False)
         profildelete.isview = True
         profildelete.save()
         return redirect("profilePage")
      
      elif submit == "profileUpdate":
         
         profileid = request.POST.get("profileid")
         profile = Profile.objects.get(user=request.user, id=profileid)
         if title:
            profile.title = title
         if image:
            profile.image = image
         profile.save()
         return redirect("profilePage")         
         
         
         
   context.update({
      "profile_list":profile_list,
   })
   return render(request, "profile.html", context)

@login_required(login_url="loginPage")
def profileDelete(request, pid):
   profile = Profile.objects.get(user=request.user,id=pid)
   profile.isview = False
   profile.save()
   return redirect("profilePage")

@login_required(login_url="loginPage")
def profileLogin(request,pid):
   profile_list = Profile.objects.filter(user=request.user) # kullanının tüm profilleri
   profile_list.update(islogin=False) # tüm listedeki islogin False olsun
   
   profile = Profile.objects.get(user=request.user, id=pid) # tıklanan profile
   profile.islogin = True # girişli olarak ayarla
   profile.save() # kaydet
   return redirect("browseindexPage")

# ============ 
@login_required(login_url="loginPage")
def hesapPage(request):
   profile = Profile.objects.get(user=request.user, islogin=True)
   
   if request.method == "POST":
      submit = request.POST.get("submit")
      
      if submit == "emailSubmit":
         email = request.POST.get("email")
         password = request.POST.get("password")
         # set_password() - check_password()
         if request.user.check_password(password): # şifre True yada False
            request.user.email = email
            request.user.save()
            return redirect("hesapPage")
         else:
            messages.error(request, "Şifreniz yanlış email değiştirlemedi!")
      elif submit == "passwordSubmit":
         password = request.POST.get("password")
         password1 = request.POST.get("password1")
         password2 = request.POST.get("password2")
         if request.user.check_password(password):
            if password1 == password2:
               request.user.set_password(password1)
               request.user.save()
               return redirect("loginPage")
            else:
               messages.error(request, "Yeni şifreler bir biriyle uyuşmuyor!")
         else:
            messages.error(request, "Şifreniz yanlış şifre değiştirlemedi!")

      elif submit == "telSubmit":
         tel = request.POST.get("tel")
         password = request.POST.get("password")
         if request.user.check_password(password): # şifre kontrol
            request.user.userinfo.tel = tel
            request.user.userinfo.save()
            return redirect("hesapPage")
         else:
            messages.error(request, "Şifreniz yanlış telefon değiştirlemedi!")
   
   
   context = {
      "profile":profile,
   }
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
                     
                     userinfo = Userinfo(user=user)
                     userinfo.save()
                     
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

@login_required(login_url="loginPage")
def logoutUser(request):
   logout(request)
   return redirect("loginPage")
      