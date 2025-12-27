"""
فایل نصب و راه‌اندازی خودکار
"""

import os
import subprocess
import sys


def install_requirements():
    """نصب پکیج‌های مورد نیاز"""
    print("📦 در حال نصب پکیج‌ها...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ پکیج‌ها با موفقیت نصب شدند.")
        return True
    except subprocess.CalledProcessError:
        print("❌ خطا در نصب پکیج‌ها.")
        return False


def check_config():
    """بررسی تنظیمات"""
    print("\n🔍 بررسی تنظیمات...")
    
    try:
        from config import BOT_TOKEN, GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO_NAME, SUPPORT_TELEGRAM_ID
        
        issues = []
        
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            issues.append("❌ توکن ربات تلگرام تنظیم نشده است")
        else:
            print("✅ توکن ربات تلگرام تنظیم شده است")
        
        if GITHUB_TOKEN == "YOUR_GITHUB_TOKEN_HERE":
            issues.append("❌ توکن GitHub تنظیم نشده است")
        else:
            print("✅ توکن GitHub تنظیم شده است")
        
        if GITHUB_USERNAME == "YOUR_GITHUB_USERNAME_HERE":
            issues.append("❌ نام کاربری GitHub تنظیم نشده است")
        else:
            print("✅ نام کاربری GitHub تنظیم شده است")
        
        if GITHUB_REPO_NAME == "landing-pages":
            print("⚠️ نام ریپازیتوری پیش‌فرض است (می‌توانید تغییر دهید)")
        else:
            print("✅ نام ریپازیتوری تنظیم شده است")
        
        if SUPPORT_TELEGRAM_ID == "YOUR_SUPPORT_TELEGRAM_ID_HERE":
            issues.append("❌ ایدی پشتیبانی تنظیم نشده است")
        else:
            print("✅ ایدی پشتیبانی تنظیم شده است")
        
        if issues:
            print("\n⚠️ مشکلات یافت شده:")
            for issue in issues:
                print(f"  {issue}")
            print("\nلطفا فایل config.py را ویرایش کنید.")
            return False
        else:
            print("\n✅ همه تنظیمات درست است!")
            return True
            
    except ImportError:
        print("❌ فایل config.py یافت نشد!")
        return False


def create_directories():
    """ایجاد پوشه‌های لازم"""
    print("\n📁 ایجاد پوشه‌ها...")
    
    directories = ["templates", "temp_images"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ پوشه {directory} ایجاد شد")
        else:
            print(f"ℹ️ پوشه {directory} از قبل وجود دارد")


def main():
    """تابع اصلی"""
    print("=" * 50)
    print("🚀 راه‌اندازی ربات ساخت لندینگ پیج")
    print("=" * 50)
    
    # ایجاد پوشه‌ها
    create_directories()
    
    # نصب پکیج‌ها
    if not install_requirements():
        print("\n❌ نصب با خطا مواجه شد!")
        return
    
    # بررسی تنظیمات
    config_ok = check_config()
    
    print("\n" + "=" * 50)
    if config_ok:
        print("✅ نصب با موفقیت انجام شد!")
        print("\nبرای اجرای ربات، دستور زیر را اجرا کنید:")
        print("  python bot.py")
    else:
        print("⚠️ لطفا تنظیمات را کامل کنید و دوباره این فایل را اجرا کنید.")
    print("=" * 50)


if __name__ == "__main__":
    main()


