from django import forms
from django.contrib.auth.forms import UserCreationForm

from .constants import (
    FIRST_NAME,
    FIRST_NAME_HELP_TEXT,
    FIRST_NAME_LABEL,
    LAST_NAME,
    LAST_NAME_HELP_TEXT,
    LAST_NAME_LABEL,
    USERNAME,
)
from .models import User


class UserForm(UserCreationForm):
    first_name = forms.CharField(
        required=True, label=FIRST_NAME_LABEL, help_text=FIRST_NAME_HELP_TEXT
    )
    last_name = forms.CharField(
        required=True, label=LAST_NAME_LABEL, help_text=LAST_NAME_HELP_TEXT
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (USERNAME, FIRST_NAME, LAST_NAME)
