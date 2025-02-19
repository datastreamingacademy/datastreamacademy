// frontend/app/lessons/[id]/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import LessonContentDisplay from '@/components/LessonContentDisplay';
import ProtectedRoute from '@/components/ProtectedRoute';
import { useAuth } from '@/contexts/AuthContext';
import { 
  Lesson, 
  NavigationInfo, 
  Resource, 
  UserProgress,
  DifficultyLevel,
  User
} from '@/types';

interface DifficultyBadgeProps {
  difficulty: DifficultyLevel;
}

const DifficultyBadge: React.FC<DifficultyBadgeProps> = ({ difficulty }) => {
  const colors = {
    [DifficultyLevel.BEGINNER]: 'bg-green-100 text-green-800',
    [DifficultyLevel.INTERMEDIATE]: 'bg-yellow-100 text-yellow-800',
    [DifficultyLevel.ADVANCED]: 'bg-red-100 text-red-800'
  };

  return (
    <span className={`px-2 py-1 rounded text-sm font-medium ${colors[difficulty]}`}>
      {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
    </span>
  );
};

interface LessonHeaderProps {
  lesson: Lesson;
  progress?: UserProgress | null;
}

const LessonHeader: React.FC<LessonHeaderProps> = ({ lesson, progress }) => {
  return (
    <div className="mb-8">
      <div className="flex justify-between items-start mb-4">
        <h1 className="text-3xl font-bold text-gray-900">{lesson.title}</h1>
        <div className="flex gap-2">
          <DifficultyBadge difficulty={lesson.difficulty} />
          {lesson.is_premium && (
            <span className="px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r from-yellow-200 to-yellow-100 text-yellow-700">
              Premium
            </span>
          )}
        </div>
      </div>
      <p className="text-xl text-gray-600">{lesson.description}</p>
      <div className="mt-4 flex gap-4 text-sm text-gray-500">
        <span>Estimated time: {lesson.estimated_time} minutes</span>
        <span>•</span>
        <span>Type: {lesson.lesson_type.replace('_', ' ')}</span>
        {progress && (
          <span>
            {progress.is_completed 
              ? '✓ Completed' 
              : progress.completed_at 
                ? `Completed on ${new Date(progress.completed_at).toLocaleDateString()}` 
                : 'Not Started'}
          </span>
        )}
      </div>
    </div>
  );
};

interface LessonNavigationProps {
  navigation: NavigationInfo;
}

const LessonNavigation: React.FC<LessonNavigationProps> = ({ navigation }) => {
  return (
    <div className="flex justify-between items-center py-6 border-t border-gray-200 mt-8">
      {navigation.previous ? (
        <Link
          href={`/lessons/${navigation.previous.id}`}
          className="flex items-center text-blue-600 hover:text-blue-800"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          <span>Previous: {navigation.previous.title}</span>
        </Link>
      ) : (
        <div></div>
      )}
      
      {navigation.next && (
        <Link
          href={`/lessons/${navigation.next.id}`}
          className="flex items-center text-blue-600 hover:text-blue-800"
        >
          <span>Next: {navigation.next.title}</span>
          <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      )}
    </div>
  );
};

interface ResourceCardProps {
  resource: Resource;
}

const ResourceCard: React.FC<ResourceCardProps> = ({ resource }) => {
  const icons: { [key: string]: string } = {
    notebook: '📓',
    code_sample: '💻',
    dataset: '📊',
    guide: '📖',
    presentation: '🎯'
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start">
        <span className="text-2xl mr-3">{icons[resource.type] || '📄'}</span>
        <div>
          <h3 className="font-medium text-gray-900">{resource.title}</h3>
          <p className="text-sm text-gray-500 mt-1">Type: {resource.type}</p>
        </div>
      </div>
    </div>
  );
};

interface ResourceSectionProps {
  lessonId: string | null;
}

const ResourceSection: React.FC<ResourceSectionProps> = ({ lessonId }) => {
  const [resources, setResources] = useState<Resource[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { getToken } = useAuth();

  useEffect(() => {
    async function fetchResources() {
      if (!lessonId) return;
      
      try {
        const token = getToken();
        const response = await fetch(`http://localhost:8000/lessons/${lessonId}/resources`, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
          },
        });
        
        if (!response.ok) {
          throw new Error(`Failed to fetch resources: ${response.status}`);
        }
        
        const data = await response.json();
        setResources(data.resources);
      } catch (error) {
        console.error('Error fetching resources:', error);
      } finally {
        setIsLoading(false);
      }
    }

    fetchResources();
  }, [lessonId, getToken]);

  if (!lessonId || isLoading) return null;
  if (resources.length === 0) return null;

  return (
    <div className="mt-12">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Additional Resources</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {resources.map((resource) => (
          <ResourceCard key={resource.id} resource={resource} />
        ))}
      </div>
    </div>
  );
};

export default function LessonPage() {
  const { user, getToken } = useAuth();
  const params = useParams();
  const lessonId = typeof params?.id === 'string' ? params.id : Array.isArray(params?.id) ? params.id[0] : null;
  
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [navigation, setNavigation] = useState<NavigationInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<UserProgress | null>(null);

  // Update lesson progress function
  const updateLessonProgress = async (isCompleted: boolean = true) => {
    try {
      const token = getToken();
      if (!token) {
        throw new Error('No authentication token found');
      }

      if (!lessonId) {
        throw new Error('No lesson ID available');
      }

      const response = await fetch(`http://localhost:8000/lessons/${lessonId}/progress`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ is_completed: isCompleted })
      });

      if (!response.ok) {
        throw new Error('Failed to update lesson progress');
      }

      const progressData = await response.json();
      setProgress(progressData);
    } catch (error) {
      console.error('Error updating lesson progress:', error);
    }
  };

  useEffect(() => {
    async function fetchData() {
      if (!lessonId) {
        setError('Invalid lesson ID');
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        setError(null);
        
        const token = getToken();
        const headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        };

        // Fetch lesson and navigation info in parallel
        const [lessonResponse, navigationResponse] = await Promise.all([
          fetch(`http://localhost:8000/lessons/${lessonId}`, { headers }),
          fetch(`http://localhost:8000/lessons/${lessonId}/navigation`, { headers })
        ]);

        if (!lessonResponse.ok) {
          throw new Error(`Failed to fetch lesson: ${lessonResponse.status}`);
        }

        const lessonData = await lessonResponse.json();
        const navigationData = await navigationResponse.json();

        // Check if lesson is premium and user has access
        if (lessonData.is_premium && (!user || !('is_premium' in user) || !user.is_premium)) {
          setError('This is a premium lesson. Please upgrade to access this content.');
          setIsLoading(false);
          return;
        }

        setLesson(lessonData);
        setNavigation(navigationData);

        // Fetch lesson progress if user is authenticated
        if (user && token) {
          const progressResponse = await fetch(`http://localhost:8000/lessons/${lessonId}/progress`, {
            headers
          });

          if (progressResponse.ok) {
            const progressData = await progressResponse.json();
            setProgress(progressData);
          }
        }
      } catch (error) {
        console.error('Error fetching lesson:', error);
        setError(
          error instanceof Error 
            ? `Failed to load lesson: ${error.message}`
            : 'Failed to load lesson. Please try again later.'
        );
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, [lessonId, user, getToken]);

  return (
    <ProtectedRoute>
      <main className="max-w-4xl mx-auto p-8">
        {isLoading && (
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="ml-2">Loading lesson...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
            <p className="font-medium">Error</p>
            <p>{error}</p>
            {error.includes('premium') && (
              <div className="mt-4">
                <Link 
                  href="/pricing" 
                  className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
                >
                  View Pricing Options
                </Link>
              </div>
            )}
          </div>
        )}

        {!isLoading && !error && lesson && (
          <>
            <LessonHeader lesson={lesson} progress={progress} />
            <LessonContentDisplay lesson={lesson} />
            <ResourceSection lessonId={lessonId} />
            {navigation && <LessonNavigation navigation={navigation} />}
            
            {/* Progress Tracking Button */}
            {user && !progress?.is_completed && (
              <div className="mt-8 text-center">
                <button
                  onClick={() => updateLessonProgress(true)}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                >
                  Mark Lesson as Completed
                </button>
              </div>
            )}
          </>
        )}
      </main>
    </ProtectedRoute>
  );
}