from django.conf.urls import url, include


urlpatterns = [
    url(r'^v1/', include('restapi.v1.urls',)),
    url(r'^v2/', include('restapi.v2.urls',))
]

