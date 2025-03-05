from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from database.setup import db
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)  # Increased length for password hash
    role = db.Column(db.String(20), nullable=True, default='user')
    is_active = db.Column(db.Boolean, default=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    mother_name = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_place = db.Column(db.String(200))
    current_address = db.Column(db.String(500))
    phone = db.Column(db.String(20))

    bachelor_university = db.Column(db.String(200))
    bachelor_college = db.Column(db.String(200))
    bachelor_department = db.Column(db.String(200))
    bachelor_branch = db.Column(db.String(200))
    graduation_year = db.Column(db.Integer)
    gpa = db.Column(db.Float)
    first_in_class_gpa = db.Column(db.Float)

    application_type = db.Column(db.String(20))
    target_university = db.Column(db.String(200))
    target_college = db.Column(db.String(200))
    target_department = db.Column(db.String(200))
    target_branch = db.Column(db.String(200))
    general_specialty = db.Column(db.String(200))
    specific_specialty = db.Column(db.String(200))
    application_channel = db.Column(db.String(100))
    employment_status = db.Column(db.String(50))
    employer = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_size = db.Column(db.Integer)  # in bytes
    content_type = db.Column(db.String(100))  # MIME type
    language = db.Column(db.String(10))  # ar, en, etc.

    content_vector = db.Column(TSVECTOR)
    metadata_vector = db.Column(TSVECTOR)

    student = db.relationship('Student', backref=db.backref('documents', lazy=True))
    tags = db.relationship('DocumentTag', secondary='document_tags', backref='documents')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_search_vectors()

    def update_search_vectors(self):
        metadata = f"{self.title} {self.document_type} {self.student.full_name if self.student else ''}"
        self.metadata_vector = func.to_tsvector('arabic', metadata)

class DocumentTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))

document_tags = db.Table('document_tags',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('document_tag.id'), primary_key=True)
)

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200))
    departments = db.relationship('Department', backref='college', lazy=True)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200))
    branches = db.relationship('Branch', backref='department', lazy=True)

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200))