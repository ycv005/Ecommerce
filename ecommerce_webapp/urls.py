from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from accounts_app.views import login_page, register_page, guest_register_page
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_page,name="home_page"),
    path('about/', views.about_page,name="about_page"),
    path('contact-us/', views.contact_page,name="contact_page"),
    path('login/', login_page,name="login_page"),
    path('logout/', LogoutView.as_view(),name="logout_page"),
    path('register/', register_page,name="register_page"),
    path('register/guest', guest_register_page,name="guest_register_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)