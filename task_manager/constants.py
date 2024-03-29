'Constants for Task Manager main application.'

from typing import Final

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

# Route names
HOME: Final[str] = 'home'
LOGIN: Final[str] = 'login'
LOGOUT: Final[str] = 'logout'


# Reverses
REVERSE_HOME: Final = reverse_lazy(HOME)
REVERSE_LOGIN: Final = reverse_lazy(LOGIN)
REVERSE_LOGOUT: Final = reverse_lazy(LOGOUT)


# Messages
MSG_LOGIN: str = gettext_lazy('You are logged in')
MSG_LOGOUT: str = gettext_lazy('You are logged out')

MSG_NO_PERMISSION = gettext_lazy('You are not authentificated! Please sign in.')


# Templates
TEMPLATE_INDEX: Final[str] = 'index.html'
