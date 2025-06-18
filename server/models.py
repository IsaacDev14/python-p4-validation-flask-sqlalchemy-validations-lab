from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # ✅ VALIDATION: Name must exist and be unique
    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Author must have a name.")
        
        # Manual check for uniqueness (for test compatibility)
        existing_author = Author.query.filter_by(name=value.strip()).first()
        if existing_author:
            raise ValueError("Author name must be unique.")
        
        return value.strip()

    # ✅ VALIDATION: Phone number must be exactly 10 digits
    @validates('phone_number')
    def validate_phone(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # ✅ VALIDATION: Title must contain clickbait words
    @validates('title')
    def validate_title(self, key, value):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in value for keyword in clickbait_keywords):
            raise ValueError("Title must contain clickbait keywords.")
        return value

    # ✅ VALIDATION: Content must be at least 250 characters
    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return value

    # ✅ VALIDATION: Summary must be at most 250 characters
    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError("Summary must be no more than 250 characters.")
        return value

    # ✅ VALIDATION: Category must be either 'Fiction' or 'Non-Fiction'
    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
