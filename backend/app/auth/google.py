# backend/app/auth/google.py
import httpx
from fastapi import HTTPException
from typing import Optional, Dict, Any
import json
from datetime import datetime
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models import User

async def exchange_code_for_token(code: str, redirect_uri: str) -> Dict[str, Any]:
    """Exchange authorization code for access token."""
    try:
        print(f"Exchanging code for token with following parameters:")
        print(f"Client ID: {settings.GOOGLE_CLIENT_ID}")
        print(f"Redirect URI: {redirect_uri}")
        
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        
        print("Making request to Google OAuth token endpoint...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data=data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            
            if not response.is_success:
                error_body = response.text
                print(f"Error response from Google: {error_body}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to exchange code for token: {error_body}"
                )
            
            token_data = response.json()
            print("Successfully received token data from Google")
            return token_data
            
    except httpx.HTTPError as e:
        print(f"HTTP error during token exchange: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to exchange code for token: {str(e)}"
        )
    except Exception as e:
        print(f"Unexpected error during token exchange: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during token exchange: {str(e)}"
        )

async def verify_google_token(token: str) -> Dict[str, Any]:
    """Verify Google OAuth token and get user info."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if not response.is_success:
                error_body = response.text
                print(f"Error response from Google userinfo: {error_body}")
                raise HTTPException(
                    status_code=401,
                    detail=f"Failed to verify token: {error_body}"
                )
            
            return response.json()
            
    except httpx.HTTPError as e:
        print(f"HTTP error during token verification: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=f"Failed to verify Google token: {str(e)}"
        )

def create_or_update_user_from_google(
    db_session: Session,
    user_info: Dict[str, Any]
) -> User:
    """Create or update user from Google OAuth data."""
    try:
        email = user_info.get("email")
        if not email:
            raise HTTPException(
                status_code=400,
                detail="Email not provided by Google"
            )
        
        # Check if user exists
        user = db_session.query(User).filter(User.email == email).first()
        
        if user:
            # Update existing user
            user.google_id = user_info.get("id")
            user.name = user_info.get("name")
            user.picture = user_info.get("picture")
            user.email_verified = user_info.get("verified_email", False)
            user.updated_at = datetime.utcnow()
        else:
            # Create new user
            user = User(
                email=email,
                username=email.split("@")[0],  # Use email prefix as username
                google_id=user_info.get("id"),
                name=user_info.get("name"),
                picture=user_info.get("picture"),
                is_active=True,
                email_verified=user_info.get("verified_email", False),
                is_premium=False  # New users start with free tier
            )
            db_session.add(user)
        
        db_session.commit()
        db_session.refresh(user)
        return user
        
    except Exception as e:
        db_session.rollback()
        print(f"Error creating/updating user: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create/update user: {str(e)}"
        )