"""disquaire_project3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
#from django.contrib import admin
from django.urls import path, include
#from django.conf import settings
#import debug_toolbar

from django.conf.urls import url
from store import views


urlpatterns = [
    path('', views.listing, name='listing'),
    url(r'^(?P<album_id>[0-9])/$', views.detail, name='detail'),
    #r'^$'
    #?p<album_id>[0-9])/
    path('search/', views.search, name='search'),
   # path('store/', include('store.urls')),
] 
#(<album_id>)/
#urlpatterns = [
#    path(r'', views.listing),
#    path('', views.detail),
#    path('search', views.search),
#    path(r'store/', include('store.urls')),
#    path(r'admin/', admin.site.urls),
#]
#if settings.DEBUG:
 #   import debug_toolbar
 #   urlpatterns=[
 #       path(r'__debug__/', include(debug_toolbar.urls)),
  #  ] + urlpatterns
#urlpatterns = [
#    path('admin/', admin.site.urls),
#]