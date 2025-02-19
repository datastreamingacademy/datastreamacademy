// frontend/app/components/CourseCard.tsx
import React from 'react';
import Link from 'next/link';
import { Course, CourseCategory, ContentFormat } from '@/types';

interface CourseCardProps {
  course: Course;
}

export const CourseCard: React.FC<CourseCardProps> = ({ course }) => {
  const getCategoryIcon = (category: CourseCategory) => {
    switch (category) {
      case CourseCategory.SPARK:
        return '⚡';
      case CourseCategory.API:
        return '🔌';
      case CourseCategory.PYTHON:
        return '🐍';
      case CourseCategory.DATA_SCIENCE:
        return '📊';
      case CourseCategory.WEB_DEVELOPMENT:
        return '🌐';
      default:
        return '📚';
    }
  };

  const getFormatLabel = (format: ContentFormat): string => {
    // Split by underscore and capitalize each word
    const words = format.toString().split('_');
    return words.map((word: string) => 
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="p-4 border-b border-gray-100">
        <div className="flex justify-between items-start">
          <div className="flex items-center gap-2">
            <span className="text-2xl" role="img" aria-label={course.category}>
              {getCategoryIcon(course.category)}
            </span>
            <h2 className="text-xl font-semibold text-gray-800">{course.title}</h2>
          </div>
          {course.is_premium && (
            <span className="px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r from-yellow-200 to-yellow-100 text-yellow-700">
              Premium
            </span>
          )}
        </div>
      </div>
      
      <div className="p-4">
        <p className="text-gray-600 mb-4">{course.description}</p>
        
        {/* Tags */}
        {course.tags && course.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {course.tags.map((tagItem: string) => (
              <span key={tagItem} className="px-2 py-1 bg-gray-100 rounded-full text-sm text-gray-600">
                {tagItem}
              </span>
            ))}
          </div>
        )}
        
        {/* Prerequisites */}
        {course.prerequisites && course.prerequisites.length > 0 && (
          <div className="mb-4">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Prerequisites:</h3>
            <ul className="list-disc list-inside text-sm text-gray-600">
              {course.prerequisites.map((prerequisite: string) => (
                <li key={prerequisite}>{prerequisite}</li>
              ))}
            </ul>
          </div>
        )}
        
        {/* Content Formats */}
        {course.supported_content_formats && course.supported_content_formats.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {course.supported_content_formats.map((formatItem: ContentFormat) => (
              <span key={formatItem} className="px-2 py-1 bg-blue-100 rounded-full text-sm text-blue-600">
                {getFormatLabel(formatItem)}
              </span>
            ))}
          </div>
        )}
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
};

export default CourseCard;