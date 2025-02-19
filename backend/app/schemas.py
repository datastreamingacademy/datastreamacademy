# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import DifficultyLevel, LessonType
import json

class ContentSection(BaseModel):
    title: str
    content: str
    order: int
    type: str  # 'text', 'code', 'exercise', etc.

class CodeSample(BaseModel):
    title: str
    code: str
    language: str
    description: Optional[str] = None

class ResourceBase(BaseModel):
    title: str
    type: str
    content: str
    description: Optional[str] = None

class ResourceCreate(ResourceBase):
    lesson_id: int

class ResourceRead(ResourceBase):
    id: int
    lesson_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    title: str
    description: str
    summary: str
    content: str
    content_sections: Optional[List[Dict[str, Any]]] = []
    code_samples: Optional[List[Dict[str, Any]]] = []
    key_points: Optional[str] = None
    order: int
    difficulty: DifficultyLevel
    lesson_type: LessonType
    estimated_time: int
    skill_level_required: Optional[str] = None
    learning_objectives: str
    is_premium: bool = False

class LessonCreate(LessonBase):
    course_id: int
    prerequisite_ids: Optional[List[int]] = []

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    content_sections: Optional[List[Dict[str, Any]]] = None
    code_samples: Optional[List[Dict[str, Any]]] = None
    key_points: Optional[str] = None
    order: Optional[int] = None
    difficulty: Optional[DifficultyLevel] = None
    lesson_type: Optional[LessonType] = None
    estimated_time: Optional[int] = None
    skill_level_required: Optional[str] = None
    learning_objectives: Optional[str] = None
    is_premium: Optional[bool] = None
    prerequisite_ids: Optional[List[int]] = None

class LessonRead(BaseModel):
    id: int
    title: str
    description: str
    content: str
    content_sections: List[Dict[str, Any]] = []
    code_samples: List[Dict[str, Any]] = []
    key_points: Optional[str] = None
    order: int
    difficulty: str
    lesson_type: str
    estimated_time: int
    learning_objectives: str
    is_premium: bool
    course_id: int
    prerequisites: List[int] = []

    @field_validator('content_sections', mode='before')
    @classmethod
    def parse_content_sections(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v

    @field_validator('code_samples', mode='before')
    @classmethod
    def parse_code_samples(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v

    @field_validator('prerequisites', mode='before')
    @classmethod
    def parse_prerequisites(cls, v):
        if v and isinstance(v, list):
            return [prereq.id for prereq in v if hasattr(prereq, 'id')]
        return []

    @field_validator('difficulty', mode='before')
    @classmethod
    def parse_difficulty(cls, v):
        return v.value if hasattr(v, 'value') else v

    @field_validator('lesson_type', mode='before')
    @classmethod
    def parse_lesson_type(cls, v):
        return v.value if hasattr(v, 'value') else v

    model_config = {
        "from_attributes": True
    }

class CourseBase(BaseModel):
    title: str
    description: str
    order: int
    is_premium: bool = False

class CourseCreate(CourseBase):
    pass

class CourseRead(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    lessons: List[LessonRead]

    class Config:
        from_attributes = True

class UserProgressBase(BaseModel):
    lesson_id: int
    is_completed: bool = False

class UserProgressCreate(UserProgressBase):
    pass

class UserProgressRead(UserProgressBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None