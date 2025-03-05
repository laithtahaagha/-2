import os
from dotenv import load_dotenv
from flask import (Flask, render_template, request, redirect, url_for, flash,
                  send_file, jsonify)

load_dotenv()  # تحميل متغيرات البيئة من ملف .env
from flask_login import (LoginManager, login_user, login_required, logout_user,
                       current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from models import User, Student, Document, College, Department, Branch, DocumentTag # Added DocumentTag import
from forms import LoginForm, StudentForm, DocumentForm, SearchForm
from database.setup import init_db, setup_database
from sqlalchemy.exc import SQLAlchemyError # Import SQLAlchemyError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.expanduser('~'), 'ArchiveSystem', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
init_db(app)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('اسم المستخدم أو كلمة المرور غير صحيحة')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    search_form = SearchForm()
    students = Student.query.all()
    return render_template('dashboard.html', students=students, search_form=search_form)

@app.route('/student/new', methods=['GET', 'POST'])
@login_required
def new_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            full_name=form.full_name.data,
            mother_name=form.mother_name.data,
            birth_date=form.birth_date.data,
            gender=form.gender.data,
            birth_place=form.birth_place.data,
            current_address=form.current_address.data,
            phone=form.phone.data,
            bachelor_university=form.bachelor_university.data,
            bachelor_college=form.bachelor_college.data,
            bachelor_department=form.bachelor_department.data,
            bachelor_branch=form.bachelor_branch.data,
            graduation_year=form.graduation_year.data,
            gpa=form.gpa.data,
            first_in_class_gpa=form.first_in_class_gpa.data,
            application_type=form.application_type.data,
            target_university=form.target_university.data,
            target_college=form.target_college.data,
            target_department=form.target_department.data,
            target_branch=form.target_branch.data,
            general_specialty=form.general_specialty.data,
            specific_specialty=form.specific_specialty.data,
            application_channel=form.application_channel.data,
            employment_status=form.employment_status.data,
            employer=form.employer.data
        )
        db.session.add(student)
        db.session.commit()

        # Handle document uploads
        if form.no_objection_letter.data:
            save_document(student.id, form.no_objection_letter.data, 'no_objection_letter')
        if form.documents.data:
            save_document(student.id, form.documents.data, 'documents')

        flash('تم إضافة الطالب بنجاح')
        return redirect(url_for('dashboard'))
    return render_template('student_form.html', form=form)

@app.route('/student/<int:id>')
@login_required
def view_student(id):
    student = Student.query.get_or_404(id)
    return render_template('student_view.html', student=student)

@app.route('/student/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        flash('تم تحديث بيانات الطالب بنجاح')
        return redirect(url_for('view_student', id=student.id))
    return render_template('student_form.html', form=form, student=student)

@app.route('/documents')
@login_required
def documents():
    docs = Document.query.all()
    return render_template('documents.html', documents=docs)

@app.route('/document/upload', methods=['GET', 'POST'])
@login_required
def upload_document():
    form = DocumentForm()
    # Populate tags choices
    form.tags.choices = [(tag.id, tag.name) for tag in DocumentTag.query.all()]

    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Create new document
            document = Document(
                title=form.title.data,
                document_type=form.document_type.data,
                file_path=file_path,
                file_size=os.path.getsize(file_path),
                content_type=file.content_type,
                language=form.language.data
            )

            # Add selected tags
            if form.tags.data:
                selected_tags = DocumentTag.query.filter(DocumentTag.id.in_(form.tags.data)).all()
                document.tags.extend(selected_tags)

            try:
                db.session.add(document)
                db.session.commit()
                flash('تم رفع المستند بنجاح')
                return redirect(url_for('documents'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash('حدث خطأ أثناء حفظ المستند')
                print(f"Error saving document: {e}")

    return render_template('document_form.html', form=form)

@app.route('/search')
@login_required
def search():
    form = SearchForm()
    # Populate tags choices
    form.tags.choices = [(tag.id, tag.name) for tag in DocumentTag.query.all()]

    query = request.args.get('search_term', '')
    search_type = request.args.get('search_type', 'all')
    document_type = request.args.get('document_type', '')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    selected_tags = request.args.getlist('tags')
    include_archived = request.args.get('include_archived', False)

    if not any([query, document_type, date_from, date_to, selected_tags]):
        return render_template('search_results.html', form=form)

    # Build the search query
    search_query = Document.query

    if query:
        if search_type in ['content', 'all']:
            search_query = search_query.filter(
                Document.content_vector.match(query, postgresql_regconfig='arabic')
            )
        if search_type in ['metadata', 'all']:
            search_query = search_query.filter(
                Document.metadata_vector.match(query, postgresql_regconfig='arabic')
            )

    if document_type:
        search_query = search_query.filter(Document.document_type == document_type)

    if date_from:
        search_query = search_query.filter(Document.upload_date >= date_from)
    if date_to:
        search_query = search_query.filter(Document.upload_date <= date_to)

    if selected_tags:
        search_query = search_query.filter(
            Document.tags.any(DocumentTag.id.in_(selected_tags))
        )

    # Execute the search
    documents = search_query.all()

    return render_template('search_results.html',
                         documents=documents,
                         query=query,
                         form=form)

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/export/<int:student_id>')
@login_required
def export_student_data(student_id):
    student = Student.query.get_or_404(student_id)
    # Generate PDF report
    # Implementation needed
    return "Export functionality to be implemented"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_document(student_id, file, doc_type):
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        document = Document(
            student_id=student_id,
            title=filename,
            document_type=doc_type,
            file_path=file_path,
            file_size=os.path.getsize(file_path)
        )
        db.session.add(document)
        db.session.commit()

if __name__ == '__main__':
    # بدلاً من إعادة إنشاء قاعدة البيانات، استخدم setup_database للإعداد الأولي فقط
    with app.app_context():
        # التحقق من وجود مستخدم admin
        from models import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # إنشاء المستخدم الافتراضي إذا لم يكن موجوداً
            from werkzeug.security import generate_password_hash
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin'),
                email='admin@example.com',
                role='admin',
                is_active=True
            )
            from database.setup import db
            db.session.add(admin_user)
            db.session.commit()
            print("تم إنشاء المستخدم الافتراضي: admin/admin")
    
    app.run(host='0.0.0.0', port=8080, debug=True)