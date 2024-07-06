from django.db import models
from django.utils import timezone
# Create your models here.
class usertable(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    # gender = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class salontable(models.Model):
    salon_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    license = models.FileField()
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    action = models.CharField(max_length=50, default="pending")
    photo = models.FileField()
    time = models.CharField(max_length=50)
    

    def __str__(self):
        return self.username

class logintable(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.IntegerField()
    def __str__(self):
        return self.username

class servicetable(models.Model):
    username = models.CharField(max_length=50)
    salon_name = models.CharField(max_length=50)
    service_name = models.CharField(max_length=40)
    description = models.CharField(max_length=80)
    amount = models.IntegerField()
    gender = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    service_photo = models.FileField()
    def __str__(self):
        return self.service_name


class bookingtable(models.Model):
    customer_name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    email = models.EmailField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField(default=True)
    service_name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    salon_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)


    def __str__(self):
        return self.customer_name

#payment
class payment(models.Model):
    s_name= models.CharField(max_length=50)
    customer_name=models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    email = models.EmailField()
    amount = models.IntegerField()
    def __str__(self):
        return self.customer_name

#admin payment
# class adpay(models.Model):
#     username = models.CharField(max_length=50)
#     amount = models.IntegerField()
#     date = models.DateField(default=timezone.now)
#     s_name = models.CharField(max_length=50)
#     def __str__(self):
#         return self.s_name

#complaint
class complaint(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.IntegerField()
    complaint = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# class PasswordReset(models.Model):
#     user=models.ForeignKey(usertable,on_delete=models.CASCADE)
#     token=models.CharField(max_length=4)

#contact
class contact(models.Model):
     name = models.CharField(max_length=50)
     email = models.EmailField()
     message = models.CharField(max_length=50)
     subject = models.CharField(max_length=50)
     def __str__(self):
         return self.name

class ResetPassword(models.Model):
    user=models.ForeignKey(usertable,on_delete=models.CASCADE)
    token=models.CharField(max_length=4)