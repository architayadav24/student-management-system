"""
URL configuration for student_records_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from student.views import index,about,contact,login_view,AdminHome,add_students,view_students,edit_student,del_student,feedback,view_feedback,search_stu,search_student,admin_logout,change_password,update_password,student_home,edit_profile,fee_detail,payment_receipt,user_change_pass,user_update_pass,forgot_password,reset_password
from django.conf import settings
from django.conf.urls.static import static
from student import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index,name="index"),
    path("about",about,name="about"),
    path("contact",contact,name="contact"),
    path("login",login_view,name="login"),
    path("AdminHome",AdminHome,name="AdminHome"),
    path("add_students",add_students,name="add_students"),
    path("view_students",view_students,name="view_students"),
    path("edit_student/<int:id>",edit_student,name="edit_student"),
    path("del_student/<int:id>",del_student,name="del_student"),
    path("feedback",feedback,name="feedback"),
    path("view_feedback",views.view_feedback,name="view_feedback"),
    path("search_stu",search_stu,name="search_stu"),
    path("search_student",search_student,name="search_student"),
    path("admin_logout",admin_logout,name="admin_logout"),
    path("change_password",change_password,name="change_password"),
    path("update_password",update_password,name="update_password"),
    path("student_home",student_home,name="student_home"),
    path("edit_profile",edit_profile, name="edit_profile"),
    path("fee_detail",fee_detail,name="fee_detail"),
    path("payment_receipt",payment_receipt,name="payment_receipt"),
    path("user_change_pass",user_change_pass,name="user_change_pass"),
    path("user_update_pass",views.user_update_pass,name="user_update_pass"),
    path("forgot_password/", forgot_password, name="forgot_password"),
    path("reset_password/", reset_password, name="reset_password")
   
    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
