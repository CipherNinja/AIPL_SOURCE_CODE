from django.http import JsonResponse
import requests
from decouple import config
from django.core.cache import cache

class SecurityKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        key = config('SECURITY_KEY', default=None)
        employee_id = config('EMPLOYEE_ID', default=None)

        if not key or not employee_id:
            return JsonResponse(
                {"error": "SECURITY_KEY or EMPLOYEE_ID is missing. Access denied."},
                status=403,
            )

        # Check if the key is already validated in cache
        cached_key = cache.get(f"validated_key_{employee_id}")
        if cached_key == key:
            # Skip validation if the cached key matches
            return self.get_response(request)

        # Validate the key with the external server
        try:
            response = requests.get(
                f"https://supersecure.agratasinfotech.com/api/approve-key/{employee_id}/",
                timeout=5,
            )
            if response.status_code == 200:
                response_data = response.json()
                server_key = response_data.get("security_key")

                if server_key == key:
                    # Cache the validated key to avoid repeated checks
                    cache.set(f"validated_key_{employee_id}", key, timeout=3600)  # Cache for 1 hour
                    return self.get_response(request)
                else:
                    return JsonResponse(
                        {"error": "SECURITY_KEY does not match the approved key. Access denied."},
                        status=403,
                    )
            elif response.status_code == 403:
                return JsonResponse(
                    {"error": "Your request has not been approved yet. Access denied."},
                    status=403,
                )
            elif response.status_code == 404:
                return JsonResponse(
                    {"error": "No request found for the given Employee ID. Access denied."},
                    status=404,
                )
            else:
                return JsonResponse(
                    {"error": "Unexpected response from the validation server. Access denied."},
                    status=500,
                )
        except requests.RequestException as e:
            return JsonResponse(
                {"error": f"Unable to connect to validation server: {str(e)}. Access denied."},
                status=403,
            )
