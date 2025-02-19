// frontend/app/page.tsx
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import type { Course } from './types';

function CourseCard({ course }: { course: Course }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="p-4 border-b border-gray-100">
        <div className="flex justify-between items-start">
          <h2 className="text-xl font-semibold text-gray-800">{course.title}</h2>
          {course.is_premium && (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r from-yellow-200 to-yellow-100 text-yellow-700">
              Premium
            </span>
          )}
        </div>
      </div>
      
      <div className="p-4">
        <p className="text-gray-600">{course.description}</p>
      </div>
      
      <div className="px-4 py-3 bg-gray-50 flex justify-between items-center">
        <span className="text-sm text-gray-500">
          Course {course.order}
        </span>
        <Link 
          href={`/courses/${course.id}`}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          View Course
        </Link>
      </div>
    </div>
  );
}

export default function HomePage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchCourses() {
      try {
        setError(null);
        console.log('Attempting to fetch courses...');
        
        const response = await fetch('http://localhost:8000/courses', {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          },
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Received data:', data);
        
        setCourses(data.courses || data); // Handle both {courses: [...]} and direct array response
      } catch (error) {
        console.error('Error details:', error);
        setError(
          error instanceof Error 
            ? `Failed to load courses: ${error.message}` 
            : 'Failed to load courses. Please ensure the backend server is running.'
        );
      } finally {
        setIsLoading(false);
      }
    }

    fetchCourses();
  }, []);

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="ml-2">Loading courses...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
          <p className="font-medium">Error</p>
          <p className="text-sm">{error}</p>
          <p className="text-sm mt-2">
            Please ensure:
            <ul className="list-disc ml-5 mt-1">
              <li>The backend server is running on port 8000</li>
              <li>You can access http://localhost:8000/courses in your browser</li>
              <li>Your network connection is stable</li>
            </ul>
          </p>
        </div>
      </div>
    );
  }

  return (
    <main className="max-w-7xl mx-auto p-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Spark Tutorial
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Start your learning journey with our comprehensive Apache Spark courses
        </p>
      </div>
      
      {courses.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-600">No courses available at the moment.</p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {courses.map((course) => (
            <CourseCard key={course.id} course={course} />
          ))}
        </div>
      )}
    </main>
  );
}