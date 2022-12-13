import pytest
from django.urls import reverse
from model_bakery import baker

from authentication.models import CustomUser


@pytest.mark.django_db
class TestUserView:

    def test_when_new_user_created_his_credentials_and_id_are_returned(
            self, api_client, user_credentials_for_registration
    ):
        response = api_client.post(reverse('authentication:user-list'), user_credentials_for_registration)
        CustomUser.objects.all()
        assert response.status_code == 201
        response_data = response.data
        user_id = response_data.pop('id')
        assert user_id
        assert isinstance(user_id, int)
        for field, value in response.data.items():
            assert user_credentials_for_registration[field] == value

    def test_if_user_cannot_be_created_error_response_is_returned(
            self, api_client, user_credentials, user_credentials_for_registration
    ):
        CustomUser.objects.create_user(**user_credentials)
        response = api_client.post(reverse('authentication:user-list'), user_credentials_for_registration)
        assert response.status_code == 400

    def test_user_contact_information_is_created_via_put_request(self, api_client, contact_information):
        user = baker.make(CustomUser)
        response = api_client.put(
            reverse('authentication:user-detail', args=[user.pk]), contact_information
        )
        response_data = response.data
        assert response_data.keys() == {'id', 'location', 'phone_number'}
        user.refresh_from_db()
        assert response_data.pop('id') == user.contact_info.pk
        assert response.status_code == 201
        for field, value in response.data.items():
            assert contact_information[field] == value

    def test_second_contact_information_creation_will_cause_an_exception(self, api_client, contact_information):
        user = baker.make(CustomUser)
        api_client.put(
            reverse('authentication:user-detail', args=[user.pk]), contact_information
        )
        response = api_client.put(
            reverse('authentication:user-detail', args=[user.pk]), contact_information
        )
        assert response.status_code == 200
        assert response.data.keys() == {'id', 'location', 'phone_number'}
