"""
ربات تلگرام برای ساخت لندینگ پیج
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN, GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO_NAME, SUPPORT_TELEGRAM_ID, SPONSOR_CHANNELS, ADMIN_IDS
from landing_page_generator import LandingPageGenerator
from github_uploader import GitHubUploader
from template_manager import TemplateManager

# تنظیم لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دیتابیس ساده برای ذخیره اطلاعات کاربران
user_data: Dict[int, Dict] = {}

# دیتابیس برای وضعیت ادمین‌ها
admin_states: Dict[int, str] = {}

# فایل برای ذخیره کانال‌های اسپانسری
CHANNELS_FILE = "sponsor_channels.json"


def load_channels():
    """بارگذاری کانال‌های اسپانسری از فایل"""
    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return SPONSOR_CHANNELS.copy()


def save_channels(channels):
    """ذخیره کانال‌های اسپانسری در فایل"""
    with open(CHANNELS_FILE, 'w', encoding='utf-8') as f:
        json.dump(channels, f, ensure_ascii=False, indent=2)


async def check_channel_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """بررسی عضویت کاربر در کانال‌های اسپانسری"""
    channels = load_channels()
    if not channels:
        return True  # اگر کانالی تعریف نشده، اجازه دسترسی بده
    
    user_id = update.effective_user.id
    
    for channel in channels:
        try:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            logger.error(f"Error checking channel {channel}: {e}")
            return False
    
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    user_id = update.effective_user.id
    
    # بررسی عضویت در کانال‌ها
    if not await check_channel_membership(update, context):
        channels = load_channels()
        channels_text = "\n".join([f"• {ch}" for ch in channels])
        await update.message.reply_text(
            f"⚠️ برای استفاده از ربات، ابتدا باید در کانال‌های زیر عضو شوید:\n\n{channels_text}\n\n"
            f"پس از عضویت، دوباره /start را ارسال کنید.",
            parse_mode='HTML'
        )
        return
    
    # پاک کردن داده‌های قبلی کاربر
    user_data[user_id] = {
        'step': 'waiting_product_name',
        'product_name': None,
        'product_image': None,
        'product_description': None,
        'template_id': None,
        'primary_color': None,
        'secondary_color': None,
        'product_link': None
    }
    
    await update.message.reply_text("📝 لطفا نام محصول را ارسال کنید:")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت کلیک روی دکمه‌های اینلاین"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if user_id not in user_data:
        await query.edit_message_text("❌ لطفا دوباره /start کنید.")
        return
    
    data = query.data
    user_info = user_data[user_id]
    
    if data.startswith("template_"):
        template_id = int(data.split("_")[1])
        user_info['template_id'] = template_id
        user_info['step'] = 'waiting_primary_color'
        await query.edit_message_text(
            "🎨 حالا رنگ اصلی (Primary Color) را انتخاب کنید:\n\n"
            "می‌توانید از گزینه‌های زیر انتخاب کنید یا کد رنگ HEX خود را ارسال کنید (مثل: #FF5733)\n\n"
            "💡 برای انتخاب رنگ دلخواه:\nhttps://htmlcolorcodes.com/color-picker/",
            reply_markup=get_color_keyboard("primary")
        )
    
    elif data.startswith("color_primary_"):
        color = data.replace("color_primary_", "")
        if color == "custom":
            user_info['step'] = 'waiting_primary_color_custom'
            await query.edit_message_text("🎨 لطفا کد رنگ HEX را ارسال کنید (مثل: #FF5733):")
        else:
            user_info['primary_color'] = color
            user_info['step'] = 'waiting_secondary_color'
            await query.edit_message_text(
                "🎨 حالا رنگ فرعی (Secondary Color) را انتخاب کنید:\n\n"
                "💡 برای انتخاب رنگ دلخواه:\nhttps://htmlcolorcodes.com/color-picker/",
                reply_markup=get_color_keyboard("secondary")
            )
    
    elif data.startswith("color_secondary_"):
        color = data.replace("color_secondary_", "")
        if color == "custom":
            await query.edit_message_text("🎨 لطفا کد رنگ HEX را ارسال کنید (مثل: #FF5733):")
            user_info['step'] = 'waiting_secondary_color_custom'
        else:
            user_info['secondary_color'] = color
            user_info['step'] = 'waiting_link'
            await query.edit_message_text("🔗 لطفا لینکی که می‌خواهید در صفحه قرار دهید را ارسال کنید:")
    
    elif data.startswith("admin_"):
        # بررسی ادمین بودن
        if not ADMIN_IDS or user_id not in ADMIN_IDS:
            await query.edit_message_text("❌ شما دسترسی به این بخش ندارید.")
            return
        await handle_admin_callback(update, context, data)


def get_color_keyboard(color_type: str):
    """ساخت کیبورد برای انتخاب رنگ"""
    colors = [
        ("🔴 قرمز", "#FF0000"),
        ("🟠 نارنجی", "#FF6B35"),
        ("🟡 زرد", "#FFD23F"),
        ("🟢 سبز", "#06A77D"),
        ("🔵 آبی", "#1E88E5"),
        ("🟣 بنفش", "#9C27B0"),
        ("⚫ مشکی", "#000000"),
        ("⚪ سفید", "#FFFFFF"),
        ("🔘 خاکستری", "#757575"),
        ("🎨 رنگ دلخواه", "custom")
    ]
    
    buttons = []
    for i in range(0, len(colors), 2):
        row = []
        for j in range(2):
            if i + j < len(colors):
                name, value = colors[i + j]
                row.append(InlineKeyboardButton(
                    name,
                    callback_data=f"color_{color_type}_{value}"
                ))
        buttons.append(row)
    
    return InlineKeyboardMarkup(buttons)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پیام‌های متنی"""
    user_id = update.effective_user.id
    text = update.message.text
    
    # بررسی دستورات ادمین
    if user_id in admin_states:
        if admin_states[user_id] == 'waiting_channel_add':
            channel = text.strip()
            if not channel.startswith('@'):
                await update.message.reply_text("❌ ایدی کانال باید با @ شروع شود (مثل: @channel_name)")
                return
            
            channels = load_channels()
            if channel in channels:
                await update.message.reply_text(f"⚠️ کانال {channel} از قبل وجود دارد.")
            else:
                channels.append(channel)
                save_channels(channels)
                await update.message.reply_text(f"✅ کانال {channel} با موفقیت اضافه شد.")
            
            del admin_states[user_id]
            return
    
    # بررسی دستورات عادی کاربر
    if user_id not in user_data:
        await update.message.reply_text("❌ لطفا /start کنید.")
        return
    
    user_info = user_data[user_id]
    step = user_info['step']
    
    if step == 'waiting_product_name':
        user_info['product_name'] = text
        user_info['step'] = 'waiting_product_image'
        await update.message.reply_text("📷 لطفا عکس محصول را ارسال کنید:")
    
    elif step == 'waiting_product_image':
        await update.message.reply_text("❌ لطفا یک عکس ارسال کنید.")
    
    elif step == 'waiting_product_description':
        user_info['product_description'] = text
        user_info['step'] = 'waiting_template'
        await show_template_selection(update, context)
    
    elif step == 'waiting_primary_color_custom':
        if is_valid_hex_color(text):
            user_info['primary_color'] = text
            user_info['step'] = 'waiting_secondary_color'
            await update.message.reply_text(
                "🎨 حالا رنگ فرعی (Secondary Color) را انتخاب کنید:",
                reply_markup=get_color_keyboard("secondary")
            )
        else:
            await update.message.reply_text("❌ کد رنگ نامعتبر است. لطفا کد HEX معتبر ارسال کنید (مثل: #FF5733)")
    
    elif step == 'waiting_secondary_color_custom':
        if is_valid_hex_color(text):
            user_info['secondary_color'] = text
            user_info['step'] = 'waiting_link'
            await update.message.reply_text("🔗 لطفا لینکی که می‌خواهید در صفحه قرار دهید را ارسال کنید:")
        else:
            await update.message.reply_text("❌ کد رنگ نامعتبر است. لطفا کد HEX معتبر ارسال کنید (مثل: #FF5733)")
    
    elif step == 'waiting_link':
        # بررسی معتبر بودن لینک
        if text.strip().startswith(('http://', 'https://')):
            user_info['product_link'] = text.strip()
            await process_landing_page_creation(update, context, user_id)
        else:
            await update.message.reply_text("❌ لطفا یک لینک معتبر ارسال کنید (باید با http:// یا https:// شروع شود)")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت دریافت عکس"""
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        await update.message.reply_text("❌ لطفا /start کنید.")
        return
    
    user_info = user_data[user_id]
    
    if user_info['step'] == 'waiting_product_image':
        # دریافت بزرگترین سایز عکس
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        # ذخیره عکس موقت
        os.makedirs("temp_images", exist_ok=True)
        file_path = f"temp_images/{user_id}_{photo.file_id}.jpg"
        await file.download_to_drive(file_path)
        
        user_info['product_image'] = file_path
        user_info['step'] = 'waiting_product_description'
        await update.message.reply_text("📝 لطفا توضیحات محصول را ارسال کنید:")


async def show_template_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش لیست تمپلت‌ها"""
    templates = TemplateManager.get_templates()
    
    buttons = []
    for i, template in enumerate(templates):
        buttons.append([InlineKeyboardButton(
            f"📄 {template['name']}",
            callback_data=f"template_{i}"
        )])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(
        "📄 لطفا یکی از تمپلت‌های زیر را انتخاب کنید:",
        reply_markup=reply_markup
    )


async def process_landing_page_creation(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """پردازش و ساخت لندینگ پیج"""
    user_info = user_data[user_id]
    
    # ارسال پیام در انتظار اگر از پیام متنی صدا زده شده
    if update.message:
        await update.message.reply_text("⏳ لطفا صبر کنید...")
    else:
        # اگر از callback query صدا زده شده، پیام جدید بفرست
        await context.bot.send_message(
            chat_id=user_id,
            text="⏳ لطفا صبر کنید..."
        )
    
    try:
        # ساخت لندینگ پیج
        generator = LandingPageGenerator()
        html_content = generator.generate(
            product_name=user_info['product_name'],
            product_image=user_info['product_image'],
            product_description=user_info['product_description'],
            product_link=user_info['product_link'],
            template_id=user_info['template_id'],
            primary_color=user_info['primary_color'],
            secondary_color=user_info['secondary_color']
        )
        
        # آپلود به گیت‌هاب
        uploader = GitHubUploader()
        repo_name = f"landing-{user_id}-{int(datetime.now().timestamp())}"
        url = await uploader.upload(html_content, repo_name)
        
        # ارسال لینک به کاربر
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ لندینگ پیج شما با موفقیت ساخته شد!\n\n🔗 لینک: {url}\n\n"
                 f"💡 برای سفارش سایت تخصصی با ایدی زیر تماس بگیرید:\n@{SUPPORT_TELEGRAM_ID}"
        )
        
        # پاک کردن داده‌های موقت
        if user_info.get('product_image') and os.path.exists(user_info['product_image']):
            os.remove(user_info['product_image'])
        
        del user_data[user_id]
        
    except Exception as e:
        logger.error(f"Error creating landing page: {e}")
        await context.bot.send_message(
            chat_id=user_id,
            text=f"❌ خطا در ساخت لندینگ پیج: {str(e)}"
        )


def is_valid_hex_color(color: str) -> bool:
    """بررسی معتبر بودن کد رنگ HEX"""
    pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return bool(re.match(pattern, color))


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور مدیریتی برای ادمین"""
    user_id = update.effective_user.id
    
    # بررسی ادمین بودن
    if not ADMIN_IDS or user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ شما دسترسی به این بخش ندارید.")
        return
    
    keyboard = [
        [InlineKeyboardButton("➕ افزودن کانال", callback_data="admin_add_channel")],
        [InlineKeyboardButton("➖ حذف کانال", callback_data="admin_remove_channel")],
        [InlineKeyboardButton("📋 لیست کانال‌ها", callback_data="admin_list_channels")],
        [InlineKeyboardButton("📄 مدیریت تمپلت‌ها", callback_data="admin_templates")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔧 پنل مدیریت",
        reply_markup=reply_markup
    )


async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    """مدیریت کلیک‌های بخش ادمین"""
    query = update.callback_query
    await query.answer()
    
    if data == "admin_add_channel":
        user_id = query.from_user.id
        admin_states[user_id] = 'waiting_channel_add'
        await query.edit_message_text("➕ لطفا ایدی کانال را ارسال کنید (مثل: @channel_name):")
    
    elif data == "admin_remove_channel":
        channels = load_channels()
        if not channels:
            await query.edit_message_text("❌ هیچ کانالی تعریف نشده است.")
        else:
            buttons = []
            for channel in channels:
                buttons.append([InlineKeyboardButton(
                    f"❌ {channel}",
                    callback_data=f"admin_delete_{channel}"
                )])
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(
                "➖ کانالی که می‌خواهید حذف کنید را انتخاب کنید:",
                reply_markup=reply_markup
            )
    
    elif data == "admin_list_channels":
        channels = load_channels()
        if not channels:
            await query.edit_message_text("❌ هیچ کانالی تعریف نشده است.")
        else:
            channels_text = "\n".join([f"• {ch}" for ch in channels])
            await query.edit_message_text(f"📋 کانال‌های اسپانسری:\n\n{channels_text}")
    
    elif data.startswith("admin_delete_"):
        channel = data.replace("admin_delete_", "")
        channels = load_channels()
        if channel in channels:
            channels.remove(channel)
            save_channels(channels)
            await query.edit_message_text(f"✅ کانال {channel} حذف شد.")
        else:
            await query.edit_message_text("❌ کانال یافت نشد.")
    
    elif data == "admin_templates":
        await query.edit_message_text("📄 برای افزودن تمپلت جدید، فایل HTML را در پوشه templates قرار دهید.")


def main():
    """تابع اصلی برای اجرای ربات"""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ لطفا توکن ربات را در فایل config.py وارد کنید.")
        return
    
    # ساخت اپلیکیشن
    application = Application.builder().token(BOT_TOKEN).build()
    
    # اضافه کردن handlerها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # اجرای ربات
    print("🤖 ربات در حال اجرا است...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

