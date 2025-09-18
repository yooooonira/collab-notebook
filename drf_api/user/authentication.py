from __future__ import annotations

import os
import base64
import logging
from typing import Optional, Tuple, Any

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .models import UserProfile

logger = logging.getLogger(__name__)


def _get_supabase_url() -> str:
    url = (getattr(settings, "SUPABASE_URL", None) or os.getenv("SUPABASE_URL") or "").rstrip("/")
    if not url:
        raise AuthenticationFailed("Server misconfigured: SUPABASE_URL not set")
    return url

def _get_supabase_secret_bytes() -> bytes:
    s = getattr(settings, "SUPABASE_JWT_SECRET", None) or os.getenv("SUPABASE_JWT_SECRET")
    if not s or not isinstance(s, str):
        raise AuthenticationFailed("Server misconfigured: SUPABASE_JWT_SECRET not set")
    return s.encode("utf-8")



class SupabaseAuthentication(BaseAuthentication):
    audience: str = "authenticated"
    leeway_seconds: int = 10

    def authenticate(self, request) -> Optional[Tuple[UserProfile, Any]]:
        auth = get_authorization_header(request).split()
        if len(auth) != 2 or auth[0].lower() != b"bearer":
            return None

        try:
            token = auth[1].decode("utf-8")
        except Exception:
            raise AuthenticationFailed("Invalid Authorization header encoding")

        supabase_url = _get_supabase_url()
        secret = _get_supabase_secret_bytes()

        try:
            payload = jwt.decode(
                token,
                secret,
                algorithms=["HS256"],
                audience=self.audience,
                issuer=f"{supabase_url}/auth/v1",
                leeway=self.leeway_seconds,
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidAudienceError:
            raise AuthenticationFailed("Invalid audience")
        except jwt.InvalidIssuerError:
            raise AuthenticationFailed("Invalid issuer")
        except jwt.InvalidSignatureError:
            raise AuthenticationFailed("Invalid signature")
        except Exception as e:
            logger.exception("Supabase JWT decode failed")
            raise AuthenticationFailed(f"Supabase decode error: {e}")

        user_id = payload.get("sub")
        email = payload.get("email") or (payload.get("user_metadata") or {}).get("email")

        if not user_id or not email:
            logger.error("Missing sub/email in payload: %s", payload)
            raise AuthenticationFailed("Invalid Supabase payload")

        user, created = UserProfile.objects.get_or_create(
            supabase_id=user_id,
            defaults={"email": email},
        )
        if not created and user.email != email:
            user.email = email
            user.save(update_fields=["email"])

        return (user, payload)