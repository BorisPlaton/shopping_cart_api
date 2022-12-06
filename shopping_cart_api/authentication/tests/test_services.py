import pytest

from authentication.models import CustomUser
from authentication.services.services import create_user


@pytest.mark.django_db
class TestCustomUserServices:

    def test_create_user_creates_record_in_db(self, user_credentials):
        assert not CustomUser.objects.all().exists()
        new_user = create_user(**user_credentials)
        assert CustomUser.objects.first() == new_user

    def test_create_user_automatically_hash_password(self, user_credentials):
        new_user = create_user(**user_credentials)
        assert new_user.password != user_credentials['password']
