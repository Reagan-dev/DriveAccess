from django.urls import path
from .views import QualificationApprove, QualificationList, QualificationDetail

urlpatterns = [
    path('qualifications/', QualificationList.as_view(), name='qualification-list'),
    path('qualifications/<uuid:qualification_id>/', QualificationDetail.as_view(), name='qualification-detail'),
    path('qualifications/<uuid:qualification_id>/approve/', QualificationApprove.as_view(), name='qualification-approve'),
]