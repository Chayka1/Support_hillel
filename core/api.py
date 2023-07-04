from rest_framework.generics import CreateAPIView

from core.serializers import UserRegistrationSerializer  # noqa


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
