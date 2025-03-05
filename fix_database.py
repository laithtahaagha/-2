import os
import sys
from flask import Flask
from werkzeug.security import generate_password_hash
import sqlalchemy

# تعيين متغيرات البيئة قبل استيراد النماذج
os.environ['FLASK_APP'] = 'main.py'
os.environ['FLASK_ENV'] = 'development'

# إنشاء تطبيق Flask جديد
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/archive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# استيراد قاعدة البيانات والنماذج
from database.setup import db, init_db
from models import User, College, Department, Branch, DocumentTag

def fix_database():
    """إصلاح قاعدة البيانات وإعادة تهيئتها إذا لزم الأمر"""
    print("جاري إصلاح وتهيئة قاعدة البيانات...")

    # تهيئة قاعدة البيانات
    init_db(app)

    # التأكد من وجود مجلد instance
    if not os.path.exists('instance'):
        os.makedirs('instance')
        print("تم إنشاء مجلد 'instance'")

    try:
        # إنشاء جميع الجداول
        with app.app_context():
            db.create_all()
            print("تم إنشاء جداول قاعدة البيانات")

            # التحقق من وجود مستخدم admin
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                # إنشاء المستخدم الافتراضي
                admin_user = User(
                    username='admin',
                    password=generate_password_hash('admin'),
                    email='admin@example.com',
                    role='admin',
                    is_active=True
                )
                db.session.add(admin_user)
                db.session.commit()
                print("تم إنشاء المستخدم الافتراضي: admin/admin")
            else:
                print("المستخدم 'admin' موجود بالفعل")

            # إضافة بعض البيانات الأساسية
            # الكليات
            if College.query.count() == 0:
                colleges = [
                    {"name": "كلية الهندسة", "name_en": "Engineering"},
                    {"name": "كلية العلوم", "name_en": "Science"},
                    {"name": "كلية الطب", "name_en": "Medicine"}
                ]
                for c in colleges:
                    db.session.add(College(**c))
                print("تم إضافة بيانات الكليات")

            # الأقسام
            if Department.query.count() == 0:
                engineering = College.query.filter_by(name="كلية الهندسة").first()
                science = College.query.filter_by(name="كلية العلوم").first()
                medicine = College.query.filter_by(name="كلية الطب").first()

                if engineering:
                    departments = [
                        {"college_id": engineering.id, "name": "هندسة الحاسوب", "name_en": "Computer Engineering"},
                        {"college_id": engineering.id, "name": "الهندسة الميكانيكية", "name_en": "Mechanical Engineering"},
                        {"college_id": engineering.id, "name": "الهندسة المدنية", "name_en": "Civil Engineering"}
                    ]
                    for d in departments:
                        db.session.add(Department(**d))

                if science:
                    departments = [
                        {"college_id": science.id, "name": "علوم الحاسوب", "name_en": "Computer Science"},
                        {"college_id": science.id, "name": "الرياضيات", "name_en": "Mathematics"},
                        {"college_id": science.id, "name": "الفيزياء", "name_en": "Physics"}
                    ]
                    for d in departments:
                        db.session.add(Department(**d))

                print("تم إضافة بيانات الأقسام")

            # وسوم المستندات
            if DocumentTag.query.count() == 0:
                tags = [
                    {"name": "شهادة", "description": "شهادات جامعية وغيرها"},
                    {"name": "كشف درجات", "description": "كشوف درجات للطلاب"},
                    {"name": "خطاب", "description": "خطابات رسمية"},
                    {"name": "تقرير", "description": "تقارير وأبحاث"},
                    {"name": "طلب", "description": "طلبات مقدمة"}
                ]
                for t in tags:
                    db.session.add(DocumentTag(**t))
                print("تم إضافة وسوم المستندات")

            db.session.commit()
            print("تم حفظ البيانات بنجاح")

        return True
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"خطأ في قاعدة البيانات: {e}")
        return False
    except Exception as e:
        print(f"خطأ غير متوقع: {e}")
        return False

if __name__ == "__main__":
    success = fix_database()
    if success:
        print("\n✅ تم إصلاح وتهيئة قاعدة البيانات بنجاح")
        print("✅ يمكنك الآن تشغيل التطبيق")
    else:
        print("\n❌ فشل إصلاح قاعدة البيانات")
        print("❌ الرجاء مراجعة الأخطاء")

    input("\nاضغط Enter للخروج...")