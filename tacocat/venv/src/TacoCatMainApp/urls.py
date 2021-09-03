"""TacoCatMainApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
# auth_views comes pre-packaged with password reset tools
from django.contrib.auth import views as auth_views
from django.urls import path, include

# this is saying, from the personal directory, in the views file, import home_screen_view function.
# because it is likely there will be multiple functions to call from the same directory,
# we create a list to stay organized
from personal.views import (
    home_screen_view,
)

from account.views import (
    register_view,
    login_view,
    logout_view,
    account_search_view,
)
# alphabitized by 'name'
urlpatterns = [
    path('admin/', admin.site.urls),
    # include is going to tell it where to find the urls
    path('account/', include('account.urls', namespace='account')),
    # there is nothing to pass into the first parameter because this is the home screen.
    # when the home screen url is passed in, the second parameter is the function that gets called.
    # the function is created in the views.py file of the app
    path('', home_screen_view, name='home'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    path('search/', account_search_view, name="search"),




    # ----------------------------------These are all prebuilt---------------------------------
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]
# --------------------------------End Of These are all prebuilt---------------------------------
# These will tell django where static files exist so it can build urls to host the resources
# if we are NOT in production:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)