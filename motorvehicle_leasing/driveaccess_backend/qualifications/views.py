from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import QualificationSerializer
from .models import Qualification
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class QualificationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qualifications = Qualification.objects.all()
        serializer = QualificationSerializer(qualifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QualificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QualificationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, qualification_id):
        try:
            return Qualification.objects.get(qualification_id=qualification_id)
        except Qualification.DoesNotExist:
            raise PermissionDenied("Qualification not found.")

    def get(self, request, qualification_id):
        qualification = self.get_object(qualification_id)
        serializer = QualificationSerializer(qualification)
        return Response(serializer.data)

    def put(self, request, qualification_id):
        qualification = self.get_object(qualification_id)
        serializer = QualificationSerializer(qualification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, qualification_id):
        qualification = self.get_object(qualification_id)
        serializer = QualificationSerializer(qualification, data=request.data, partial=True)  # partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, qualification_id):
        qualification = self.get_object(qualification_id)
        qualification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class QualificationApprove(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, qualification_id):
        qualification = Qualification.objects.get(qualification_id=qualification_id)
        if not request.user.is_admin:
            raise PermissionDenied("You do not have permission to approve qualifications.")
        
        qualification.approved = True
        qualification.save()
        return Response({"message": "Qualification approved successfully."}, status=status.HTTP_200_OK)
    

