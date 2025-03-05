
import os
import sys
import subprocess
import shutil
from pathlib import Path
import time

def create_executable():
    print("جاري إنشاء الملف التنفيذي...")
    
    # التأكد من وجود PyInstaller
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("تم تثبيت PyInstaller بنجاح!")
    except:
        print("فشل تثبيت PyInstaller. يرجى تثبيته يدويًا.")
        return False
    
    # إنشاء الملف التنفيذي
    try:
        subprocess.run([
            sys.executable, 
            "-m", 
            "PyInstaller",
            "--name=نظام_الأرشفة",
            "--add-data=templates:templates",
            "--add-data=static:static",
            "--add-data=database:database",
            "--onefile",
            "main.py"
        ], check=True)
        print("تم إنشاء الملف التنفيذي بنجاح!")
        return True
    except:
        print("فشل إنشاء الملف التنفيذي.")
        return False

if __name__ == "__main__":
    print("بدء عملية إنشاء ملف التنصيب...")
    if create_executable():
        print("تم إنشاء ملف التنصيب بنجاح!")
        print(f"يمكنك العثور على الملف التنفيذي في المجلد: {os.path.abspath('dist')}")
        
        # إنشاء ملف README للتعليمات
        readme_path = os.path.join("dist", "تعليمات_التثبيت.txt")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("""
# نظام الأرشفة للدراسات العليا

## تعليمات التثبيت والتشغيل:

1. قم بنسخ ملف "نظام_الأرشفة.exe" إلى المجلد المطلوب على جهازك.
2. قم بتشغيل الملف بالنقر المزدوج عليه.
3. سوف يفتح المتصفح تلقائيًا ويعرض واجهة النظام.
4. استخدم بيانات تسجيل الدخول الافتراضية:
   - اسم المستخدم: admin
   - كلمة المرور: admin

للدعم الفني، يرجى التواصل عبر: support@example.com
""")
            
        print(f"تم إنشاء ملف التعليمات في: {os.path.abspath(readme_path)}")
    else:
        print("فشل إنشاء ملف التنصيب!")
    
    # انتظار لقراءة الرسالة
    print("\nاضغط Enter للخروج...")
    input()
