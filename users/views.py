import os.path
from django.conf import settings
from django.shortcuts import render,redirect
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from .models import Player,Clan
from django.contrib.auth.models import User
from .forms import PlayerForm,ClanForm
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image

def index(request):
    return render(request,"users/index.html")

def profile(request):
    user = request.user
    try:
        player = Player.objects.get(user=user)
    except Player.DoesNotExist:
        player = None

    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            current_player = form.save(commit=False)
            current_player.user = user  # Ensure the user is set for the new player

            # Check if the nickname already exists for another user
            if Player.objects.filter(nickname=form.cleaned_data.get('nickname')).exclude(user=user).exists():
                form.add_error('nickname', 'This nickname is already taken.')
            else:
                avatar = form.cleaned_data.get("avatar")
                if avatar and not isinstance(avatar, str):
                    avatar_filename = f'{current_player.nickname}{os.path.splitext(avatar.name)[1]}'
                    avatar_path = os.path.join(settings.MEDIA_ROOT, "avatar", avatar_filename)

                    with Image.open(avatar) as image:
                        image.thumbnail((200, 200))
                        if image.format == 'JPEG':
                            image.save(avatar_path, quality=100)
                        elif image.format == 'PNG':
                            image.save(avatar_path, optimize=True)
                        else:
                            image.save(avatar_path)  # For other formats

                    current_player.avatar = f"avatar/{avatar_filename}"

                current_player.save()
                return redirect("index")
    else:
        form = PlayerForm(instance=player)

    return render(request, "users/player_form.html", {"form": form})

@login_required
def clan_form(request):
    user = request.user

    # Get the clan instance if it exists, otherwise None
    clan = Clan.objects.filter(leader=user).first()

    if request.method == "POST":
        form = ClanForm(request.POST, request.FILES, instance=clan)
        if form.is_valid():
            current_clan = form.save(commit=False)

            if form.cleaned_data.get("emblem"):
                emblem = form.cleaned_data.get("emblem")
                emblem_filename = f'{current_clan.name}{os.path.splitext(emblem.name)[1]}'
                emblem_path = os.path.join(settings.MEDIA_ROOT, "emblems", emblem_filename)

                os.makedirs(os.path.dirname(emblem_path), exist_ok=True)

                with Image.open(emblem) as image:
                    image.thumbnail((200, 200))
                    if image.format == 'JPEG':
                        image.save(emblem_path, quality=100)
                    elif image.format == 'PNG':
                        image.save(emblem_path, optimize=True)
                    else:
                        image.save(emblem_path)  # For other formats

                current_clan.emblem = f"emblems/{emblem_filename}"

            if not current_clan.leader:
                current_clan.leader = user

            current_clan.save()
            return redirect("index")
    else:
        form = ClanForm(instance=clan)

    return render(request, "users/clan_form.html", {"form": form})

@login_required
def user(request,nickname):
    player=Player.objects.get(nickname=nickname)
    if user==request.user.player:
        return redirect('profile')
    return render(request,"users/user.html",{"player":player})