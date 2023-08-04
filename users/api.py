from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.constants import Role
from users.models import User
from users.serializers import UserCreateSerializer  # noqa
from users.serializers import UserRegistrationResponseSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    permission_classes = [AllowAny]

    def post(self, request):
        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        self.perform_create(create_serializer)

        public_serializer = UserRegistrationResponseSerializer(
            create_serializer.instance
        )
        headers = self.get_success_headers(public_serializer.data)

        return Response(
            public_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get(self, request, format=None):
        users = User.objects.all()
        user = self.request.user
        if user.role == Role.ADMIN or user.role == Role.MANAGER:
            serializer = UserRegistrationResponseSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {
                    "message": "You don't have permission to access this resource."  # noqa
                },
                status=403,
            )
