from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from unixdashboard.views import *
urlpatterns = patterns('',
   
    url(r'^$', loginpage),
    url(r'^login/',login_check),
    url(r'^home/', home),
    url(r'^edit/', edit),
    url(r'^state/', state),
    url(r'^addrow/', addrow),
    url(r'^modifyrow/', modifyrow),
    url(r'^admin/', include(admin.site.urls)),

) 
# * static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
