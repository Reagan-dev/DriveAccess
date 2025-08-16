from django.urls import path
from .views import VehicleCreateView, VehicleListView, VehicleUpdateView

urlpatterns = [
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),  # GET all vehicles
    path('vehicles/create/', VehicleCreateView.as_view(), name='vehicle-create'),  # POST a new vehicle
    path('vehicles/<uuid:vehicle_id>/', VehicleUpdateView.as_view(), name='vehicle-update'),  # PUT to update vehicle details
]