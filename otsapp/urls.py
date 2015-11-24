from django.conf.urls import patterns, url
from otsapp import views


urlpatterns = patterns('views',
    url(r'^$', views.index, name="index"),
    url(r'^user/login/$', views.login, name="login"),
)
