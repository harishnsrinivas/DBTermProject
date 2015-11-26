from django.conf.urls import patterns, url
from otsapp import views


urlpatterns = patterns('views',
    url(r'^$', views.index, name="index"),
    url(r'^user/login/$', views.login, name="login"),
    url(r'^user/logout/$', views.logout, name="logout"),
    url(r'^user/home/$', views.home_dashborad, name="dashborad"),
)
