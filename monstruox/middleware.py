from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import os
class EnsurePlayerMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and if they have a profile
        if request.user.is_authenticated:
            try:
                player = request.user.player
            except Exception:
                player = None

            # If the user does not have a player, redirect them to the player creation URL
            if not player and request.path != reverse('profile'):
                return redirect(settings.PROFILE_CREATION_REDIRECT_URL)

            if player and request.path==reverse('profile'):
                return redirect('index')
        response = self.get_response(request)
        return response