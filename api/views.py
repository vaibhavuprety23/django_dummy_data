from rest_framework import viewsets
from rest_framework.response import Response
from faker import Faker
from .models import User
from .serializers import UserSerializer

fake = Faker()

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.all()  # Fetch users from DB
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Generate and store 10 dummy users in PostgreSQL"""
        for _ in range(10):
            User.objects.create(
                name=fake.name(),
                email=fake.email(),
                address=fake.address(),
            )
        return Response({"message": "Dummy users added successfully!"})
