from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny



class SignupView(APIView):
    permission_classes = [AllowAny]  # 회원가입은 인증 필요 없음

    def post(self, request):
        supabase_id = request.data.get("supabase_id")
        email = request.data.get("email")
        role = request.data.get("role", "student")

        if not supabase_id or not email:
            return Response({"detail": "supabase_id and email are required"}, status=status.HTTP_400_BAD_REQUEST)

        profile, created = UserProfile.objects.update_or_create(
            email=email,
            defaults={
                "supabase_id": supabase_id,
                "role": role,
            },
        )

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)



class MyInfo(APIView): #내 정보 조회 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(email=request.user.email)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)



class Search(ListAPIView): #이메일 기반 검색 (권한줄때 필요)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # 로그인된 유저만 검색 가능하도록

    def get_queryset(self):
        email = self.request.query_params.get("email")
        return UserProfile.objects.filter(email__icontains=email)

class AvailableUserList(ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.exclude(pk=self.request.user.pk)