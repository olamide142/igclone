from django.urls import path

from . import views
from .services.register import Register
from .services.auth import Auth
from .services.account import Account
from .services.tools import Tools
from .services.follows import Follows

urlpatterns = [
    path('', views.index, name='index'),
    
    # Register
    path('register/', Register.register_user, name='register_user'),

    # Authentication
    path('auth/login/', Auth.login_view, name='login_view'),
    path('auth/logout/', Auth.logout_view, name='logout_view'),

    # Account
    path('account/<str:username>/', Account.view_account, name='view_account'),
    path('account/<str:username>/update/', Account.update_account, name='update_account'),

    # Follows
    path('actions/follows/', Follows.follow_or_unfollow, name='follow_or_unfollow'),

    #Settings
    path('settings/', Tools.profile_settings, name='profile_settings'),

]
