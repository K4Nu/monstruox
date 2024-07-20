import os.path
from django.conf import settings
from django import forms
from .models import Player,Clan


class PlayerForm(forms.ModelForm):
    image_clear = forms.BooleanField(required=False, label="Clear image")

    class Meta:
        model = Player
        fields = ['nickname', 'bio', 'avatar', 'image_clear']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('image_clear'):
            if instance.avatar and instance.avatar.name != 'default.jpg':
                instance.avatar.delete(save=False)
            instance.avatar = 'default.jpg'
        if commit:
            instance.save()
        return instance

class ClanForm(forms.ModelForm):
    emblem_clear = forms.BooleanField(required=False)

    class Meta:
        model = Clan
        fields = ["name", "motto", "description", "emblem"]
        widgets = {
            # the forms.FileInput removes the current and clear text from ImageField!!!
            'emblem': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_description(self):
        description=self.cleaned_data.get("description")
        if len(description.rstrip())>2500:
            raise forms.ValidationError("The description is too long, it can be 2500 characters max")

    def save(self, commit=True):
        instance = super(ClanForm, self).save(commit=False)
        if self.cleaned_data.get('emblem_clear'):
            if instance.emblem and instance.emblem.name != 'default_emblem.jpg':
                instance.emblem.delete(save=False)
            instance.emblem = 'default_emblem.jpg'
        if commit:
            instance.save()
        return instance

