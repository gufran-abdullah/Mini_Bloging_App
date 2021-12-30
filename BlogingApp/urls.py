"""BlogingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from blog.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('user_login',user_login,name="user_login"),
    path('user_signup',user_signup,name="user_signup"),
    path('user_home',user_home,name="user_home"),
    path('logout_users',logout_users,name="logout_users"),
    path('user_createblog',user_createblog,name="user_createblog"),
    path('user_viewblogs',user_viewblogs,name="user_viewblogs"),
    path('user_blogdetail/<int:id>',user_blogdetail,name="user_blogdetail"),
    path('user_editblog/<int:id>',user_editblog,name="user_editblog"),
    path('user_deleteblog/<int:id>',user_deleteblog,name="user_deleteblog"),
    path('user_changepassword',user_changepassword,name="user_changepassword"),
    path('admin_login',admin_login,name="admin_login"),
    path('admin_home',admin_home,name="admin_home"),
    path('admin_changestatus/<int:id>',admin_changestatus,name="admin_changestatus"),
    path('admin_pendingblogs',admin_pendingblogs,name="admin_pendingblogs"),
    path('admin_acceptedblogs',admin_acceptedblogs,name="admin_acceptedblogs"),
    path('admin_rejectedblogs',admin_rejectedblogs,name="admin_rejectedblogs"),
    path('admin_allblogs',admin_allblogs,name="admin_allblogs"),
    path('admin_deleteblog/<int:id>',admin_deleteblog,name="admin_deleteblog"),
    path('admin_allusers',admin_allusers,name="admin_allusers"),
    path('admin_deleteusers/<int:id>',admin_deleteusers,name="admin_deleteusers"),
    path('admin_changepassword',admin_changepassword,name="admin_changepassword"),
    path('blog_details/<int:id>',blog_details,name="blog_details"),
    # path('serach_blogs',serach_blogs,name="serach_blogs"),
    path('about_us',about_us,name="about_us"),
    path('contact_us',contact_us,name="contact_us"),
    path('admin_allmessages',admin_allmessages,name="admin_allmessages"),
    path('admin_deletemsgs/<int:id>',admin_deletemsgs,name="admin_deletemsgs")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
