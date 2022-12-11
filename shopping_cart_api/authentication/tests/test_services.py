import pytest
from model_bakery import baker
from rest_framework.exceptions import NotFound

from authentication.models import CustomUser, ContactInformation
from authentication.services.services import create_user, create_user_contact_information
from exceptions.http_exceptions import StateConflict


@pytest.mark.django_db
class TestCustomUserServices:

    def test_create_user_creates_record_in_db(self, user_credentials):
        assert not CustomUser.objects.all().exists()
        new_user = create_user(**user_credentials)
        assert CustomUser.objects.first() == new_user

    def test_create_user_automatically_hash_password(self, user_credentials):
        new_user = create_user(**user_credentials)
        assert new_user.password != user_credentials['password']


@pytest.mark.django_db
class TestContactInformationServices:

    def test_if_user_doesnt_exist_contact_information_will_not_be_created(self, contact_information):
        assert not ContactInformation.objects.all().exists()
        with pytest.raises(NotFound):
            create_user_contact_information(1, **contact_information)
        assert not ContactInformation.objects.all().exists()

    def test_contact_information_is_successfully_created_if_user_exists(self, contact_information):
        user = baker.make(CustomUser)
        assert not ContactInformation.objects.all().exists()
        contact_info = create_user_contact_information(user.pk, **contact_information)
        assert user.contact_info == contact_info

    def test_if_user_has_already_contact_information_exception_is_raised(self, contact_information):
        user = baker.make(CustomUser)
        create_user_contact_information(user.pk, **contact_information)
        with pytest.raises(StateConflict):
            create_user_contact_information(user.pk, **contact_information)
