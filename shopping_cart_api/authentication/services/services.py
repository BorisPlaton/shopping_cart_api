from authentication.models import CustomUser


def create_user(email: str, password: str, **kwargs):
    """
    Creates a new user model with given credentials. Password
    is automatically cached.
    """
    return CustomUser.objects.create_user(email, password, **kwargs)
