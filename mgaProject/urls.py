from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

handler400 = 'api.views.custom400'
handler403 = 'api.views.custom403'
handler404 = 'api.views.custom404'
handler500 = 'api.views.custom500'

urlpatterns = [
    path("api", include('api.urls')),
]

urlpatterns += staticfiles_urlpatterns()