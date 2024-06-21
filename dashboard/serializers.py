from rest_framework import serializers

from dashboard.models import Reservation


class DashboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = (
            'hotel_id',
            'total',
            'period_type',
            'period_start',
            'period_end',
        )
        read_only = fields


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = (
            'hotel_id',
            'total',
            'period_type',
            'period_start',
            'period_end',
        )

    def create(self, validated_data):
        """
        This method is overriden to support upsert operation.
        """
        total = validated_data.pop('total')
        obj, _ = Reservation.objects.update_or_create(
            **validated_data,
            defaults={'total': total}
        )

        return obj
