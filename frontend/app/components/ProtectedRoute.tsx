// frontend/app/components/ProtectedRoute.tsx
'use client';

import { useAuth } from '../contexts/AuthContext';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { user, isLoading, getToken } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Don't redirect while loading
    if (isLoading) return;

    // If no user and not loading, redirect to login
    if (!user && !getToken()) {
      // Save the attempted URL to redirect back after login
      sessionStorage.setItem('redirectUrl', pathname);
      router.push('/login');
    }
  }, [user, isLoading, router, pathname, getToken]);

  // Show loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="ml-2">Loading...</p>
      </div>
    );
  }

  // If not logged in, don't render anything
  if (!user) {
    return null;
  }

  // If logged in, render the protected content
  return <>{children}</>;
};

export default ProtectedRoute;