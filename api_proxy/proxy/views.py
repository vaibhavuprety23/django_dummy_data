from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os
from dotenv import load_dotenv
import logging

load_dotenv()
CLIENT_API_BASE_URL = os.getenv("CLIENT_API_BASE_URL", "https://client-api.com")

CLIENT_API_BASE_URL = "https://jsonplaceholder.typicode.com"  # Replace with actual client API base URL





@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def forward_request(request, path):
    """Forward requests to the client's API."""
    url = f"{CLIENT_API_BASE_URL}/{path}"
    
    headers = {
        'Authorization': request.headers.get('Authorization', ''),  # Forward auth headers if needed
        'Content-Type': request.content_type
    }
    
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.body if request.method in ['POST', 'PUT'] else None,
            params=request.GET
        )
        return JsonResponse(response.json(), status=response.status_code, safe=False)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
