"""
آپلود لندینگ پیج به GitHub
"""

import os
from github import Github
from config import GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO_NAME


class GitHubUploader:
    """کلاس آپلود به GitHub"""
    
    def __init__(self):
        self.token = GITHUB_TOKEN
        self.username = GITHUB_USERNAME
        self.repo_name = GITHUB_REPO_NAME
    
    async def upload(self, html_content: str, repo_name: str) -> str:
        """آپلود HTML به GitHub و برگرداندن لینک"""
        import asyncio
        
        def _upload_sync():
            """تابع همگام برای آپلود"""
            try:
                g = Github(self.token)
                user = g.get_user()
                
                # بررسی وجود ریپازیتوری
                try:
                    repo = user.get_repo(self.repo_name)
                except:
                    # ساخت ریپازیتوری جدید
                    repo = user.create_repo(
                        self.repo_name,
                        description="Landing pages repository",
                        private=False,
                        auto_init=False
                    )
                
                # آپلود فایل HTML
                file_path = f"{repo_name}/index.html"
                try:
                    # حذف فایل قبلی اگر وجود داشته باشد
                    try:
                        contents = repo.get_contents(file_path)
                        repo.delete_file(
                            contents.path,
                            f"Update {repo_name}",
                            contents.sha
                        )
                    except:
                        pass
                    
                    # آپلود فایل جدید
                    repo.create_file(
                        file_path,
                        f"Create landing page: {repo_name}",
                        html_content,
                        branch="main"
                    )
                except Exception as e:
                    # اگر فایل وجود نداشت، ایجاد می‌کنیم
                    repo.create_file(
                        file_path,
                        f"Create landing page: {repo_name}",
                        html_content,
                        branch="main"
                    )
                
                # ساخت لینک
                url = f"https://{self.username}.github.io/{self.repo_name}/{repo_name}/"
                return url
                
            except Exception as e:
                raise Exception(f"خطا در آپلود به GitHub: {str(e)}")
        
        # اجرای تابع همگام در یک thread pool
        loop = asyncio.get_event_loop()
        url = await loop.run_in_executor(None, _upload_sync)
        return url

