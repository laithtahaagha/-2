from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SelectField, DateField, 
                    FloatField, FileField, SubmitField, SelectMultipleField,
                    BooleanField)
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    submit = SubmitField('تسجيل الدخول')

class StudentForm(FlaskForm):
    # Personal Information
    full_name = StringField('الاسم الرباعي واللقب', validators=[DataRequired()])
    mother_name = StringField('اسم الأم الثلاثي', validators=[DataRequired()])
    birth_date = DateField('تاريخ الميلاد', validators=[DataRequired()])
    gender = SelectField('الجنس', choices=[('male', 'ذكر'), ('female', 'أنثى')])
    birth_place = StringField('محل الولادة')
    current_address = StringField('السكن الحالي')
    phone = StringField('رقم الهاتف')
    
    # Bachelor's Information
    bachelor_university = StringField('الجامعة')
    bachelor_college = StringField('الكلية')
    bachelor_department = StringField('القسم')
    bachelor_branch = StringField('الفرع')
    graduation_year = StringField('سنة التخرج')
    gpa = FloatField('المعدل')
    first_in_class_gpa = FloatField('معدل الطالب الأول')
    
    # Graduate Studies Application
    application_type = SelectField('نوع التقديم', 
                                 choices=[('masters', 'ماجستير'), 
                                        ('phd', 'دكتوراه')])
    target_university = StringField('الجامعة المستهدفة')
    target_college = StringField('الكلية المستهدفة')
    target_department = StringField('القسم المستهدف')
    target_branch = StringField('الفرع المستهدف')
    general_specialty = StringField('الاختصاص العام')
    specific_specialty = StringField('الاختصاص الدقيق')
    application_channel = SelectField('قناة التقديم',
                                    choices=[('general', 'القناة العامة'),
                                           ('private', 'النفقة الخاصة'),
                                           ('martyrs', 'قناة الشهداء')])
    employment_status = SelectField('حالة التوظيف',
                                  choices=[('employed', 'موظف'),
                                         ('unemployed', 'غير موظف')])
    employer = StringField('جهة العمل')
    
    # Documents
    no_objection_letter = FileField('كتاب عدم الممانعة')
    documents = FileField('المستمسكات والوثائق')
    
    submit = SubmitField('حفظ')

class DocumentForm(FlaskForm):
    title = StringField('عنوان المستند', validators=[DataRequired()])
    document_type = SelectField('نوع المستند',
                              choices=[('certificate', 'شهادة'),
                                     ('transcript', 'كشف درجات'),
                                     ('id', 'هوية'),
                                     ('other', 'أخرى')])
    file = FileField('الملف', validators=[DataRequired()])
    language = SelectField('لغة المستند',
                         choices=[('ar', 'العربية'),
                                ('en', 'الإنجليزية'),
                                ('other', 'أخرى')])
    tags = SelectMultipleField('الوسوم', coerce=int)
    submit = SubmitField('رفع المستند')

class SearchForm(FlaskForm):
    search_term = StringField('البحث')
    search_type = SelectField('نوع البحث',
                            choices=[
                                ('content', 'محتوى المستند'),
                                ('metadata', 'البيانات الوصفية'),
                                ('tags', 'الوسوم'),
                                ('all', 'بحث شامل')
                            ])
    document_type = SelectField('نوع المستند',
                              choices=[
                                  ('', 'الكل'),
                                  ('certificate', 'شهادة'),
                                  ('transcript', 'كشف درجات'),
                                  ('id', 'هوية'),
                                  ('other', 'أخرى')
                              ])
    date_from = DateField('من تاريخ', validators=[Optional()])
    date_to = DateField('إلى تاريخ', validators=[Optional()])
    tags = SelectMultipleField('الوسوم', coerce=int)
    include_archived = BooleanField('البحث في المؤرشف')

    submit = SubmitField('بحث')