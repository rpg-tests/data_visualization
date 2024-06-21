from rest_framework import generics

from dashboard.filters import ReservationFilter
from dashboard.models import Reservation
from dashboard.serializers import DashboardSerializer, ReservationSerializer


class DashboardView(generics.ListAPIView):
    serializer_class = DashboardSerializer
    filterset_class = ReservationFilter

    def get_queryset(self):
        sorted_list = ['hotel_id', 'period_type', 'period_start']
        return Reservation.objects.all().order_by(*sorted_list)


class ReservationView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
