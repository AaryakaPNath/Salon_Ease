from django.contrib import admin

# Register your models here.
from .models import usertable
admin.site.register(usertable)
from .models import salontable
admin.site.register(salontable)
from .models import logintable
admin.site.register(logintable)
from .models import servicetable
admin.site.register(servicetable)
from .models import bookingtable
admin.site.register(bookingtable)
from .models import payment
admin.site.register(payment)
from .models import complaint
admin.site.register(complaint)
from .models import ResetPassword
admin.site.register(ResetPassword)
from .models import contact
admin.site.register(contact)

