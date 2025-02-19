// frontend/app/lessons/page.tsx
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Lesson {
  id: number;
  title: string;
  description: string;
  is_premium: boolean;
  order: number;
}

function LessonCard({ lesson }: { lesson: Lesson }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-300">
      {/* Card Header with Premium Badge */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex justify-between items-start">
          <h2 className="text-xl font-semibold text-gray-800">{lesson.title}</h2>
          {lesson.is_premium && (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r from-yellow-200 to-yellow-100 text-yellow-700">
              Premium
            </span>
          )}
        </div>
      </div>
      
      {/* Card Body */}
      <div className="p-4">
        <p className="text-gray-600">{lesson.description}</p>
      </div>
      
      {/* Card Footer */}
      <div className="px-4 py-3 bg-gray-50 flex justify-between items-center">
        <span className="text-sm text-gray-500">
          Lesson {lesson.order}
        </span>
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

export default function LessonsPage() {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchLessons() {
      try {
        const response = await fetch('http://localhost:8000/lessons');
        const data = await response.json();
        setLessons(data.lessons);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching lessons:', error);
        setIsLoading(false);
      }
    }

    fetchLessons();
  }, []);

  if (isLoading) {
    return (
      <div className="p-8">
        <p>Loading lessons...</p>
      </div>
    );
  }

  return (
    <main className="max-w-7xl mx-auto p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Available Lessons</h1>
        <p className="text-gray-600">Start your learning journey with our comprehensive Spark tutorials.</p>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {lessons.map((lesson) => (
          <LessonCard key={lesson.id} lesson={lesson} />
        ))}
      </div>
    </main>
  );
}