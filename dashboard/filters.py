from django_filters import rest_framework as filters


from dashboard.models import Reservation


class ReservationFilter(filters.FilterSet):
    hotel_id = filters.NumberFilter(field_name='hotel_id')
    period = filters.ChoiceFilter(
        choices=Reservation.PERIOD_CHOICES,
        field_name='period_type',
    )

    class Meta:
        model = Reservation
        fields = ('hotel_id', 'period',)
