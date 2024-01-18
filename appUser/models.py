from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
   user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
   title = models.CharField(("Başlık"), max_length=50)
   image = models.ImageField(("Profile Resmi"), upload_to="profile", max_length=250)
   isview = models.BooleanField(("Görüntüle"), default=True)
   isnew = models.BooleanField(("Silinen Yeni Profil Mi"), default=False) # yeni profil olup olmadığını anlamızı sağlıcak
   islogin = models.BooleanField(("Girişli Profil"), default=False)
   
   def __str__(self) -> str:
      return self.title