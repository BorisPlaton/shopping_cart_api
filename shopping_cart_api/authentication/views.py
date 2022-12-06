from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.serializers import UserSerializer
from authentication.services.selectors import get_all_users


class UserView(GenericAPIView):
    """
    Handles the User model.
    """
    queryset = get_all_users()
    serializer_class = UserSerializer

    def post(self, request: Request):
        """
        Registers a new user model with given credentials.
        """
        serializer: UserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_user = serializer.create(serializer.validated_data)
        return Response(self.get_serializer(created_user).data, status=201)
