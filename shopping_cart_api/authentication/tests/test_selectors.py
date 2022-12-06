import pytest

from authentication.models import CustomUser
from authentication.services.selectors import get_all_users


@pytest.mark.django_db
class TestCustomUserSelectors:

    def test_get_all_users_returns_empty_queryset_if_none_is_stored_in_db(self):
        assert not CustomUser.objects.all().exists()
        assert not get_all_users()

    def test_get_all_users_returns_all_users_from_db(self):
        new_user = CustomUser.objects.create_user('test@test.com', 'qwerty')
        assert get_all_users().first() == new_user
