from django.conf.urls import url
from  .import views

app_name = "shadowsocks"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^nodeinfo$',views.nodeinfo,name='nodeinfo'),
    url(r'^sshelp$',views.sshelp,name='sshelp'),
    url(r'^ssclient$',views.ssclient,name='ssclient'),
    url(r'^ssinvite$',views.ssinvite,name='ssinvite'),
    url(r'ssinvite/(?P<Num>[0-9]{1,2})/$',views.gen_invite_code,name='geninvitecode'),
    url(r'passinvite/(?P<invitecode>[\S]+)/$',views.pass_invitecode,name='passinvitecode'),
    url(r'register/$',views.register,name='register'),
    url(r'login/$',views.Login_view,name='login'),
    url(r'logout/$',views.Logout_view,name='logout'),
    url(r'users/userinfo/$',views.userinfo,name='userinfo'),
    ]
