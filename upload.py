# upload_fixed.py
import requests
import base64
import json
from config import GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO_NAME


def check_and_create_repo():
    """بررسی و ایجاد ریپازیتوری اگر وجود ندارد"""
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 1. بررسی وجود ریپو
    check_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}"
    response = requests.get(check_url, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ ریپازیتوری '{GITHUB_REPO_NAME}' پیدا شد")
        return True
    elif response.status_code == 404:
        print(f"📁 ریپازیتوری '{GITHUB_REPO_NAME}' پیدا نشد - در حال ایجاد...")
        
        # 2. ایجاد ریپو جدید
        create_url = "https://api.github.com/user/repos"
        repo_data = {
            "name": GITHUB_REPO_NAME,
            "description": "Landing pages repository",
            "private": False,
            "auto_init": True,  # README ایجاد کن
            "has_issues": False,
            "has_projects": False,
            "has_wiki": False
        }
        
        create_response = requests.post(create_url, headers=headers, json=repo_data)
        
        if create_response.status_code == 201:
            print(f"✅ ریپازیتوری با موفقیت ایجاد شد")
            return True
        else:
            print(f"❌ خطا در ایجاد ریپو: {create_response.status_code} - {create_response.text}")
            return False
    else:
        print(f"❌ خطای ناشناخته: {response.status_code} - {response.text}")
        return False


def upload_file(html_content: str, page_name: str) -> str:
    """آپلود فایل به GitHub"""
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    # 1. اول ریپو را چک/ایجاد کن
    if not check_and_create_repo():
        raise Exception("نمی‌توان ریپازیتوری را ایجاد یا پیدا کرد")
    
    # 2. مسیر فایل
    file_path = f"{page_name}/index.html"
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}/contents/{file_path}"
    
    # 3. محتوای HTML را encode کن
    content_bytes = html_content.encode('utf-8')
    content_base64 = base64.b64encode(content_bytes).decode('utf-8')
    
    # 4. ابتدا چک کن فایل وجود دارد یا نه
    get_response = requests.get(url, headers=headers)
    
    data = {
        "message": f"Add landing page: {page_name}",
        "content": content_base64,
        "branch": "main"
    }
    
    if get_response.status_code == 200:
        # فایل وجود دارد - آپدیت
        existing_data = get_response.json()
        data["sha"] = existing_data["sha"]
        data["message"] = f"Update landing page: {page_name}"
        print("📝 فایل موجود آپدیت می‌شود")
    elif get_response.status_code == 404:
        # فایل وجود ندارد - ایجاد جدید
        print("🆕 فایل جدید ایجاد می‌شود")
    else:
        print(f"⚠️  وضعیت غیرمنتظره: {get_response.status_code}")
    
    # 5. آپلود فایل
    response = requests.put(url, headers=headers, json=data)
    
    print(f"📤 وضعیت آپلود: {response.status_code}")
    
    if response.status_code in [200, 201]:
        result = response.json()
        print(f"✅ فایل با موفقیت آپلود شد")
        print(f"📎 Commit SHA: {result['commit']['sha'][:10]}...")
        
        # لینک صفحه
        page_url = f"https://{GITHUB_USERNAME}.github.io/{GITHUB_REPO_NAME}/{page_name}/"
        return page_url
    else:
        error_msg = f"❌ خطا در آپلود: {response.status_code}\n"
        error_msg += f"پیام: {response.text}"
        raise Exception(error_msg)


# تست اجرا
if __name__ == "__main__":
    
    # محتوای HTML تست
    html_test = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>صفحه تست</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            margin: 20px;
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        p {
            font-size: 1.2em;
            line-height: 1.6;
            margin-bottom: 30px;
        }
        .success {
            background: #10b981;
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            font-weight: bold;
            display: inline-block;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 موفقیت‌آمیز!</h1>
        <p>صفحه لندینگ شما با موفقیت بر روی GitHub Pages قرار گرفت.</p>
        <div class="success">آپلود کامل شد ✅</div>
        <p style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
            ایجاد شده توسط سیستم اتوماتیک - ۱۴۰۳
        </p>
    </div>
</body>
</html>"""
    
    try:
        print("🚀 شروع فرآیند آپلود...")
        print("=" * 50)
        
        # آپلود
        page_url = upload_file(html_test, "test-landing-page")
        
        print("=" * 50)
        print(f"🌐 ل"""
آپلود لندینگ پیج به GitHub
"""

import os
import asyncio
from github import Github, GithubException
from config import GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO_NAME


class GitHubUploader:
    """کلاس آپلود به GitHub"""
    
    def __init__(self):
        self.token = GITHUB_TOKEN
        self.username = GITHUB_USERNAME
        self.repo_name = GITHUB_REPO_NAME
    
    async def upload(self, html_content: str, page_name: str) -> str:
        """آپلود HTML به GitHub و برگرداندن لینک"""
        
        def _upload_sync():
            """تابع همگام برای آپلود"""
            try:
                print(f"🔗 در حال اتصال به GitHub...")
                g = Github(self.token)
                user = g.get_user()
                print(f"✅ کاربر: {user.login}")
                
                # بررسی وجود ریپازیتوری
                try:
                    repo = user.get_repo(self.repo_name)
                    print(f"📁 ریپازیتوری '{self.repo_name}' پیدا شد")
                except GithubException:
                    print(f"📦 ایجاد ریپازیتوری جدید: {self.repo_name}")
                    # ساخت ریپازیتوری جدید
                    repo = user.create_repo(
                        self.repo_name,
                        description="Landing pages repository",
                        private=False,
                        auto_init=False
                    )
                    print(f"✅ ریپازیتوری ایجاد شد")
                
                # آپلود فایل HTML
                file_path = f"{page_name}/index.html"
                print(f"📤 آپلود فایل: {file_path}")
                
                try:
                    # بررسی و حذف فایل قبلی اگر وجود داشته باشد
                    try:
                        contents = repo.get_contents(file_path, ref="main")
                        print(f"🗑️ حذف فایل قبلی...")
                        repo.delete_file(
                            contents.path,
                            f"Update landing page: {page_name}",
                            contents.sha,
                            branch="main"
                        )
                        print(f"✅ فایل قبلی حذف شد")
                    except GithubException as e:
                        if e.status == 404:
                            print(f"🆕 فایل جدید ایجاد می‌شود")
                        else:
                            print(f"⚠️ خطا در بررسی فایل: {e}")
                            pass
                    
                    # آپلود فایل جدید
                    repo.create_file(
                        file_path,
                        f"Create landing page: {page_name}",
                        html_content,
                        branch="main"
                    )
                    print(f"✅ فایل با موفقیت آپلود شد")
                    
                except Exception as e:
                    print(f"⚠️ خطا در آپلود، تلاش مجدد...")
                    # اگر فایل وجود نداشت، ایجاد می‌کنیم
                    repo.create_file(
                        file_path,
                        f"Create landing page: {page_name}",
                        html_content,
                        branch="main"
                    )
                    print(f"✅ فایل ایجاد شد")
                
                # ساخت لینک
                url = f"https://{self.username}.github.io/{self.repo_name}/{page_name}/"
                print(f"🌐 لینک صفحه: {url}")
                return url
                
            except Exception as e:
                error_msg = f"❌ خطا در آپلود به GitHub: {str(e)}"
                print(error_msg)
                raise Exception(error_msg)
        
        # اجرای تابع همگام در یک thread pool
        loop = asyncio.get_event_loop()
        url = await loop.run_in_executor(None, _upload_sync)
        return url
    
    async def upload_with_css_js(self, html_content: str, css_content: str = None, 
                                js_content: str = None, page_name: str = None) -> dict:
        """آپلود صفحه کامل با HTML, CSS و JavaScript"""
        
        if not page_name:
            import uuid
            page_name = f"page-{str(uuid.uuid4())[:8]}"
        
        results = {
            "page_name": page_name,
            "html_url": None,
            "css_url": None,
            "js_url": None,
            "page_url": None
        }
        
        # آپلود HTML
        results["page_url"] = await self.upload(html_content, page_name)
        results["html_url"] = f"https://raw.githubusercontent.com/{self.username}/{self.repo_name}/main/{page_name}/index.html"
        
        # آپلود CSS اگر وجود دارد
        if css_content:
            css_url = await self.upload_file(css_content, f"{page_name}/style.css", 
                                           f"Add CSS for {page_name}")
            results["css_url"] = css_url
        
        # آپلود JavaScript اگر وجود دارد
        if js_content:
            js_url = await self.upload_file(js_content, f"{page_name}/script.js", 
                                          f"Add JS for {page_name}")
            results["js_url"] = js_url
        
        return results
    
    async def upload_file(self, content: str, file_path: str, commit_message: str) -> str:
        """آپلود یک فایل به ریپازیتوری"""
        
        def _upload_file_sync():
            try:
                g = Github(self.token)
                user = g.get_user()
                repo = user.get_repo(self.repo_name)
                
                print(f"📤 آپلود فایل: {file_path}")
                
                try:
                    # بررسی وجود فایل قبلی
                    contents = repo.get_contents(file_path, ref="main")
                    repo.delete_file(
                        contents.path,
                        f"Update {commit_message}",
                        contents.sha,
                        branch="main"
                    )
                except GithubException as e:
                    if e.status != 404:
                        print(f"⚠️ خطا در بررسی فایل: {e}")
                
                # آپلود فایل جدید
                repo.create_file(
                    file_path,
                    commit_message,
                    content,
                    branch="main"
                )
                
                print(f"✅ فایل {file_path} آپلود شد")
                return f"https://raw.githubusercontent.com/{self.username}/{self.repo_name}/main/{file_path}"
                
            except Exception as e:
                raise Exception(f"خطا در آپلود فایل {file_path}: {str(e)}")
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _upload_file_sync)


# تابع کمکی برای استفاده آسان
async def upload_landing_page(html_content: str, page_name: str = None) -> str:
    """
    تابع سریع برای آپلود صفحه لندینگ
    
    مثال استفاده:
        url = await upload_landing_page(html_content, "my-page")
    """
    uploader = GitHubUploader()
    if not page_name:
        import uuid
        page_name = f"page-{str(uuid.uuid4())[:8]}"
    
    return await uploader.upload(html_content, page_name)


# مثال استفاده
async def example_usage():
    """نمونه استفاده از کلاس"""
    
    uploader = GitHubUploader()
    
    # محتوای HTML نمونه
    sample_html = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>صفحه نمونه</title>
        <style>
            body {
                font-family: Tahoma, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                text-align: center;
                padding: 20px;
            }
            .container {
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 موفقیت‌آمیز!</h1>
            <p>صفحه شما با موفقیت آپلود شد.</p>
            <p>تاریخ: ۱۴۰۳</p>
        </div>
    </body>
    </html>
    """
    
    try:
        print("🚀 شروع آپلود صفحه...")
        
        # روش ۱: آپلود ساده
        url = await uploader.upload(sample_html, "test-page")
        print(f"\n✅ لینک صفحه: {url}")
        
        # روش ۲: آپلود پیشرفته
        sample_css = """
        body {
            background: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        """
        
        sample_js = """
        console.log('صفحه لود شد!');
        """
        
        results = await uploader.upload_with_css_js(
            html_content=sample_html,
            css_content=sample_css,
            js_content=sample_js,
            page_name="advanced-page"
        )
        
        print(f"\n📊 نتایج آپلود پیشرفته:")
        print(f"نام صفحه: {results['page_name']}")
        print(f"لینک صفحه: {results['page_url']}")
        print(f"لینک HTML: {results['html_url']}")
        if results['css_url']:
            print(f"لینک CSS: {results['css_url']}")
        if results['js_url']:
            print(f"لینک JS: {results['js_url']}")
        
    except Exception as e:
        print(f"❌ خطا: {e}")


# برای اجرای مستقیم
if __name__ == "__main__":
    import asyncio
    
    # اجرای مثال
    asyncio.run(example_usage())ینک صفحه شما:")
        print(f"🔗 {page_url}")
        print("=" * 50)
        print("✅ عملیات با موفقیت انجام شد!")
        
    except Exception as e:
        print("=" * 50)
        print(f"❌ خطا:")
        print(str(e))
        print("=" * 50)