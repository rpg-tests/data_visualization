from django.urls import path

from dashboard.views import DashboardView, ReservationView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('reservations/', ReservationView.as_view(), name='reservations'),
]
