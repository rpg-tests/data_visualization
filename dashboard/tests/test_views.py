from django.utils.timezone import now
from model_bakery.recipe import Recipe
from rest_framework.test import APIRequestFactory, APITestCase

from dashboard.filters import ReservationFilter
from dashboard.models import Reservation
from dashboard.serializers import DashboardSerializer, ReservationSerializer
from dashboard.views import DashboardView, ReservationView


class TestDashboardView(APITestCase):
    """ Test the `DashboardView` """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DashboardView()

    def test_get_serializer_class(self):
        self.assertEqual(
            self.view.get_serializer_class(),
            DashboardSerializer
        )

    def test_filterset_class(self):
        self.assertEqual(
            self.view.filterset_class,
            ReservationFilter
        )

    def test_get_queryset(self):
        """
        Test the `get_queryset` method returns `Reservation` instances
        sorted by [`hotel_id`, `period_type`, `period_start`] in ascending order.
        """
        today = now()
        hotel_one_recipe = Recipe(Reservation, hotel_id=1)
        hotel_two_recipe = Recipe(Reservation, hotel_id=2)

        hotel_2_reservation_1 = hotel_two_recipe.make(
            period_type=Reservation.PERIOD_YEARLY,
            period_start=today.replace(hour=12)
        )
        hotel_2_reservation_2 = hotel_two_recipe.make(
            period_type=Reservation.PERIOD_DAILY,
            period_start=today.replace(hour=9)
        )
        hotel_2_reservation_3 = hotel_two_recipe.make(
            period_type=Reservation.PERIOD_MONTHLY,
            period_start=today.replace(hour=16)
        )

        hotel_1_reservation_1 = hotel_one_recipe.make(
            period_type=Reservation.PERIOD_YEARLY,
            period_start=today.replace(hour=12)
        )
        hotel_1_reservation_2 = hotel_one_recipe.make(
            period_type=Reservation.PERIOD_DAILY,
            period_start=today.replace(hour=9)
        )
        hotel_1_reservation_3 = hotel_one_recipe.make(
            period_type=Reservation.PERIOD_MONTHLY,
            period_start=today.replace(hour=16)
        )

        self.view.request = self.factory.get('/')

        actual = self.view.get_queryset()
        expected = [
            hotel_1_reservation_2, hotel_1_reservation_3, hotel_1_reservation_1,
            hotel_2_reservation_2, hotel_2_reservation_3, hotel_2_reservation_1,
        ]
        self.assertQuerysetEqual(
            actual,
            expected,
            lambda item: item,
            ordered=True
        )


class TestReservationView(APITestCase):
    """ Test the `ReservationView` """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ReservationView()

    def test_get_serializer_class(self):
        self.assertEqual(
            self.view.get_serializer_class(),
            ReservationSerializer
        )
