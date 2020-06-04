from rest_framework.generics import RetrieveAPIView
from delivaryapp.models import Orders
from api.serializer import SingleOrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class SingleOrdersView(RetrieveAPIView):
    queryset = Orders.objects.all()
    serializer_class = SingleOrderSerializer


class CountActiveOrderSView(APIView):

    def get(self, request):
        l = len(Orders.objects.filter(is_closed=False, is_active=False))
        return Response({'aolenth': l})
