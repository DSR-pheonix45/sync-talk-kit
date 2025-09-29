from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Dict, Any
import structlog
from .config import settings

logger = structlog.get_logger()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Validate Supabase JWT token and return user information
    """
    try:
        token = credentials.credentials
        # Decode JWT without verification first to get the payload
        payload = jwt.decode(token, options={"verify_signature": False})

        # Verify the JWT signature with Supabase JWT secret
        decoded = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
            issuer="supabase"
        )

        # Return user info
        return {
            "user_id": decoded.get("sub"),
            "email": decoded.get("email"),
            "role": decoded.get("role", "authenticated"),
            "exp": decoded.get("exp"),
            "iat": decoded.get("iat")
        }

    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        logger.warning("Invalid JWT token", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    except Exception as e:
        logger.error("JWT validation error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
