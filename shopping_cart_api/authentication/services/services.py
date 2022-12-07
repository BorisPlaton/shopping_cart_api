from django.db import IntegrityError

from authentication.exceptions import StateConflict
from authentication.models import CustomUser, ContactInformation
from authentication.services.selectors import get_user_by_pk


def create_user(email: str, password: str, **kwargs):
    """
    Creates a new user model with given credentials. Password
    is automatically cached.
    """
    return CustomUser.objects.create_user(email, password, **kwargs)


def create_user_contact_information(user_pk: int, phone_number: str, location: str):
    """
    Creates contact information for the already existing user.
    """
    user = get_user_by_pk(user_pk)
    try:
        return ContactInformation.objects.create(user=user, phone_number=phone_number, location=location)
    except IntegrityError:
        raise StateConflict("User with `id` %s already has contact information." % user_pk)
