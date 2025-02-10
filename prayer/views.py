from rest_framework.response import Response
from rest_framework.views import APIView

from .services.services import get_user_ip

class GetIpView(APIView):

    def get(self, request):
        ip = get_user_ip(request)
        return Response(ip)