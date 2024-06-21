from datetime import datetime
from django.utils.timezone import now, make_aware
from model_bakery import baker
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory, APITestCase

from dashboard.models import Reservation
from dashboard.serializers import ReservationSerializer


class TestReservationSerializer(APITestCase):
    """ Test the `ReservationSerializer` """

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_serialization(self):
        """
        Test output of the `Reservation` serialization.
        """
        instance = baker.make(Reservation)

        actual = ReservationSerializer(instance=instance).data
        expected = {
            'hotel_id': instance.hotel_id,
            'total': instance.total,
            'period_type': instance.period_type,
            'period_start': instance.period_start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'period_end': instance.period_end.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.assertDictEqual(expected, actual)

    def test_deserialization_upsert_success_1(self):
        """
        Test the `Reservation` deserialization with valid payload
        for create action.
        """
        today = now()
        period_start = make_aware(datetime.combine(today, datetime.min.time()))
        period_end = make_aware(datetime.combine(today, datetime.max.time()))

        payload = {
            'hotel_id': 1,
            'total': 10,
            'period_type': Reservation.PERIOD_DAILY,
            'period_start': period_start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'period_end': period_end.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }

        request = self.factory.post('/')
        deserializer = ReservationSerializer(
            data=payload,
            context={'request': request}
        )

        try:
            deserializer.is_valid(raise_exception=True)
        except ValidationError:
            self.fail('Gotcha! You fail the test!')

        deserializer.save()

        self.assertEqual(Reservation.objects.count(), 1)

    def test_deserialization_upsert_success_2(self):
        """
        Test the `Reservation` deserialization with valid payload
        for update action.
        """
        today = now()
        period_start = make_aware(datetime.combine(today, datetime.min.time()))
        period_end = make_aware(datetime.combine(today, datetime.max.time()))

        baker.make(
            Reservation,
            hotel_id=1,
            period_type=Reservation.PERIOD_DAILY,
            period_start=period_start,
            period_end=period_end
        )

        payload = {
            'hotel_id': 1,
            'total': 20,
            'period_type': Reservation.PERIOD_DAILY,
            'period_start': period_start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'period_end': period_end.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }

        request = self.factory.post('/')
        deserializer = ReservationSerializer(
            data=payload,
            context={'request': request}
        )

        try:
            deserializer.is_valid(raise_exception=True)
        except ValidationError:
            self.fail('Gotcha! You fail the test!')

        deserializer.save()

        # Ensure there is no new `Reservation` instance is created
        self.assertEqual(Reservation.objects.count(), 1)

        # Ensure total reservation is updated
        self.assertEqual(deserializer.instance.total, 20)
