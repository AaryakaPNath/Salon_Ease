"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.display),
    path('', views.profile),
    path('about', views.aboutpage),
    path('contact.html',views.contactpage),
    path('user_reg',views.userreg),
    path('user', views.user_create),
    path('uviewappt', views.user_view_appt),
    # path('paycancel',views.pay_cancel),
    path('salon_reg',views.salonreg),
    path('salon', views.salon_create),
    path('login', views.login_page),
    path('log_in', views.login_details),
    path('log_out', views.logout),
    path('profile', views.profilepage),
    path('ch_password', views.change_password),
    path('ch_p', views.password_change),
    path('update', views.update_user),
    path('updateuser', views.user_update),
    path('req',views.s_request),
    path('s_update',views.supdate),
    path('delete',views.sdelete),
    path('view',views.vsalon),
    path('deletesalon',views.salondelete),
    path('salonwarning',views.warning),
    path('salonwar',views.salonwarning),
    path('s_profile',views.s_profilepage),
    path('update_profile_salon',views.update_salonprofile),
    path('s_update_final',views.salon_update_final),
    path('ch_password2',views.change_password2),
    path('ch_p2',views.password_change2),
    path('locfil',views.locfil),
    path('addserv',views.addservices),
    path('viewserv',views.viewservice),
    path('delete_service',views.deleteservice),
    path('update_service',views.update_service),
    path('updateserv',views.updateservice),
    path('userwarning',views.userwarning),
    path('userwar',views.uwarning),
    path('deleteuser',views.deleteuser),


    path('salon_avl/<a>',views.salon_avl),
    path('det',views.details),
    # path('det/salon_avl/<a>',views.salon_avl),
    path('serv',views.selectgender),
    path('sg',views.select_gender),
    path('servicepg',views.servicepg),
    path('book1/<name>/<amount>',views.book_appointment1),
    path('book',views.book_appointment),
    path('payment',views.payment1),
    path('pay/<int:id>',views.pay),
    path('paycancel', views.paycancel),
    path('bookreq',views.book_request),
    path('accept_appt',views.approve_appt),
    path('reject_appt',views.reject_appt),
    path('salonviewconf',views.salon_view_confirm),
    path('salonpayview',views.salon_payment_view),
    path('avbook',views.admin_view_booking),
    path('comp',views.comp),
    path('usviewcomp',views.viewcomp),
    path('adviewcomp',views.adminviewcomp),
    path('adviewcon', views.adminviewcontact),
    path('logoutt',views.logoutt),
    # payment
    path('success', views.success),
    path('salonpays',views.salon_payments),
    path('salonpaytotal',views.salontotalpayment),
    # path('payad',views.adminviewpay),
    # path('adpaytotal',views.adminpaytotal),
    # path('adpayview',views.admin_view_pay),
    # path('adviewtotal',views.admin_view_total),
    # forgot password
    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='reset_password'),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)