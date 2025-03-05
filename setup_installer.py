import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_installer():
    print("بدء إنشاء ملف التنصيب...")

    # التأكد من وجود مجلد البناء
    build_dir = Path("build")
    dist_dir = Path("dist")
    if not build_dir.exists():
        build_dir.mkdir()
    if not dist_dir.exists():
        dist_dir.mkdir()

    # بناء التطبيق باستخدام PyInstaller
    try:
        print("جاري بناء التطبيق...")
        subprocess.run([
            "pyinstaller",
            "--name=نظام الأرشفة للدراسات العليا",
            "--icon=generated-icon.png",
            "--add-data=templates:templates",
            "--add-data=static:static",
            "--hidden-import=sqlalchemy.sql.default_comparator",
            "--hidden-import=werkzeug.middleware.proxy_fix",
            "--noconfirm",
            "--windowed",
            "main.py"
        ], check=True)
        print("تم بناء التطبيق بنجاح!")
    except subprocess.CalledProcessError as e:
        print(f"حدث خطأ أثناء بناء التطبيق: {e}")
        return False
    except FileNotFoundError:
        print("خطأ: تأكد من تثبيت PyInstaller. يمكنك تثبيته باستخدام 'pip install pyinstaller'")
        return False

    # إنشاء ملف التنصيب باستخدام Inno Setup
    try:
        print("جاري إنشاء ملف التنصيب...")
        iss_file = Path("inno_setup.iss")
        if not iss_file.exists():
            print("خطأ: ملف inno_setup.iss غير موجود")
            return False

        # استخدام البرنامج المساعد innosetup.exe
        inno_exe = Path("innosetup.exe")
        if inno_exe.exists():
            print("جاري استخدام innosetup.exe المحلي...")
            subprocess.run([str(inno_exe), str(iss_file)], check=True)
        else:
            # محاولة استخدام ISCC من Inno Setup
            print("ملف innosetup.exe غير موجود، محاولة استخدام ISCC...")
            try:
                subprocess.run(["iscc", str(iss_file)], check=True)
            except FileNotFoundError:
                print("تحذير: Inno Setup غير مثبت. لن يتم إنشاء ملف التنصيب.")
                print("يمكنك استخدام الملف التنفيذي المنشأ في مجلد dist مباشرة.")
                # إنشاء ملف README بتعليمات التثبيت اليدوي
                with open("dist/README_INSTALL.txt", "w", encoding="utf-8") as f:
                    f.write("لتثبيت البرنامج:\n")
                    f.write("1. انسخ مجلد 'نظام الأرشفة للدراسات العليا' إلى المكان المرغوب\n")
                    f.write("2. قم بتشغيل الملف التنفيذي 'نظام الأرشفة للدراسات العليا.exe'\n")
                return True

        print("تم إنشاء ملف التنصيب بنجاح!")

        # اسم ملف التنصيب النهائي
        setup_file = next(Path("Output").glob("*.exe"), None)
        if setup_file:
            print(f"ملف التنصيب: {setup_file}")
        else:
            print("تم إنشاء ملف التنصيب ولكن لم يتم العثور عليه في مجلد Output")

        return True
    except subprocess.CalledProcessError as e:
        print(f"حدث خطأ أثناء إنشاء ملف التنصيب: {e}")
        return False
    except FileNotFoundError:
        print("خطأ: تأكد من تثبيت Inno Setup وأنه متاح في مسار النظام أو وجود innosetup.exe")
        return False

if __name__ == "__main__":
    success = create_installer()
    if success:
        print("تم إنشاء ملف التنصيب بنجاح!")
    else:
        print("فشل إنشاء ملف التنصيب!")
    input("اضغط Enter للخروج...")