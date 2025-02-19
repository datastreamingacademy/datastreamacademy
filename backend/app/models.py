# backend/app/models.py
from sqlalchemy import (
    Boolean, Column, Integer, String, Text, ForeignKey, 
    Enum, JSON, DateTime, Table, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum
from passlib.hash import bcrypt

Base = declarative_base()

class CourseCategory(str, enum.Enum):
    SPARK = "spark"
    API = "api"
    PYTHON = "python"
    DATA_SCIENCE = "data_science"
    WEB_DEVELOPMENT = "web_development"

class ContentFormat(str, enum.Enum):
    CODE = "code"
    TEXT = "text"
    VIDEO = "video"
    EXERCISE = "exercise"
    QUIZ = "quiz"
    API_PLAYGROUND = "api_playground"
    INTERACTIVE_DEMO = "interactive_demo"

class DifficultyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class LessonType(str, enum.Enum):
    THEORY = "theory"
    HANDS_ON = "hands_on"
    PROJECT = "project"
    CASE_STUDY = "case_study"

# Association table for lesson prerequisites
lesson_prerequisites = Table(
    'lesson_prerequisites', Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id'), primary_key=True),
    Column('prerequisite_id', Integer, ForeignKey('lessons.id'), primary_key=True)
)

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    order = Column(Integer)
    is_premium = Column(Boolean, default=False)
    category = Column(Enum(CourseCategory), nullable=False, default=CourseCategory.SPARK)
    tags = Column(JSON)
    prerequisites = Column(JSON)
    target_audience = Column(String)
    learning_outcomes = Column(JSON)
    supported_content_formats = Column(JSON)
    course_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    lessons = relationship("Lesson", back_populates="course")

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    summary = Column(String)
    content = Column(Text)
    content_sections = Column(JSON)
    code_samples = Column(JSON)
    key_points = Column(Text)
    order = Column(Integer)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.BEGINNER)
    lesson_type = Column(Enum(LessonType), default=LessonType.THEORY)
    content_format = Column(Enum(ContentFormat), default=ContentFormat.TEXT)
    estimated_time = Column(Integer)  # in minutes
    skill_level_required = Column(String)
    learning_objectives = Column(Text)
    interactive_elements = Column(JSON)
    external_resources = Column(JSON)
    practical_application = Column(Text)
    is_premium = Column(Boolean, default=False)
    course_id = Column(Integer, ForeignKey("courses.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    course = relationship("Course", back_populates="lessons")
    resources = relationship("Resource", back_populates="lesson")
    prerequisites = relationship(
        "Lesson",
        secondary=lesson_prerequisites,
        primaryjoin=id==lesson_prerequisites.c.lesson_id,
        secondaryjoin=id==lesson_prerequisites.c.prerequisite_id,
        backref="required_for"
    )

class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String)
    content = Column(Text)
    description = Column(String)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    lesson = relationship("Lesson", back_populates="resources")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # New fields for Google OAuth
    google_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    email_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    
    # Make password optional for OAuth users
    hashed_password = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with UserProgress
    progress = relationship("UserProgress", back_populates="user")
    
    def set_password(self, password):
        """Hash and set the password"""
        self.hashed_password = bcrypt.hash(password)
    
    def check_password(self, password):
        """Verify a password against the stored hash"""
        return bcrypt.verify(password, self.hashed_password)

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson")
    
    def mark_completed(self):
        """Mark the lesson as completed"""
        self.is_completed = True
        self.completed_at = datetime.utcnow()