#!/usr/bin/env python3
"""
Database seeding script
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.data.src.db_models.LessonDB import LessonDB, Base

def seed_database():
    """Seed the database with sample data"""
    
    # Get database URL from environment
    db_url = os.getenv('DB_URL', 'mysql+pymysql://root:password@db:3306/tarifiyt')
    
    # Create engine and session
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if lessons already exist
        existing_lessons = session.query(LessonDB).count()
        if existing_lessons > 0:
            print(f"Database already has {existing_lessons} lessons. Skipping seeding.")
            return

        
        # Sample lesson data
        sample_lessons = [
            {
                'id': str(uuid4()),
                'title': 'Introduction to Tamazight',
                'description': 'Learn the basics of the Tamazight language and its history.'
            },
            {
                'id': str(uuid4()),
                'title': 'Basic Vocabulary',
                'description': 'Essential words and phrases for everyday conversation in Tamazight.'
            },
            {
                'id': str(uuid4()),
                'title': 'Grammar Fundamentals',
                'description': 'Understanding the grammatical structure of Tamazight.'
            },
            {
                'id': str(uuid4()),
                'title': 'Numbers and Counting',
                'description': 'Learn how to count and use numbers in Tamazight.'
            },
            {
                'id': str(uuid4()),
                'title': 'Family and Relationships',
                'description': 'Vocabulary related to family members and relationships.'
            }
        ]
        
        # Insert sample lessons
        for lesson_data in sample_lessons:
            lesson = LessonDB(**lesson_data)
            session.add(lesson)
        
        # Commit the changes
        session.commit()
        print(f"Successfully seeded database with {len(sample_lessons)} lessons.")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
