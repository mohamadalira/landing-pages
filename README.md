# ربات تلگرام ساخت لندینگ پیج

این ربات به شما کمک می‌کند تا لندینگ پیج حرفه‌ای برای محصولات خود بسازید و آن را در GitHub Pages منتشر کنید.

## ویژگی‌ها

- ساخت لندینگ پیج حرفه‌ای با HTML/CSS
- پشتیبانی از لایت مود و دارک مود
- 4 تمپلت آماده و امکان افزودن تمپلت سفارشی
- انتخاب رنگ اصلی و فرعی
- بررسی عضویت در کانال‌های اسپانسری
- آپلود خودکار به GitHub Pages
- پنل مدیریت برای کانال‌ها و تمپلت‌ها

## نصب و راه‌اندازی

### 1. نصب پکیج‌ها

```bash
pip install -r requirements.txt
```

### 2. تنظیمات

فایل `config.py` را باز کنید و اطلاعات زیر را وارد کنید:

- **BOT_TOKEN**: توکن ربات تلگرام (از @BotFather دریافت کنید)
- **GITHUB_TOKEN**: توکن GitHub (از Settings > Developer settings > Personal access tokens)
- **GITHUB_USERNAME**: نام کاربری GitHub شما
- **GITHUB_REPO_NAME**: نام ریپازیتوری برای ذخیره لندینگ پیج‌ها
- **SUPPORT_TELEGRAM_ID**: ایدی تلگرام برای پشتیبانی

### 3. اجرای ربات

```bash
python bot.py
```

## راهنمای دریافت توکن ربات

1. به ربات [@BotFather](https://t.me/BotFather) در تلگرام پیام دهید
2. دستور `/newbot` را ارسال کنید
3. نام ربات و یوزرنیم را وارد کنید
4. توکن دریافتی را در فایل `config.py` در قسمت `BOT_TOKEN` قرار دهید

## راهنمای دریافت توکن GitHub

1. به [GitHub Settings](https://github.com/settings/tokens) بروید
2. روی "Generate new token (classic)" کلیک کنید
3. دسترسی‌های `repo` (Full control) را فعال کنید
4. توکن را کپی کرده و در `config.py` در قسمت `GITHUB_TOKEN` قرار دهید

## راهنمای دریافت ایدی تلگرام

برای دریافت ایدی خود:
1. به ربات [@userinfobot](https://t.me/userinfobot) پیام دهید
2. ایدی عددی خود را کپی کنید
3. در `config.py` در قسمت `ADMIN_IDS` و `SUPPORT_TELEGRAM_ID` قرار دهید

## افزودن تمپلت سفارشی

1. پوشه جدید در `templates/` ایجاد کنید
2. فایل `template.html` را در آن قرار دهید
3. فایل `info.json` را با این ساختار ایجاد کنید:

```json
{
  "name": "نام تمپلت",
  "description": "توضیحات تمپلت",
  "id": 4
}
```

4. در فایل HTML از متغیرهای زیر استفاده کنید:
   - `{{PRODUCT_NAME}}` - نام محصول
   - `{{PRODUCT_IMAGE}}` - عکس محصول (base64)
   - `{{PRODUCT_DESCRIPTION}}` - توضیحات
   - `{{PRODUCT_PRICE}}` - قیمت
   - `{{PRIMARY_COLOR}}` - رنگ اصلی
   - `{{SECONDARY_COLOR}}` - رنگ فرعی

## مدیریت کانال‌های اسپانسری

برای مدیریت کانال‌های اسپانسری، دستور `/admin` را در ربات ارسال کنید.

## پشتیبانی

برای سفارش سایت تخصصی، با ایدی تعریف شده در `config.py` تماس بگیرید.

## لینک انتخاب رنگ

برای انتخاب رنگ دلخواه، از این لینک استفاده کنید:
https://htmlcolorcodes.com/color-picker/

## نصب سریع (ویندوز)

1. فایل `نصب.bat` را اجرا کنید
2. فایل `config.py` را ویرایش کنید
3. فایل `اجرا.bat` را اجرا کنید

## نصب سریع (لینوکس/Mac)

```bash
python install.py
python bot.py
```

## ساختار پروژه

```
landingpage/
├── bot.py                      # فایل اصلی ربات
├── config.py                   # تنظیمات (باید پر شود)
├── config.example.py           # نمونه تنظیمات
├── requirements.txt            # پکیج‌ها
├── landing_page_generator.py   # تولید لندینگ پیج
├── template_manager.py         # مدیریت تمپلت‌ها
├── github_uploader.py          # آپلود به GitHub
├── install.py                  # اسکریپت نصب
├── templates/                  # پوشه تمپلت‌های سفارشی
│   └── README.md
├── README.md                   # راهنمای اصلی
├── راهنمای_نصب.md            # راهنمای نصب
├── راهنمای_استفاده.md        # راهنمای استفاده
└── PROJECT_SUMMARY.md         # خلاصه پروژه
```

