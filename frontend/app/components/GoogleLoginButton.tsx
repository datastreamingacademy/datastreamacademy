// frontend/app/components/GoogleLoginButton.tsx
'use client';

import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';

const GoogleLoginButton = () => {
  const [error, setError] = useState<string | null>(null);

  const handleGoogleLogin = () => {
    try {
      const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
      if (!clientId) {
        throw new Error('Google client ID is not configured');
      }

      // Google OAuth configuration
      const GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth";
      const REDIRECT_URI = `${window.location.origin}/auth/callback`;
      
      // Required OAuth parameters
      const params = new URLSearchParams({
        client_id: clientId,
        redirect_uri: REDIRECT_URI,
        response_type: "code",
        scope: "openid email profile",
        access_type: "offline",
        prompt: "consent",
      });

      // Redirect to Google's OAuth page
      window.location.href = `${GOOGLE_AUTH_URL}?${params.toString()}`;
    } catch (error) {
      console.error('Error initiating Google login:', error);
      setError(
        error instanceof Error 
          ? error.message 
          : 'Failed to initiate Google login'
      );
    }
  };

  if (error) {
    return (
      <div className="text-center p-4 bg-red-50 rounded-lg">
        <div className="flex items-center justify-center gap-2 text-red-600 mb-2">
          <AlertCircle size={20} />
          <p className="font-medium">Configuration Error</p>
        </div>
        <p className="text-sm text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <button
      onClick={handleGoogleLogin}
      className="flex items-center justify-center gap-2 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm bg-white hover:bg-gray-50 transition-colors"
    >
      {/* Google Icon */}
      <svg 
        viewBox="0 0 24 24" 
        width="24" 
        height="24" 
        className="w-6 h-6"
      >
        <path
          fill="#4285F4"
          d="M23.745 12.27c0-.79-.07-1.54-.19-2.27h-11.3v4.51h6.47c-.29 1.48-1.14 2.73-2.4 3.58v3h3.86c2.26-2.09 3.56-5.17 3.56-8.82z"
        />
        <path
          fill="#34A853"
          d="M12.255 24c3.24 0 5.95-1.08 7.93-2.91l-3.86-3c-1.08.72-2.45 1.16-4.07 1.16-3.13 0-5.78-2.11-6.73-4.96h-3.98v3.09C3.515 21.3 7.565 24 12.255 24z"
        />
        <path
          fill="#FBBC05"
          d="M5.525 14.29c-.25-.72-.38-1.49-.38-2.29s.14-1.57.38-2.29V6.62h-3.98a11.86 11.86 0 000 10.76l3.98-3.09z"
        />
        <path
          fill="#EA4335"
          d="M12.255 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C18.205 1.19 15.495 0 12.255 0c-4.69 0-8.74 2.7-10.71 6.62l3.98 3.09c.95-2.85 3.6-4.96 6.73-4.96z"
        />
      </svg>
      
      <span className="text-gray-700 font-medium">
        Continue with Google
      </span>
    </button>
  );
};

export default GoogleLoginButton;