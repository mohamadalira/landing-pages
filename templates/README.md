# راهنمای افزودن تمپلت سفارشی

برای افزودن تمپلت HTML/CSS سفارشی به ربات:

## مراحل

1. یک پوشه جدید در اینجا ایجاد کنید (مثلاً: `my-template`)

2. فایل `template.html` را در پوشه ایجاد کنید

3. فایل `info.json` را با این ساختار ایجاد کنید:

```json
{
  "name": "نام تمپلت شما",
  "description": "توضیحات تمپلت",
  "id": 4
}
```

**نکته:** ایدی باید منحصر به فرد باشد و از 4 شروع شود (0-3 برای تمپلت‌های پیش‌فرض)

## متغیرهای قابل استفاده در HTML

در فایل HTML خود می‌توانید از متغیرهای زیر استفاده کنید:

- `{{PRODUCT_NAME}}` - نام محصول
- `{{PRODUCT_IMAGE}}` - عکس محصول (به صورت base64)
- `{{PRODUCT_DESCRIPTION}}` - توضیحات محصول
- `{{PRODUCT_PRICE}}` - قیمت محصول
- `{{PRIMARY_COLOR}}` - رنگ اصلی
- `{{SECONDARY_COLOR}}` - رنگ فرعی

## مثال

```html
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{{PRODUCT_NAME}}</title>
    <style>
        body {
            background-color: {{PRIMARY_COLOR}};
            color: {{SECONDARY_COLOR}};
        }
    </style>
</head>
<body>
    <h1>{{PRODUCT_NAME}}</h1>
    <img src="{{PRODUCT_IMAGE}}" alt="{{PRODUCT_NAME}}">
    <p>{{PRODUCT_DESCRIPTION}}</p>
    <div class="price">{{PRODUCT_PRICE}}</div>
</body>
</html>
```

## نکات مهم

- حتماً از لایت مود و دارک مود پشتیبانی کنید
- طراحی را ریسپانسیو (responsive) کنید
- از متغیرهای رنگ برای سفارشی‌سازی استفاده کنید


