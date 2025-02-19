// frontend/app/types.ts

// Course related types
export enum CourseCategory {
  SPARK = 'spark',
  API = 'api',
  PYTHON = 'python',
  DATA_SCIENCE = 'data_science',
  WEB_DEVELOPMENT = 'web_development'
}

export enum ContentFormat {
  CODE = 'code',
  TEXT = 'text',
  VIDEO = 'video',
  EXERCISE = 'exercise',
  QUIZ = 'quiz',
  API_PLAYGROUND = 'api_playground',
  INTERACTIVE_DEMO = 'interactive_demo'
}

export enum DifficultyLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced'
}

export interface Course {
  id: number;
  title: string;
  description: string;
  order: number;
  is_premium: boolean;
  category: CourseCategory;
  tags: string[];
  prerequisites: string[];
  target_audience: string;
  learning_outcomes: string[];
  supported_content_formats: ContentFormat[];
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Lesson related types
export interface Lesson {
  id: number;
  title: string;
  description: string;
  content: string;
  content_sections?: string | string[];
  code_samples?: string | string[];
  key_points?: string;
  order: number;
  difficulty: DifficultyLevel;
  lesson_type: string;
  estimated_time: number;
  learning_objectives: string;
  is_premium: boolean;
  course_id: number;
  created_at: string;
  updated_at: string;
}

export interface ContentSection {
  title: string;
  content: string;
  type: ContentFormat;
  order: number;
}

export interface CodeSample {
  title: string;
  language: string;
  code: string;
  description?: string;
}

// User related types
export interface User {
  id: number;
  email: string;
  name: string | null;
  picture: string | null;
  is_premium: boolean;
}

// Progress tracking types
export interface LessonProgress {
  lesson_id: number;
  is_completed: boolean;
  completed_at: string | null;
}

export interface CourseProgress {
  course_id: number;
  completed_lessons: number;
  total_lessons: number;
  last_accessed: string;
}

// Navigation types
export interface NavigationInfo {
  previous: {
    id: number;
    title: string;
  } | null;
  next: {
    id: number;
    title: string;
  } | null;
}

// Resource types
export interface Resource {
  id: number;
  title: string;
  type: string;
  content: string;
  description?: string;
  lesson_id: number;
}

export interface UserProgress {
  lesson_id: number;
  is_completed: boolean;
  completed_at?: string | null;
}

export interface NavigationInfo {
  previous: {
    id: number;
    title: string;
  } | null;
  next: {
    id: number;
    title: string;
  } | null;
}