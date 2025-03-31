import json
from django.http import JsonResponse
from django.views import View
from jsonapi.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import os

with open('jsonapi/data.json', 'r') as file:
    data = json.load(file)


class JSONDataView(View):
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(__file__), 'data.json')
        
        with open(file_path, 'r') as file:
            data = json.load(file)

        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for testing
class JSONDataView(View):
    def get(self, request, *args, **kwargs):
        """Retrieve all stored users."""
        users = list(UserProfile.objects.values())  # Convert QuerySet to list
        return JsonResponse(users, safe=False)

    def post(self, request, *args, **kwargs):
        """Store new JSON data from the request body."""
        try:
            data = json.loads(request.body.decode('utf-8'))  # Parse JSON request
            
            # Create a new UserProfile instance
            user = UserProfile.objects.create(**data)

            return JsonResponse({"message": "User stored", "user_id": user.id}, status=201)
        except IntegrityError:
            return JsonResponse({"error": "User with this email already exists"}, status=400)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)