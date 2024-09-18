from rest_framework.views import APIView
from rest_framework.response import Response

from taskmanager.tasks import send_test_email

# Create your views here.

class ExecuteTask(APIView):
    @staticmethod
    def get(request):
        send_test_email.apply_async()
        return Response({"success": "True", "message": "executed successfully", "data": []})
