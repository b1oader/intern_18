from django.conf.urls import url, include
from django.contrib import admin
from .api import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
