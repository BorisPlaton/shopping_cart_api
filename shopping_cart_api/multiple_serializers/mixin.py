from rest_framework.serializers import Serializer


class MultipleSerializerMixin:
    """
    Mixin for the viewsets that allows using multiple serializers
    in one view.
    """

    def get_serializer_class(self) -> Serializer:
        """
        Overrides base `get_serializer_class` method. Returns a specific
        serializer for a specific action.
        """
        serializer_class = super().get_serializer_class()
        if isinstance(serializer_class, dict):
            return self._get_serializer_from_dict()
        return serializer_class

    def _get_serializer_from_dict(self) -> Serializer:
        """
        Searches for the serializer of current action.
        """
        if serializer_class := self.serializer_class.get(self.action):
            return serializer_class
        for actions_tuple, serializer in self.serializer_class:
            if self.action in actions_tuple:
                return serializer
