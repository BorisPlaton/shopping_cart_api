import pytest
from model_bakery import baker
from rest_framework.exceptions import NotFound

from authentication.models import CustomUser
from authentication.services.selectors import get_all_users, get_user_by_pk


@pytest.mark.django_db
class TestCustomUserSelectors:

    def test_get_all_users_returns_empty_queryset_if_none_is_stored_in_db(self):
        assert not CustomUser.objects.all().exists()
        assert not get_all_users()

    def test_get_all_users_returns_all_users_from_db(self):
        new_user = CustomUser.objects.create_user('test@test.com', 'qwerty')
        assert get_all_users().first() == new_user

    def test_get_user_by_pk_raises_an_exception_if_none_exists(self):
        with pytest.raises(NotFound):
            get_user_by_pk(1)

    def test_get_user_by_pk_returns_specific_user(self):
        created_user = baker.make(CustomUser)
        user = get_user_by_pk(created_user.pk)
        assert created_user == user
