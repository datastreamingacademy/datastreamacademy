import React, { useEffect } from 'react';
import { Code } from 'lucide-react';
import Prism from 'prismjs';
import CopyButton from './CopyButton';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-scala';

interface ContentSectionData {
  title: string;
  content: string;
  type: 'text' | 'code' | 'exercise';
  order: number;
}

interface CodeSample {
  title: string;
  language: string;
  code: string;
  description?: string;
}

interface Lesson {
  id: number;
  title: string;
  content: string;
  content_sections?: string; // JSON string
  code_samples?: string; // JSON string
  key_points?: string;
  learning_objectives: string;
}

interface ContentSectionProps {
  section: ContentSectionData;
}

interface CodeBlockProps {
  code: string;
  language?: string;
  title?: string;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ 
  code, 
  language = 'python',
  title 
}) => {
  return (
    <div className="relative">
      {title && (
        <div className="flex items-center gap-2 mb-2 text-gray-700">
          <Code size={20} />
          <span className="font-medium">{title}</span>
        </div>
      )}
      <pre className="!bg-gray-900 !p-4 rounded-lg overflow-x-auto">
        <CopyButton code={code} />
        <code className={`language-${language}`}>{code}</code>
      </pre>
    </div>
  );
};

const ContentSection: React.FC<ContentSectionProps> = ({ section }) => {
  useEffect(() => {
    Prism.highlightAll();
  }, [section]);

  const getContent = () => {
    switch (section.type) {
      case 'code':
        return (
          <div className="bg-gray-50 rounded-lg p-4 my-4">
            <CodeBlock 
              code={section.content}
              title={section.title}
            />
          </div>
        );
      
      case 'exercise':
        return (
          <div className="border-l-4 border-blue-500 bg-blue-50 p-4 my-4 rounded-r-lg">
            <h3 className="font-semibold text-blue-900 mb-2">{section.title}</h3>
            <div className="prose text-blue-800">
              {section.content}
            </div>
          </div>
        );
      
      default:
        return (
          <div className="my-4">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">{section.title}</h3>
            <div className="prose text-gray-700">
              {section.content.split('\n').map((paragraph: string, index: number) => (
                <p key={index} className="mb-4">{paragraph}</p>
              ))}
            </div>
          </div>
        );
    }
  };

  return getContent();
};

interface LessonContentDisplayProps {
  lesson: Lesson | null;
}

const LessonContentDisplay: React.FC<LessonContentDisplayProps> = ({ lesson }) => {
  useEffect(() => {
    Prism.highlightAll();
  }, [lesson]);

  // Early return if lesson is null
  if (!lesson) {
    return null;
  }

  if (!lesson.content_sections) {
    return (
      <div className="prose max-w-none">
        {lesson.content.split('\n').map((paragraph: string, index: number) => (
          <p key={index} className="mb-4">{paragraph}</p>
        ))}
      </div>
    );
  }

  const sections: ContentSectionData[] = JSON.parse(lesson.content_sections);

  return (
    <div className="max-w-4xl mx-auto">
      {/* Key Points Section */}
      {lesson.key_points && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
          <h2 className="text-xl font-semibold text-yellow-900 mb-4">Key Points</h2>
          <ul className="list-disc list-inside space-y-2 text-yellow-900">
            {lesson.key_points.split('\n').map((point: string, index: number) => (
              <li key={index} className="ml-4">{point.replace(/^\d+\.\s*/, '')}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Learning Objectives */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
        <h2 className="text-xl font-semibold text-blue-900 mb-4">Learning Objectives</h2>
        <div className="prose text-blue-800">
          {lesson.learning_objectives.split('\n').map((objective: string, index: number) => (
            <p key={index} className="mb-2">{objective}</p>
          ))}
        </div>
      </div>

      {/* Main Content Sections */}
      {sections.map((section, index) => (
        <ContentSection key={index} section={section} />
      ))}

      {/* Code Samples */}
      {lesson.code_samples && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Code Examples</h2>
          {JSON.parse(lesson.code_samples).map((sample: CodeSample, index: number) => (
            <div key={index} className="bg-gray-50 rounded-lg p-4 mb-4">
              {sample.description && (
                <p className="text-gray-600 mb-2">{sample.description}</p>
              )}
              <CodeBlock 
                code={sample.code}
                language={sample.language}
                title={sample.title}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LessonContentDisplay;