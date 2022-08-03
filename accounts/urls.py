from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts.views import account_views, profile_views, kakaopay_views  

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', account_views.signup, name='signup'),	
    path('profile/<int:pk>', profile_views.profile, name='profile'),
    path('profile/<int:pk>/register', profile_views.profile_register, name='profile_register'),
    path('profile/<int:pk>/modify', profile_views.profile_modify, name='profile_modify'),
    path('profile/<int:pk>/point', profile_views.point_charge, name='point_charge'),
    path('kakaoPay/', kakaopay_views.kakaoPay, name='kakaoPay'),
    path('paySuccess/', kakaopay_views.paySuccess, name='paySuccess'),
    path('payFail/', kakaopay_views.payFail, name='payFail'),
    path('payCancel/', kakaopay_views.payCancel, name='payCancel'),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )