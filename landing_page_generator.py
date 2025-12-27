"""
تولید لندینگ پیج از تمپلت‌ها
"""

import base64
from template_manager import TemplateManager


class LandingPageGenerator:
    """کلاس تولید لندینگ پیج"""
    
    def generate(self, product_name: str, product_image: str, product_description: str,
                 product_link: str, template_id: int, primary_color: str, secondary_color: str) -> str:
        """تولید HTML لندینگ پیج"""
        
        # تبدیل عکس به base64
        image_base64 = self._image_to_base64(product_image)
        
        # انتخاب تمپلت
        if template_id == 0:
            return self._template_modern(product_name, image_base64, product_description, 
                                       product_link, primary_color, secondary_color)
        elif template_id == 1:
            return self._template_creative(product_name, image_base64, product_description,
                                         product_link, primary_color, secondary_color)
        elif template_id == 2:
            return self._template_business(product_name, image_base64, product_description,
                                         product_link, primary_color, secondary_color)
        elif template_id == 3:
            return self._template_premium(product_name, image_base64, product_description,
                                        product_link, primary_color, secondary_color)
        else:
            # تمپلت سفارشی
            custom_html = TemplateManager.get_template_html(template_id)
            if custom_html:
                return self._apply_custom_template(custom_html, product_name, image_base64,
                                                  product_description, product_link,
                                                  primary_color, secondary_color)
            else:
                # پیش‌فرض
                return self._template_modern(product_name, image_base64, product_description,
                                           product_link, primary_color, secondary_color)
    
    def _image_to_base64(self, image_path: str) -> str:
        """تبدیل عکس به base64"""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
                return base64.b64encode(image_data).decode('utf-8')
        except:
            return ""
    
    def _apply_custom_template(self, html: str, product_name: str, image_base64: str,
                               product_description: str, product_link: str,
                               primary_color: str, secondary_color: str) -> str:
        """اعمال داده‌ها به تمپلت سفارشی"""
        html = html.replace('{{PRODUCT_NAME}}', product_name)
        html = html.replace('{{PRODUCT_IMAGE}}', f'data:image/jpeg;base64,{image_base64}')
        html = html.replace('{{PRODUCT_DESCRIPTION}}', product_description)
        html = html.replace('{{PRODUCT_LINK}}', product_link)
        html = html.replace('{{PRIMARY_COLOR}}', primary_color)
        html = html.replace('{{SECONDARY_COLOR}}', secondary_color)
        return html
    
    def _template_modern(self, product_name: str, image_base64: str, product_description: str,
                        product_link: str, primary_color: str, secondary_color: str) -> str:
        """تمپلت مدرن و مینیمال"""
        return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            --bg-light: #ffffff;
            --bg-dark: #1a1a1a;
            --text-light: #333333;
            --text-dark: #ffffff;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: background-color 0.3s, color 0.3s;
        }}
        
        body.light-mode {{
            background-color: var(--bg-light);
            color: var(--text-light);
        }}
        
        body.dark-mode {{
            background-color: var(--bg-dark);
            color: var(--text-dark);
        }}
        
        .theme-toggle {{
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }}
        
        .theme-toggle:hover {{
            transform: scale(1.05);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 80px 20px;
        }}
        
        .hero {{
            text-align: center;
            padding: 60px 0;
        }}
        
        .product-image {{
            width: 100%;
            max-width: 600px;
            height: auto;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin: 40px 0;
        }}
        
        h1 {{
            font-size: 3.5em;
            margin-bottom: 20px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .description {{
            font-size: 1.3em;
            line-height: 1.8;
            margin: 30px 0;
            opacity: 0.9;
        }}
        
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 18px 50px;
            border: none;
            border-radius: 50px;
            font-size: 1.2em;
            cursor: pointer;
            text-decoration: none;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            margin: 40px 0;
        }}
        
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2em;
            }}
            .description {{
                font-size: 1.1em;
            }}
        }}
    </style>
</head>
<body class="light-mode">
    <button class="theme-toggle" onclick="toggleTheme()">🌓 تغییر تم</button>
    
    <div class="container">
        <div class="hero">
            <h1>{product_name}</h1>
            <img src="data:image/jpeg;base64,{image_base64}" alt="{product_name}" class="product-image">
            <p class="description">{product_description}</p>
            <a href="{product_link}" class="cta-button" target="_blank">اطلاعات بیشتر</a>
        </div>
    </div>
    
    <script>
        function toggleTheme() {{
            document.body.classList.toggle('light-mode');
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        }}
        
        // بارگذاری تم ذخیره شده
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {{
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
        }}
    </script>
</body>
</html>"""
    
    def _template_creative(self, product_name: str, image_base64: str, product_description: str,
                          product_link: str, primary_color: str, secondary_color: str) -> str:
        """تمپلت خلاقانه"""
        return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            --bg-light: #f8f9fa;
            --bg-dark: #0d1117;
            --text-light: #212529;
            --text-dark: #c9d1d9;
        }}
        
        body {{
            font-family: 'Vazir', 'Segoe UI', sans-serif;
            transition: all 0.3s;
        }}
        
        body.light-mode {{
            background: var(--bg-light);
            color: var(--text-light);
        }}
        
        body.dark-mode {{
            background: var(--bg-dark);
            color: var(--text-dark);
        }}
        
        .theme-toggle {{
            position: fixed;
            top: 30px;
            left: 30px;
            z-index: 1000;
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 30px;
            cursor: pointer;
            font-size: 18px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            transition: all 0.3s;
        }}
        
        .theme-toggle:hover {{
            transform: rotate(180deg) scale(1.1);
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 100px 40px;
        }}
        
        .hero-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
            margin-bottom: 80px;
        }}
        
        .content {{
            animation: fadeInRight 1s;
        }}
        
        .image-container {{
            animation: fadeInLeft 1s;
        }}
        
        @keyframes fadeInRight {{
            from {{
                opacity: 0;
                transform: translateX(50px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        @keyframes fadeInLeft {{
            from {{
                opacity: 0;
                transform: translateX(-50px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        h1 {{
            font-size: 4em;
            margin-bottom: 30px;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.2;
        }}
        
        .description {{
            font-size: 1.4em;
            line-height: 2;
            margin: 40px 0;
            opacity: 0.85;
        }}
        
        .product-image {{
            width: 100%;
            border-radius: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            transform: perspective(1000px) rotateY(-5deg);
            transition: transform 0.5s;
        }}
        
        .product-image:hover {{
            transform: perspective(1000px) rotateY(0deg) scale(1.05);
        }}
        
        .cta-button {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 20px 60px;
            border: none;
            border-radius: 50px;
            font-size: 1.3em;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            display: inline-block;
            margin: 40px auto;
        }}
        
        .cta-button:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.3);
        }}
        
        .cta-container {{
            text-align: center;
            margin: 60px 0;
        }}
        
        @media (max-width: 968px) {{
            .hero-section {{
                grid-template-columns: 1fr;
            }}
            h1 {{
                font-size: 2.5em;
            }}
        }}
    </style>
</head>
<body class="light-mode">
    <button class="theme-toggle" onclick="toggleTheme()">🌓</button>
    
    <div class="container">
        <div class="hero-section">
            <div class="content">
                <h1>{product_name}</h1>
                <p class="description">{product_description}</p>
            </div>
            <div class="image-container">
                <img src="data:image/jpeg;base64,{image_base64}" alt="{product_name}" class="product-image">
            </div>
        </div>
        
        <div class="cta-container">
            <a href="{product_link}" class="cta-button" target="_blank">اطلاعات بیشتر</a>
        </div>
    </div>
    
    <script>
        function toggleTheme() {{
            document.body.classList.toggle('light-mode');
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        }}
        
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {{
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
        }}
    </script>
</body>
</html>"""
    
    def _template_business(self, product_name: str, image_base64: str, product_description: str,
                          product_link: str, primary_color: str, secondary_color: str) -> str:
        """تمپلت تجاری"""
        return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            --bg-light: #ffffff;
            --bg-dark: #161b22;
            --text-light: #24292f;
            --text-dark: #f0f6fc;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: all 0.3s;
        }}
        
        body.light-mode {{
            background: var(--bg-light);
            color: var(--text-light);
        }}
        
        body.dark-mode {{
            background: var(--bg-dark);
            color: var(--text-dark);
        }}
        
        .theme-toggle {{
            position: fixed;
            top: 25px;
            left: 25px;
            z-index: 1000;
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            padding: 80px 0;
            text-align: center;
            color: white;
        }}
        
        h1 {{
            font-size: 3.5em;
            margin-bottom: 20px;
            font-weight: 700;
        }}
        
        .subtitle {{
            font-size: 1.3em;
            opacity: 0.95;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 80px 20px;
        }}
        
        .product-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            margin: 60px 0;
            align-items: center;
        }}
        
        .product-image {{
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }}
        
        .product-info {{
            padding: 40px;
        }}
        
        .description {{
            font-size: 1.2em;
            line-height: 2;
            margin: 30px 0;
            opacity: 0.9;
        }}
        
        .cta-container {{
            text-align: center;
            margin: 40px 0;
        }}
        
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 18px 50px;
            border: none;
            border-radius: 8px;
            font-size: 1.2em;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s;
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        }}
        
        @media (max-width: 968px) {{
            .product-section {{
                grid-template-columns: 1fr;
            }}
            h1 {{
                font-size: 2.5em;
            }}
        }}
    </style>
</head>
<body class="light-mode">
    <button class="theme-toggle" onclick="toggleTheme()">🌓 تغییر تم</button>
    
    <div class="header">
        <div class="container">
            <h1>{product_name}</h1>
            <p class="subtitle">محصولی استثنایی برای شما</p>
        </div>
    </div>
    
    <div class="container">
        <div class="product-section">
            <div>
                <img src="data:image/jpeg;base64,{image_base64}" alt="{product_name}" class="product-image">
            </div>
            <div class="product-info">
                <h2>درباره محصول</h2>
                <p class="description">{product_description}</p>
            </div>
        </div>
        
        <div class="cta-container">
            <a href="{product_link}" class="cta-button" target="_blank">اطلاعات بیشتر</a>
        </div>
    </div>
    
    <script>
        function toggleTheme() {{
            document.body.classList.toggle('light-mode');
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        }}
        
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {{
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
        }}
    </script>
</body>
</html>"""
    
    def _template_premium(self, product_name: str, image_base64: str, product_description: str,
                         product_link: str, primary_color: str, secondary_color: str) -> str:
        """تمپلت پریمیوم"""
        return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            --bg-light: #fafafa;
            --bg-dark: #0a0a0a;
            --text-light: #1a1a1a;
            --text-dark: #e0e0e0;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow-x: hidden;
            transition: all 0.3s;
        }}
        
        body.light-mode {{
            background: var(--bg-light);
            color: var(--text-light);
        }}
        
        body.dark-mode {{
            background: var(--bg-dark);
            color: var(--text-dark);
        }}
        
        .theme-toggle {{
            position: fixed;
            top: 30px;
            left: 30px;
            z-index: 1000;
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            transition: all 0.3s;
        }}
        
        .theme-toggle:hover {{
            transform: scale(1.1);
            box-shadow: 0 12px 35px rgba(0,0,0,0.4);
        }}
        
        .hero {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            padding: 100px 20px;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, var(--primary-color)22, var(--secondary-color)22);
            opacity: 0.1;
            z-index: -1;
        }}
        
        .content-wrapper {{
            max-width: 1400px;
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 80px;
            align-items: center;
        }}
        
        .text-content {{
            z-index: 1;
        }}
        
        h1 {{
            font-size: 5em;
            font-weight: 800;
            margin-bottom: 40px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.1;
        }}
        
        .description {{
            font-size: 1.4em;
            line-height: 2;
            margin: 50px 0;
            opacity: 0.85;
            font-weight: 300;
        }}
        
        .image-wrapper {{
            position: relative;
            z-index: 1;
        }}
        
        .product-image {{
            width: 100%;
            border-radius: 40px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.3);
            transform: perspective(1200px) rotateY(-8deg);
            transition: transform 0.6s;
        }}
        
        .product-image:hover {{
            transform: perspective(1200px) rotateY(0deg) scale(1.05);
        }}
        
        .cta-container {{
            text-align: center;
            margin-top: 80px;
        }}
        
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 25px 70px;
            border: none;
            border-radius: 50px;
            font-size: 1.4em;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.4s;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .cta-button:hover {{
            transform: translateY(-8px) scale(1.05);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        @media (max-width: 1024px) {{
            .content-wrapper {{
                grid-template-columns: 1fr;
            }}
            h1 {{
                font-size: 3em;
            }}
        }}
    </style>
</head>
<body class="light-mode">
    <button class="theme-toggle" onclick="toggleTheme()">🌓 تغییر تم</button>
    
    <div class="hero">
        <div class="content-wrapper">
            <div class="text-content">
                <h1>{product_name}</h1>
                <p class="description">{product_description}</p>
            </div>
            <div class="image-wrapper">
                <img src="data:image/jpeg;base64,{image_base64}" alt="{product_name}" class="product-image">
            </div>
        </div>
    </div>
    
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
        <div class="cta-container">
            <a href="{product_link}" class="cta-button" target="_blank">اطلاعات بیشتر</a>
        </div>
    </div>
    
    <script>
        function toggleTheme() {{
            document.body.classList.toggle('light-mode');
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        }}
        
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {{
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
        }}
    </script>
</body>
</html>"""


