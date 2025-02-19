// frontend/app/layout.tsx
import type { Metadata } from "next";
import { AuthProvider } from './contexts/AuthContext';
import NavHeader from './components/NavHeader';
import "./globals.css";

export const metadata: Metadata = {
  title: "Spark Tutorial Platform",
  description: "Learn Apache Spark with interactive tutorials",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <AuthProvider>
          <div className="flex flex-col min-h-screen">
            <NavHeader />
            <main className="flex-grow">
              {children}
            </main>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}