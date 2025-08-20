from django.urls import path
from .views import LeaseList, LeaseApprove, LeaseReject, LeaseReturn, LeaseDetail, LeaseStatusList

urlpatterns = [
    path('leases/', LeaseList.as_view(), name='lease-list'),
    path('leases/<int:lease_id>/approve/', LeaseApprove.as_view(), name='lease-approve'),
    path('leases/<int:lease_id>/reject/', LeaseReject.as_view(), name='lease-reject'),
    path('leases/<int:lease_id>/return/', LeaseReturn.as_view(), name='lease-return'),
    path('leases/<int:pk>/', LeaseDetail.as_view(), name='lease-detail'),
    path('leases/status/', LeaseStatusList.as_view(), name='lease-status-list'),
]
