import pytest

from authentication.serializers import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:

    def test_repeat_password_field_is_required_for_deserialization(self, user_credentials):
        serializer = UserSerializer(data=user_credentials)
        assert not serializer.is_valid()

    def test_repeat_password_must_match_password_field(self, user_credentials):
        user_credentials.update({'repeat_password': user_credentials.get('password') + '1'})
        serializer = UserSerializer(data=user_credentials)
        assert not serializer.is_valid()

    def test_create_method_creates_valid_user_record(self, user_credentials_for_registration):
        serializer = UserSerializer(data=user_credentials_for_registration)
        serializer.is_valid()
        new_user = serializer.create(serializer.validated_data)
        user_credentials_for_registration.pop('repeat_password')
        assert user_credentials_for_registration.pop('password') != new_user.password
        for field, value in user_credentials_for_registration.items():
            assert getattr(new_user, field) == value
