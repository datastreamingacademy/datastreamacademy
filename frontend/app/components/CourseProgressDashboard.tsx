// frontend/app/components/CourseProgressDashboard.tsx
import React, { useState, useEffect } from 'react';
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Clock, Target, Trophy } from 'lucide-react';

interface WeeklyActivity {
  week: string;
  completed: number;
  minutes: number;
}

interface CourseProgressData {
  completionRate: number;
  totalLessons: number;
  completedLessons: number;
  weeklyActivity: WeeklyActivity[];
}

const CourseDashboard: React.FC = () => {
  const [courseProgress, setCourseProgress] = useState<CourseProgressData>({
    completionRate: 0,
    totalLessons: 0,
    completedLessons: 0,
    weeklyActivity: []
  });

  useEffect(() => {
    // Mock data for demonstration
    const mockProgress: CourseProgressData = {
      completionRate: 65,
      totalLessons: 24,
      completedLessons: 16,
      weeklyActivity: [
        { week: 'Week 1', completed: 4, minutes: 120 },
        { week: 'Week 2', completed: 3, minutes: 90 },
        { week: 'Week 3', completed: 5, minutes: 150 },
        { week: 'Week 4', completed: 4, minutes: 110 }
      ]
    };
    setCourseProgress(mockProgress);
  }, []);

  const progressColor = (percentage: number): string => {
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 50) return 'text-blue-600';
    return 'text-yellow-600';
  };

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Completion Rate</CardTitle>
            <Trophy className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              <span className={progressColor(courseProgress.completionRate)}>
                {courseProgress.completionRate}%
              </span>
            </div>
            <p className="text-xs text-gray-500">
              Overall course progress
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Lessons Completed</CardTitle>
            <Target className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {courseProgress.completedLessons}/{courseProgress.totalLessons}
            </div>
            <p className="text-xs text-gray-500">
              Total lessons completed
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Study Time</CardTitle>
            <Clock className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {courseProgress.weeklyActivity.reduce((acc, week) => acc + week.minutes, 0)} mins
            </div>
            <p className="text-xs text-gray-500">
              Total study time
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Weekly Activity Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Weekly Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={courseProgress.weeklyActivity}>
                <defs>
                  <linearGradient id="colorMinutes" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="week" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="minutes" 
                  stroke="#3B82F6" 
                  fillOpacity={1} 
                  fill="url(#colorMinutes)" 
                  name="Study Minutes"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Lessons Completion Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Lessons Completed</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={courseProgress.weeklyActivity}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="week" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar 
                  dataKey="completed" 
                  fill="#10B981" 
                  name="Lessons Completed"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CourseDashboard;