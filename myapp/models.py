from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionManager
from django.db.models.signals import post_delete,pre_save,pre_delete
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
from PIL import Image
import os
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


class custm_user(AbstractUser):
    phone = models.IntegerField(null=True,blank=True)
    age = models.IntegerField(("Age"),null=True,blank=True)
    createTime= models.DateTimeField(auto_now_add=True)
    dob = models.DateField(("Date of Birth"),null=True,blank=True)
    pro_pic = models.ImageField(upload_to="dp",default="default_pic.jpg")
    thumbnail_pro_pic = models.ImageField(upload_to="thumbnail",default="default_pic.jpg",blank=True)


    # class Meta:
    #     unique_together = [['email']]

    def save(self,*args, **kwargs):
        
        photo = super().save(*args, **kwargs)
        return photo
    
    def clean(self, *args, **kwargs):
        
        data = self.email
        print(data)
        if not self.pk:
            return 
        
        old_obj=custm_user.objects.get(pk=self.pk)
        print(old_obj)

        for i in custm_user.objects.all():
            if i.email==data and i.pk !=old_obj.pk:
                raise ValidationError("This mail is already taken")    

        if not old_obj.email:
            return 
            
        if not data:
            raise ValidationError("Email is important")
        super().clean( *args, **kwargs)


        
  
# class propicmodel(models.Model):
#     pro_pic = models.ImageField(upload_to="media/dp",default="default_pic.jpg")
#     # pro_pic_thamb=models.ImageField(upload_to="media/dp",default="default_pic.jpg")
#     user_id = models.OneToOneField(custm_user,models.CASCADE)



@receiver(pre_delete, sender=custm_user)
def submission_delete(sender, instance, **kwargs):
    instance.pro_pic.delete(False) 
    instance.thumbnail_pro_pic.delete(False) 


@receiver(pre_save, sender=custm_user)
def submission_save(sender, instance, **kwargs):
    if not instance.pk:# new instance
        return False
    try:    #old instance
        old_obj=sender.objects.get(pk=instance.pk)
        old_file = old_obj.pro_pic
        new_file = instance.pro_pic
        if not old_file == new_file: #image is changed
            old_obj.pro_pic.delete(False) 
    except sender.DoesNotExist:
        return False

@receiver(pre_save, sender=custm_user)
def submission_save2(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_obj=sender.objects.get(pk=instance.pk)
        old_file = old_obj.pro_pic
        new_file = instance.pro_pic
        if not old_file == new_file:
            old_obj.thumbnail_pro_pic.delete(False) 
            instance.thumbnail_pro_pic.delete(False) 
            try: 
                
                image = Image.open(instance.pro_pic)    #opening image for edit
                # cropped_image = image.crop(()) #crop image
                resized_image = image.resize((200, 200), Image.ANTIALIAS)   #resize image
                
                instance.thumbnail_pro_pic.file=instance.pro_pic.file
                new_picture_name = instance.pro_pic.name.split("/")[-1]
                instance.thumbnail_pro_pic.save(new_picture_name,instance.pro_pic.file,False)
                print(instance.thumbnail_pro_pic.name)
                # save updated image  to thumbnail

                # if("thumbnail" not in self.thumbnail_pro_pic.name or "thumbnail" not in self.thumbnail_pro_pic.name):
                #     print("vsdfvbsfgvb")
                resized_image.save(instance.thumbnail_pro_pic.path)

            except FileNotFoundError:
                pass


    except sender.DoesNotExist:
        return False
