from django.contrib import admin
from django.urls import path, include
from users import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("allauth.urls")),
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path("clan_form",views.clan_form,name="clan_form"),
    path('user/<str:nickname>/', views.user, name='user'),
    path('friend-request/send/<int:receiver_id>/', views.send_friend_request, name='send_friend_request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
