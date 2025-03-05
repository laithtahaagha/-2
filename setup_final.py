
import os
import sys
import subprocess
from pathlib import Path
import shutil
import time
import signal

def kill_process_on_port(port):
    """إيقاف العمليات التي تستخدم المنفذ المحدد"""
    try:
        # الحصول على معرف العملية التي تستخدم المنفذ
        if os.name == 'posix':  # نظام Linux/Mac
            cmd = f"lsof -i :{port} -t"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            pid = process.stdout.read().decode().strip()
            if pid:
                print(f"🔄 إيقاف العملية {pid} التي تستخدم المنفذ {port}...")
                os.kill(int(pid), signal.SIGTERM)
                time.sleep(1)  # انتظار لإغلاق العملية
                return True
        else:  # نظام Windows
            cmd = f"netstat -ano | findstr :{port}"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = process.stdout.read().decode()
            if output:
                # استخراج معرف العملية من الخرج
                pid = output.strip().split()[-1]
                print(f"🔄 إيقاف العملية {pid} التي تستخدم المنفذ {port}...")
                os.kill(int(pid), signal.SIGTERM)
                time.sleep(1)  # انتظار لإغلاق العملية
                return True
    except Exception as e:
        print(f"⚠️ تحذير: فشل إيقاف العملية على المنفذ {port}: {e}")
    return False

def create_documents():
    """إنشاء ملفات الدليل والتعليمات"""
    print("📄 جاري إنشاء ملفات التوثيق...")
    
    # إنشاء ملف دليل المستخدم
    user_guide_path = os.path.join("dist", "دليل_نظام_الأرشفة.txt")
    with open(user_guide_path, "w", encoding="utf-8") as f:
        f.write("""
# دليل استخدام نظام الأرشفة للدراسات العليا

## مقدمة
هذا النظام مصمم لتسهيل عملية أرشفة وإدارة وثائق طلاب الدراسات العليا.

## الميزات الرئيسية
1. إضافة وإدارة بيانات الطلاب
2. أرشفة وتصنيف الوثائق
3. البحث المتقدم في قاعدة البيانات
4. إنشاء تقارير وإحصائيات

## طريقة الاستخدام
1. قم بتسجيل الدخول باستخدام بيانات الاعتماد المقدمة
2. من لوحة التحكم، يمكنك الوصول إلى جميع وظائف النظام
3. لإضافة طالب جديد، انقر على "إضافة طالب" وأدخل البيانات المطلوبة
4. لإضافة وثيقة، انقر على "إضافة وثيقة" واختر الطالب المرتبط بها
5. للبحث، استخدم شريط البحث في الأعلى

## المساعدة والدعم
للحصول على مساعدة إضافية، يرجى التواصل مع مسؤول النظام.
""")
        print(f"✅ تم إنشاء دليل المستخدم في: {os.path.abspath(user_guide_path)}")
    
    # إنشاء ملف تعليمات التثبيت
    install_guide_path = os.path.join("dist", "تعليمات_الاستخدام.txt")
    with open(install_guide_path, "w", encoding="utf-8") as f:
        f.write("""
# تعليمات تثبيت واستخدام نظام الأرشفة للدراسات العليا

## متطلبات النظام
- نظام تشغيل: Windows 10 أو أحدث / Linux / macOS
- ذاكرة عشوائية: 4 جيجابايت كحد أدنى
- مساحة القرص: 500 ميجابايت كحد أدنى

## خطوات التثبيت
1. قم بفك ضغط حزمة البرنامج إلى المجلد المطلوب
2. قم بتشغيل ملف "نظام_الأرشفة_النهائي.exe"
3. سيتم فتح المتصفح تلقائيًا وعرض واجهة الويب الخاصة بالنظام

## بدء الاستخدام
1. استخدم بيانات تسجيل الدخول الافتراضية:
   - اسم المستخدم: admin
   - كلمة المرور: admin
2. قم بتغيير كلمة المرور الافتراضية من صفحة الإعدادات
3. ابدأ باستخدام النظام!

## ملاحظات هامة
- يتم حفظ قاعدة البيانات تلقائيًا في مجلد التطبيق
- قم بعمل نسخة احتياطية من قاعدة البيانات بشكل دوري
- في حالة نسيان كلمة المرور، يمكن إعادة تعيينها عن طريق حذف ملف قاعدة البيانات وإعادة تشغيل البرنامج
""")
        print(f"✅ تم إنشاء تعليمات الاستخدام في: {os.path.abspath(install_guide_path)}")

def create_final_package():
    """تجميع الملفات في حزمة واحدة"""
    print("📦 جاري إنشاء الحزمة النهائية...")
    
    # إنشاء مجلد الحزمة النهائية
    final_dir = os.path.join("dist", "نظام_الأرشفة_النهائي")
    os.makedirs(final_dir, exist_ok=True)
    
    # نسخ الملفات الضرورية
    try:
        # نسخ ملفات التوثيق
        shutil.copy2(os.path.join("dist", "تعليمات_الاستخدام.txt"), final_dir)
        shutil.copy2(os.path.join("dist", "دليل_نظام_الأرشفة.txt"), final_dir)
        
        # نسخ الملفات الضرورية للتشغيل
        print("🔄 جاري نسخ ملفات النظام...")
        shutil.copy2("main.py", final_dir)
        
        # إنشاء مجلدات النظام
        os.makedirs(os.path.join(final_dir, "templates"), exist_ok=True)
        os.makedirs(os.path.join(final_dir, "static"), exist_ok=True)
        os.makedirs(os.path.join(final_dir, "database"), exist_ok=True)
        
        # نسخ محتويات المجلدات
        for item in os.listdir("templates"):
            src = os.path.join("templates", item)
            dst = os.path.join(final_dir, "templates", item)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
        
        for item in os.listdir("static"):
            src = os.path.join("static", item)
            dst = os.path.join(final_dir, "static", item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif os.path.isfile(src):
                shutil.copy2(src, dst)
        
        for item in os.listdir("database"):
            src = os.path.join("database", item)
            dst = os.path.join(final_dir, "database", item)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
        
        # نسخ ملفات النظام الأخرى
        for file in ["models.py", "forms.py", "fix_database.py", "config.py"]:
            if os.path.exists(file):
                shutil.copy2(file, final_dir)
        
        # إنشاء ملف تشغيل للنظام
        starter_script = os.path.join(final_dir, "تشغيل_نظام_الأرشفة.bat")
        with open(starter_script, "w", encoding="utf-8") as f:
            f.write("""@echo off
echo تشغيل نظام الأرشفة للدراسات العليا...
python main.py
pause
""")
        
        print(f"✅ تم إنشاء حزمة النظام بنجاح في: {os.path.abspath(final_dir)}")
        return True
    except Exception as e:
        print(f"❌ فشل إنشاء الحزمة النهائية: {e}")
        return False

if __name__ == "__main__":
    print("==== بدء عملية إنشاء ملف التنصيب ====")

    # إيقاف أي عمليات تستخدم المنفذ 8080
    kill_process_on_port(8080)

    try:
        # إنشاء ملفات التوثيق
        create_documents()
        
        # إنشاء الحزمة النهائية
        create_final_package()
        
        print("\n✅✅✅ تم اكتمال العمل بنجاح! ✅✅✅")
        print(f"يمكنك العثور على ملف النظام في: {os.path.abspath(os.path.join('dist', 'نظام_الأرشفة_النهائي'))}")
        print("\nيمكنك الآن تشغيل النظام من خلال واجهة الويب على العنوان:")
        print("http://127.0.0.1:8080\n")
        print("بيانات تسجيل الدخول:")
        print("اسم المستخدم: admin")
        print("كلمة المرور: admin")
    except Exception as e:
        print(f"\n❌ حدث خطأ غير متوقع: {e}")

    print("\nاضغط Enter للخروج...")
    input()
