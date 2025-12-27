"""
مدیریت تمپلت‌های لندینگ پیج
"""

import os
import json
from pathlib import Path


class TemplateManager:
    """کلاس مدیریت تمپلت‌ها"""
    
    TEMPLATES_DIR = "templates"
    
    @staticmethod
    def get_templates():
        """دریافت لیست تمپلت‌ها"""
        templates = []
        
        # تمپلت‌های پیش‌فرض
        default_templates = [
            {
                'id': 0,
                'name': 'تمپلت مدرن و مینیمال',
                'description': 'طراحی ساده و حرفه‌ای'
            },
            {
                'id': 1,
                'name': 'تمپلت خلاقانه',
                'description': 'طراحی خلاق و جذاب'
            },
            {
                'id': 2,
                'name': 'تمپلت تجاری',
                'description': 'مناسب برای کسب و کار'
            },
            {
                'id': 3,
                'name': 'تمپلت پریمیوم',
                'description': 'طراحی لوکس و حرفه‌ای'
            }
        ]
        
        templates.extend(default_templates)
        
        # بارگذاری تمپلت‌های سفارشی از پوشه templates
        if os.path.exists(TemplateManager.TEMPLATES_DIR):
            custom_templates = TemplateManager._load_custom_templates()
            templates.extend(custom_templates)
        
        return templates
    
    @staticmethod
    def _load_custom_templates():
        """بارگذاری تمپلت‌های سفارشی"""
        custom_templates = []
        templates_path = Path(TemplateManager.TEMPLATES_DIR)
        
        for template_dir in templates_path.iterdir():
            if template_dir.is_dir():
                info_file = template_dir / "info.json"
                if info_file.exists():
                    try:
                        with open(info_file, 'r', encoding='utf-8') as f:
                            info = json.load(f)
                            custom_templates.append({
                                'id': len(custom_templates) + 4,
                                'name': info.get('name', template_dir.name),
                                'description': info.get('description', ''),
                                'path': str(template_dir)
                            })
                    except:
                        pass
        
        return custom_templates
    
    @staticmethod
    def get_template_html(template_id: int):
        """دریافت HTML تمپلت"""
        # تمپلت‌های پیش‌فرض در landing_page_generator ساخته می‌شوند
        if template_id < 4:
            return None  # از generator استفاده می‌شود
        
        # بارگذاری تمپلت سفارشی
        templates_path = Path(TemplateManager.TEMPLATES_DIR)
        for template_dir in templates_path.iterdir():
            if template_dir.is_dir():
                info_file = template_dir / "info.json"
                if info_file.exists():
                    try:
                        with open(info_file, 'r', encoding='utf-8') as f:
                            info = json.load(f)
                            if info.get('id') == template_id:
                                html_file = template_dir / "template.html"
                                if html_file.exists():
                                    with open(html_file, 'r', encoding='utf-8') as f:
                                        return f.read()
                    except:
                        pass
        
        return None


