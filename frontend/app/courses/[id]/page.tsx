// frontend/app/courses/[id]/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import type { Course, Lesson } from '../../types';

function DifficultyBadge({ difficulty }: { difficulty: Lesson['difficulty'] }) {
  const colors = {
    beginner: 'bg-green-100 text-green-800',
    intermediate: 'bg-yellow-100 text-yellow-800',
    advanced: 'bg-red-100 text-red-800'
  };

  return (
    <span className={`px-2 py-1 rounded text-sm font-medium ${colors[difficulty]}`}>
      {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
    </span>
  );
}

function LessonCard({ lesson }: { lesson: Lesson }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="p-4 border-b border-gray-100">
        <div className="flex justify-between items-start">
          <h3 className="text-xl font-semibold text-gray-800">{lesson.title}</h3>
          <div className="flex gap-2">
            <DifficultyBadge difficulty={lesson.difficulty} />
            {lesson.is_premium && (
              <span className="px-2 py-1 rounded text-sm font-medium bg-gradient-to-r from-yellow-200 to-yellow-100 text-yellow-700">
                Premium
              </span>
            )}
          </div>
        </div>
      </div>
      
      <div className="p-4">
        <p className="text-gray-600 mb-4">{lesson.description}</p>
        <div className="flex gap-4 text-sm text-gray-500">
          <span>Type: {lesson.lesson_type.replace('_', ' ')}</span>
          <span>•</span>
          <span>{lesson.estimated_time} minutes</span>
        </div>
      </div>
      
      <div className="px-4 py-3 bg-gray-50 flex justify-between items-center">
        <div className="text-sm text-gray-500">
          Lesson {lesson.order}
        </div>
        <Link 
          href={`/lessons/${lesson.id}`}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Start Lesson
        </Link>
      </div>
    </div>
  );
}

export default function CoursePage() {
  const params = useParams();
  const courseId = typeof params?.id === 'string' ? params.id : Array.isArray(params?.id) ? params.id[0] : null;
  
  const [course, setCourse] = useState<Course | null>(null);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchCourseAndLessons() {
      if (!courseId) {
        setError('Invalid course ID');
        setIsLoading(false);
        return;
      }

      try {
        setError(null);
        console.log('Attempting to fetch course data...');

        // Fetch course data
        console.log(`Fetching course: http://localhost:8000/courses/${courseId}`);
        const courseResponse = await fetch(`http://localhost:8000/courses/${courseId}`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
        });

        if (!courseResponse.ok) {
          throw new Error(`Course fetch failed with status: ${courseResponse.status}`);
        }

        const courseData = await courseResponse.json();
        console.log('Course data received:', courseData);

        // Fetch lessons data
        console.log(`Fetching lessons: http://localhost:8000/courses/${courseId}/lessons`);
        const lessonsResponse = await fetch(`http://localhost:8000/courses/${courseId}/lessons`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
        });

        if (!lessonsResponse.ok) {
          throw new Error(`Lessons fetch failed with status: ${lessonsResponse.status}`);
        }

        const lessonsData = await lessonsResponse.json();
        console.log('Lessons data received:', lessonsData);

        setCourse(courseData);
        setLessons(lessonsData.lessons || []);
      } catch (error) {
        console.error('Error details:', error);
        setError(
          error instanceof Error 
            ? `Failed to load course: ${error.message}` 
            : 'Failed to load course. Please ensure the backend server is running.'
        );
      } finally {
        setIsLoading(false);
      }
    }

    fetchCourseAndLessons();
  }, [courseId]);

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="ml-2">Loading course...</p>
        </div>
      </div>
    );
  }

  if (error || !course) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
          <p className="font-medium">Error</p>
          <p>{error || 'Course not found'}</p>
          <div className="mt-2">
            <p className="text-sm font-medium">Troubleshooting steps:</p>
            <ul className="list-disc ml-5 mt-1 text-sm">
              <li>Ensure the backend server is running on port 8000</li>
              <li>Check that the course ID is valid</li>
              <li>Try refreshing the page</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <main className="max-w-7xl mx-auto p-8">
      <div className="mb-8">
        <div className="flex justify-between items-start mb-4">
          <h1 className="text-3xl font-bold text-gray-900">{course.title}</h1>
          {course.is_premium && (
            <span className="px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r from-yellow-200 to-yellow-100 text-yellow-700">
              Premium Course
            </span>
          )}
        </div>
        <p className="text-xl text-gray-600">{course.description}</p>
      </div>
      
      {lessons.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-600">No lessons available for this course yet.</p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {lessons.map((lesson) => (
            <LessonCard key={lesson.id} lesson={lesson} />
          ))}
        </div>
      )}
    </main>
  );
}