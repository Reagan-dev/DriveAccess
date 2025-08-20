from django.urls import path
from .views import PaymentDetailView, PaymentListCreateView, PaymentApprove, PaymentReject

urlpatterns = [
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('payments/<int:payment_id>/approve/', PaymentApprove.as_view(), name='payment-approve'),
    path('payments/<int:payment_id>/reject/', PaymentReject.as_view(), name='payment-reject'),
]