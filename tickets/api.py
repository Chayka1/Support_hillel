from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tickets.models import Ticket
from tickets.permissions import IsOwner, RoleIsAdmin, RoleIsManager, RoleIsUser
from tickets.serializers import TicketAssignSerializer, TicketSerializer
from users.constants import Role


class TicketAPIViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        all_tickets = Ticket.objects.all()
        user = self.request.user

        if user.role == Role.ADMIN:
            return all_tickets
        elif user.role == Role.MANAGER:
            return all_tickets.filter(Q(manager=user) | Q(manager=None))
        else:
            # User's role fallback solution
            return all_tickets.filter(user=user)

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
        elif self.action == "create":
            permission_classes = [RoleIsUser]
        elif self.action == "retrieve":
            permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
        elif self.action == "update":
            permission_classes = [RoleIsAdmin | RoleIsManager]
        elif self.action == "destroy":
            permission_classes = [RoleIsAdmin | RoleIsManager]
        elif self.action == "take":
            permission_classes = [RoleIsManager]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["put"])
    def take(self, request, pk):
        ticket = self.get_object()

        serializer = TicketAssignSerializer(
            data={"manager_id": request.user.id}
        )  # noqa
        serializer.is_valid()
        ticket = serializer.assign(ticket)
        return Response(TicketSerializer(ticket).data)

    @action(detail=True, methods=["put"])
    def reassign(self, request, pk):
        if request.user.role != Role.ADMIN:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
            )
        ticket = self.get_object()

        serializer = TicketAssignSerializer(
            data={"manager_id": request.data["user_id"]}
        )  # noqa
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)


class MessageListCreateAPIView(ListCreateAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        return NotImplementedError