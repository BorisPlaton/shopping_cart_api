from authentication.models import CustomUser


def get_all_users():
    """
    Returns all users that are stored in the db.
    """
    return CustomUser.objects.all()
