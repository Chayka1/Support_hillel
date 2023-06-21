import json

from django.http import HttpResponse
from core.models import User


def create_user(request):
    if request.method != "POST":
        raise ValueError("Only POST method is allowed")

    data = json.loads(request.body)

    user = User.objects.create_user(**data)

    result = {
        "id": user.pk,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "role": user.role,
    }

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )
