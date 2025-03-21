from rest_framework import viewsets
from rest_framework.response import Response
from faker import Faker

fake = Faker()

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        users = [{
            'name': fake.name(),
            'email': fake.email(),
            'address': fake.address()
        } for _ in range(10)]
        return Response(users)
