from rest_framework.response import Response
from rest_framework.views import APIView

class GetIpAPI(APIView):

    def get(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        return Response(f'Ваш IP-адрес: {ip_address}')