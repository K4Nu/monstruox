from django.contrib import admin
from .models import Player,Clan,ClanRequest,FriendRequest
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    pass

@admin.register(ClanRequest)
class ClanRequestAdmin(admin.ModelAdmin):
    pass