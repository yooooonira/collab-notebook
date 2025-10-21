from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests
from dotenv import load_dotenv
import os
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

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
        email = request.user.email  # 또는 token의 claim에서
        try:
            profile = UserProfile.objects.get(email=email)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "User profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )


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
    
class Login(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Supabase로 로그인 (비밀번호 필요)
            supabase_response = requests.post(
                f"{SUPABASE_URL}/token?grant_type=password",
                json={"email": email, "password": password},
                headers={"apikey": SUPABASE_KEY}
            )

            if supabase_response.status_code != 200:
                return Response(
                    {"detail": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            supabase_data = supabase_response.json()
            
            # DB에서 일치 확인 
            try:
                profile = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                return Response(
                    {"detail": "User profile not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response({
                "access_token": supabase_data.get("access_token"),
                "token_type": supabase_data.get("token_type"),
                "user": UserProfileSerializer(profile).data
            })

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        