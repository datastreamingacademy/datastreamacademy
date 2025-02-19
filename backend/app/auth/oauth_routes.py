# backend/app/auth/oauth_routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Any
import traceback

from ..database import get_db
from ..models import User
from ..core.config import settings
from .google import verify_google_token, exchange_code_for_token, create_or_update_user_from_google
from .utils import create_access_token

router = APIRouter(prefix="/auth/google", tags=["auth"])

@router.post("/token")
async def google_auth(
    request: Request,
    db: Session = Depends(get_db)
) -> Any:
    """Handle Google OAuth authentication."""
    try:
        # Get request body
        data = await request.json()
        code = data.get("code")
        redirect_uri = data.get("redirect_uri")

        if not code:
            raise HTTPException(
                status_code=400,
                detail="Authorization code is required"
            )

        print(f"Received auth code: {code[:10]}...")  # Log first 10 chars of code
        print(f"Redirect URI: {redirect_uri}")
        print(f"Using client ID: {settings.GOOGLE_CLIENT_ID}")

        # Exchange authorization code for access token
        token_data = await exchange_code_for_token(code, redirect_uri)
        access_token = token_data.get("access_token")
        
        if not access_token:
            print("Failed to get access token from Google")
            raise HTTPException(
                status_code=400,
                detail="Could not get access token from Google"
            )

        print("Successfully got access token from Google")
        
        # Get user info from Google
        user_info = await verify_google_token(access_token)
        print(f"Got user info from Google: {user_info.get('email')}")
        
        # Create or update user in our database
        user = create_or_update_user_from_google(db, user_info)
        
        # Create our own JWT token
        token = create_access_token(
            data={
                "sub": user.email,
                "google_id": user.google_id
            }
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "picture": user.picture,
                "is_premium": user.is_premium
            }
        }
        
    except Exception as e:
        print(f"Error in google_auth: {str(e)}")
        print(f"Full error details: {traceback.format_exc()}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to authenticate with Google: {str(e)}"
        )