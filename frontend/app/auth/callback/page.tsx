// frontend/app/auth/callback/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { AlertCircle } from 'lucide-react';

export default function AuthCallback() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [debugInfo, setDebugInfo] = useState<string>('');

  useEffect(() => {
    async function handleCallback() {
      try {
        setDebugInfo('Starting authentication process...');
        
        const code = searchParams.get('code');
        const error = searchParams.get('error');

        if (error) {
          throw new Error(
            error === 'access_denied' 
              ? 'Login was cancelled' 
              : `Authentication error: ${error}`
          );
        }

        if (!code) {
          throw new Error('No authorization code received');
        }

        setDebugInfo('Got authorization code. Attempting to exchange for token...');

        // Test backend connectivity
        try {
          const healthCheck = await fetch('http://localhost:8000/');
          if (!healthCheck.ok) {
            throw new Error('Backend server is not responding');
          }
        } catch (e) {
          throw new Error('Cannot connect to backend server. Please ensure it is running.');
        }

        // Exchange code for token
        const response = await fetch('http://localhost:8000/auth/google/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            code,
            redirect_uri: `${window.location.origin}/auth/callback`
          }),
        });

        setDebugInfo('Received response from token endpoint...');

        if (!response.ok) {
          const errorData = await response.text();
          console.error('Token exchange failed:', errorData);
          throw new Error(`Failed to exchange token: ${errorData}`);
        }

        const data = await response.json();
        await login(data.access_token);

        setDebugInfo('Successfully logged in. Redirecting...');

        // Redirect to saved URL or home
        const redirectUrl = sessionStorage.getItem('redirectUrl') || '/';
        sessionStorage.removeItem('redirectUrl');
        router.push(redirectUrl);
      } catch (error) {
        console.error('Authentication error:', error);
        setError(
          error instanceof Error 
            ? error.message 
            : 'An unexpected error occurred'
        );
        setDebugInfo(`Error occurred: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    }

    handleCallback();
  }, [searchParams, login, router]);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center gap-2 text-red-600 mb-4">
            <AlertCircle className="h-5 w-5" />
            <h2 className="text-lg font-semibold">Authentication Error</h2>
          </div>
          <p className="text-gray-600 mb-4">{error}</p>
          {debugInfo && (
            <div className="bg-gray-50 p-4 rounded-md mb-4">
              <p className="text-sm text-gray-500 font-mono">{debugInfo}</p>
            </div>
          )}
          <div className="flex gap-4">
            <button
              onClick={() => router.push('/login')}
              className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Return to Login
            </button>
            <button
              onClick={() => window.location.reload()}
              className="flex-1 bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Completing sign in...</p>
        {debugInfo && (
          <p className="text-sm text-gray-500 mt-2">{debugInfo}</p>
        )}
      </div>
    </div>
  );
}