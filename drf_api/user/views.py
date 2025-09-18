from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.response import Response

class MyInfo(APIView): #내 정보 조회 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

class Search(ListAPIView): #이메일 기반 검색 (권한줄때 필요)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # 로그인된 유저만 검색 가능하도록

    def get_queryset(self):
        email = self.request.query_params.get("email")
        return UserProfile.objects.filter(email__icontains=email)
