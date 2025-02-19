# backend/app/seed.py
from datetime import datetime
import json
from app.database import SessionLocal, engine
from app.models import Base, Course, Lesson, Resource, DifficultyLevel, LessonType

def seed_data():
    db = SessionLocal()
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(Resource).delete()
        db.query(Lesson).delete()
        db.query(Course).delete()
        
        # Create courses
        print("Creating courses...")
        fundamentals = Course(
            title="Fundamentals of Apache Spark",
            description="Master the core concepts of Apache Spark and its ecosystem",
            order=1,
            is_premium=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        pyspark = Course(
            title="PySpark Programming",
            description="Learn to write efficient Spark applications using Python",
            order=2,
            is_premium=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        advanced = Course(
            title="Advanced Spark Programming",
            description="Deep dive into advanced Spark concepts and optimizations",
            order=3,
            is_premium=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add_all([fundamentals, pyspark, advanced])
        db.commit()
        
        # Create lessons for Fundamentals course
        print("Creating lessons...")
        
        # Helper function to create content sections
        def create_content_sections(title, description, main_content):
            return json.dumps([
                {
                    "title": "Introduction",
                    "content": description,
                    "order": 1,
                    "type": "text"
                },
                {
                    "title": "Main Content",
                    "content": main_content,
                    "order": 2,
                    "type": "text"
                }
            ])

        # Helper function to create code samples
        def create_code_samples(samples):
            return json.dumps(samples)

        fundamental_lessons = [
            Lesson(
                title="Introduction to Big Data and Apache Spark",
                description="Understand the basics of big data and where Spark fits in",
                summary="An overview of big data challenges and Apache Spark's role in solving them",
                content="Apache Spark is a unified analytics engine for large-scale data processing...",
                content_sections=create_content_sections(
                    "Introduction to Big Data",
                    "Understanding big data challenges and Apache Spark's role",
                    "Detailed explanation of Apache Spark architecture and components..."
                ),
                code_samples=create_code_samples([
                    {
                        "title": "First Spark Application",
                        "language": "python",
                        "code": "from pyspark.sql import SparkSession\n\nspark = SparkSession.builder.getOrCreate()",
                        "description": "Basic SparkSession initialization"
                    }
                ]),
                key_points="1. Understanding big data challenges\n2. Spark's role in data processing\n3. Basic Spark architecture",
                order=1,
                difficulty=DifficultyLevel.BEGINNER,
                lesson_type=LessonType.THEORY,
                estimated_time=45,
                skill_level_required="None",
                learning_objectives="Understand big data challenges and Spark's role in solving them",
                is_premium=False,
                course_id=fundamentals.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Lesson(
                title="Spark Architecture Overview",
                description="Learn about Spark's distributed architecture",
                summary="Deep dive into Spark's architectural components and distributed computing model",
                content="Explore Spark's architectural components...",
                content_sections=create_content_sections(
                    "Spark Architecture",
                    "Understanding Spark's distributed computing model",
                    "Detailed explanation of master-worker architecture..."
                ),
                code_samples=create_code_samples([
                    {
                        "title": "Examining Spark Configuration",
                        "language": "python",
                        "code": "spark.sparkContext.getConf().getAll()",
                        "description": "Viewing Spark configuration"
                    }
                ]),
                key_points="1. Master-worker architecture\n2. RDD fundamentals\n3. Execution model",
                order=2,
                difficulty=DifficultyLevel.BEGINNER,
                lesson_type=LessonType.THEORY,
                estimated_time=60,
                skill_level_required="Basic Python",
                learning_objectives="Understand Spark's distributed computing model",
                is_premium=False,
                course_id=fundamentals.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        # Create lessons for PySpark course
        pyspark_lessons = [
            Lesson(
                title="Getting Started with PySpark",
                description="Set up your PySpark development environment",
                summary="Complete guide to setting up and configuring PySpark",
                content="Step-by-step guide to setting up PySpark...",
                content_sections=create_content_sections(
                    "PySpark Setup",
                    "Setting up your development environment",
                    "Detailed installation and configuration steps..."
                ),
                code_samples=create_code_samples([
                    {
                        "title": "Environment Setup",
                        "language": "bash",
                        "code": "pip install pyspark\nexport SPARK_HOME=/path/to/spark",
                        "description": "Basic setup commands"
                    }
                ]),
                key_points="1. Installation steps\n2. Environment configuration\n3. Verification",
                order=1,
                difficulty=DifficultyLevel.BEGINNER,
                lesson_type=LessonType.HANDS_ON,
                estimated_time=90,
                skill_level_required="Basic Python",
                learning_objectives="Install and configure PySpark locally",
                is_premium=False,
                course_id=pyspark.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Lesson(
                title="Working with DataFrames",
                description="Learn to manipulate data using PySpark DataFrames",
                summary="Comprehensive guide to DataFrame operations in PySpark",
                content="Master DataFrame operations in PySpark...",
                content_sections=create_content_sections(
                    "DataFrame Operations",
                    "Working with PySpark DataFrames",
                    "Detailed guide to DataFrame transformations and actions..."
                ),
                code_samples=create_code_samples([
                    {
                        "title": "Creating DataFrames",
                        "language": "python",
                        "code": "df = spark.createDataFrame(data)",
                        "description": "Creating DataFrames from data"
                    }
                ]),
                key_points="1. DataFrame creation\n2. Transformations\n3. Actions",
                order=2,
                difficulty=DifficultyLevel.INTERMEDIATE,
                lesson_type=LessonType.HANDS_ON,
                estimated_time=120,
                skill_level_required="Basic Python, PySpark Setup",
                learning_objectives="Master DataFrame operations in PySpark",
                is_premium=False,
                course_id=pyspark.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        # Create lessons for Advanced course
        advanced_lessons = [
            Lesson(
                title="Spark Performance Tuning",
                description="Learn advanced optimization techniques",
                summary="Comprehensive guide to optimizing Spark applications",
                content="Deep dive into Spark performance optimization...",
                content_sections=create_content_sections(
                    "Performance Tuning",
                    "Advanced optimization techniques",
                    "Detailed performance tuning strategies..."
                ),
                code_samples=create_code_samples([
                    {
                        "title": "Memory Configuration",
                        "language": "python",
                        "code": "spark.conf.set('spark.executor.memory', '4g')",
                        "description": "Setting executor memory"
                    }
                ]),
                key_points="1. Memory management\n2. Job optimization\n3. Resource allocation",
                order=1,
                difficulty=DifficultyLevel.ADVANCED,
                lesson_type=LessonType.HANDS_ON,
                estimated_time=150,
                skill_level_required="Intermediate Python, Basic Spark",
                learning_objectives="Master Spark performance optimization techniques",
                is_premium=True,
                course_id=advanced.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        all_lessons = fundamental_lessons + pyspark_lessons + advanced_lessons
        db.add_all(all_lessons)
        db.commit()
        
        # Add resources for lessons
        print("Creating resources...")
        resources = [
            Resource(
                title="Introduction Slides",
                type="presentation",
                content="path/to/slides.pdf",
                description="Comprehensive slides for the introduction",
                lesson_id=fundamental_lessons[0].id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Resource(
                title="PySpark Installation Guide",
                type="guide",
                content="Detailed steps for installation...",
                description="Step-by-step installation guide",
                lesson_id=pyspark_lessons[0].id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Resource(
                title="Performance Tuning Notebook",
                type="notebook",
                content="path/to/notebook.ipynb",
                description="Interactive notebook for performance tuning",
                lesson_id=advanced_lessons[0].id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        db.add_all(resources)
        db.commit()
        
        # Set up prerequisites
        print("Setting up prerequisites...")
        # Fundamentals course prerequisites
        fundamental_lessons[1].prerequisites.append(fundamental_lessons[0])
        
        # PySpark course prerequisites
        pyspark_lessons[0].prerequisites.append(fundamental_lessons[1])
        pyspark_lessons[1].prerequisites.append(pyspark_lessons[0])
        
        # Advanced course prerequisites
        advanced_lessons[0].prerequisites.extend([
            fundamental_lessons[1],
            pyspark_lessons[1]
        ])
        
        db.commit()
        print("Sample data added successfully!")
        
    except Exception as e:
        print(f"Error seeding data: {str(e)}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Seeding data...")
    seed_data()
    print("Done!")