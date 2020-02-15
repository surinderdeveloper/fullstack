from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from .routers import router


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]