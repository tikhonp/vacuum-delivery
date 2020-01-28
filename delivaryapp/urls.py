from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.loginp, name='loginp'),
    path('register/', views.registerp, name='registerp'),
    path('authed/', views.authedp, name='authedp'),
    path('logout/', views.logoutp, name='logoutp'),
    path('authed/profile/', views.profilep, name='profilep'),
    path('authed/working/', views.workingp, name='workingp'),
    path('authed/working/profile/', views.profilep, name='profilep'),
    path('authed/addorder/', views.addorderp, name='addorderp'),
    path('authed/working/stop/', views.stopworkingp, name='stopworkingp'),
    path('authed/working/getorder/', views.getorderp, name='getorderp'),
    path('test/', views.testp, name='testp'),
    path('authed/working/compliteorder/', views.compliteorderp, name='compliteorderp'),
    path('authed/working/compliteorder/sendorder/', views.sendorderp, name='sendorderp'),
    path('authed/working/compliteorder/cancel/', views.cancelsendingp, name='cancelsendingp'),
    path('authed/getorder/', views.authgetorderp, name='authgetorderp'),
]
