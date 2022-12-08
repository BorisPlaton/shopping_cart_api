from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authentication.serializers import UserSerializer, ContactInformationSerializer
from authentication.services.selectors import get_all_users
from authentication.services.services import create_user_contact_information
from multiple_serializers.mixin import MultipleSerializerMixin


class UserView(MultipleSerializerMixin, GenericViewSet):
    """
    Handles the User model.
    """

    queryset = get_all_users()
    serializer_class = {
        'create': UserSerializer,
        'contact_information': ContactInformationSerializer,
    }

    def create(self, request: Request):
        """
        Registers a new user model with given credentials.
        """
        serializer: UserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_user = serializer.create(serializer.validated_data)
        return Response(self.get_serializer(created_user).data, status=201)

    @action(methods=['post'], detail=True)
    def contact_information(self, request: Request, pk: int):
        """
        Adds contact information to the specific user.
        """
        serializer: ContactInformationSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact_information = create_user_contact_information(pk, **serializer.validated_data)
        return Response(self.get_serializer(contact_information).data, status=201)
