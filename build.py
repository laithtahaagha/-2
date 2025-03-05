
import os
import shutil
import subprocess
import sys

def create_installer():
    print("بدء عملية إنشاء ملف التنصيب...")
    
    # تأكد من تثبيت المكتبات المطلوبة
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # إنشاء مجلد للبناء إذا لم يكن موجوداً
    os.makedirs("build", exist_ok=True)
    os.makedirs("dist", exist_ok=True)
    
    # إنشاء ملف تكوين PyInstaller
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('config.py', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_login',
        'flask_sqlalchemy',
        'flask_wtf',
        'werkzeug',
        'sqlalchemy',
        'wtforms',
        'jinja2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='نظام الأرشفة للدراسات العليا',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='generated-icon.png',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='نظام الأرشفة للدراسات العليا',
)
"""
    
    with open("archive_system.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    # إنشاء ملف تنصيبي باستخدام PyInstaller
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "PyInstaller", 
        "archive_system.spec", 
        "--noconfirm"
    ])
    
    print("تم إنشاء ملف التنصيب بنجاح!")
    print(f"يمكنك العثور على الملف التنفيذي في المجلد: {os.path.abspath('dist/نظام الأرشفة للدراسات العليا')}")

    # إنشاء ملف README بالتعليمات
    readme_content = """
# نظام الأرشفة للدراسات العليا

## تعليمات التثبيت والتشغيل

1. قم بنسخ مجلد "نظام الأرشفة للدراسات العليا" إلى المكان المطلوب على جهازك.
2. قم بتشغيل الملف التنفيذي "نظام الأرشفة للدراسات العليا.exe" الموجود داخل المجلد.
3. سيتم تشغيل البرنامج وفتح نافذة المتصفح تلقائيًا.
4. استخدم اسم المستخدم وكلمة المرور الافتراضية للدخول:
   - اسم المستخدم: admin
   - كلمة المرور: admin

## معلومات إضافية

- يقوم البرنامج بتخزين البيانات محليًا على جهازك.
- إذا كنت ترغب في إعادة تعيين قاعدة البيانات، قم بحذف الملف "data.db" من مجلد البرنامج وإعادة تشغيل البرنامج.

للدعم الفني أو الاستفسارات: example@example.com
"""
    
    with open("dist/نظام الأرشفة للدراسات العليا/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("تم إنشاء ملف التعليمات بنجاح!")

if __name__ == "__main__":
    create_installer()
