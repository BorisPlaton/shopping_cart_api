import pytest
from django.urls import reverse

from authentication.models import CustomUser


@pytest.mark.django_db
class TestUserView:

    def test_when_new_user_created_his_credentials_and_id_are_returned(
            self, api_client, user_credentials_for_registration
    ):
        response = api_client.post(reverse('authentication:user-detail'), user_credentials_for_registration)
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
        response = api_client.post(reverse('authentication:user-detail'), user_credentials_for_registration)
        assert response.status_code == 400
