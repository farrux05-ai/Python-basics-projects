# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 10:19:47 2025

@author: U S E R
"""
pip install python-telegram-bot
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List
import json
import os
from dataclasses import dataclass, asdict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot tokenini bu yerga kiriting
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Admin ID (stadion egasining Telegram ID)
ADMIN_ID = 123456789  # Bu yerga admin IDni kiriting

@dataclass
class Booking:
    id: str
    date: str
    time_slot: str
    duration: int
    customer_name: str
    customer_phone: str
    customer_id: int
    status: str  # "pending", "confirmed", "cancelled"
    created_at: str

class StadiumBot:
    def __init__(self):
        self.bookings: Dict[str, Booking] = {}
        self.time_slots = [
            "08:00-10:00", "10:00-12:00", "12:00-14:00", 
            "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00"
        ]
        self.prices = {
            "2_hours": 100000,  # 2 soat - 100,000 so'm
            "3_hours": 140000,  # 3 soat - 140,000 so'm
            "full_day": 500000  # To'liq kun - 500,000 so'm
        }
        self.load_bookings()

    def save_bookings(self):
        """Bronlarni faylga saqlash"""
        try:
            with open('bookings.json', 'w', encoding='utf-8') as f:
                bookings_dict = {k: asdict(v) for k, v in self.bookings.items()}
                json.dump(bookings_dict, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Bronlarni saqlashda xatolik: {e}")

    def load_bookings(self):
        """Bronlarni fayldan yuklash"""
        try:
            if os.path.exists('bookings.json'):
                with open('bookings.json', 'r', encoding='utf-8') as f:
                    bookings_dict = json.load(f)
                    self.bookings = {k: Booking(**v) for k, v in bookings_dict.items()}
        except Exception as e:
            logger.error(f"Bronlarni yuklashda xatolik: {e}")

    def get_available_slots(self, date: str) -> List[str]:
        """Berilgan sanada bo'sh vaqtlarni topish"""
        booked_slots = []
        for booking in self.bookings.values():
            if booking.date == date and booking.status == "confirmed":
                booked_slots.append(booking.time_slot)
        
        return [slot for slot in self.time_slots if slot not in booked_slots]

    def generate_booking_id(self) -> str:
        """Yangi bron IDsini yaratish"""
        return f"BOOK_{datetime.now().strftime('%Y%m%d%H%M%S')}"

stadium_bot = StadiumBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start komandasi"""
    user_id = update.effective_user.id
    
    if user_id == ADMIN_ID:
        text = """
🏟 **STADION ADMIN PANEL**

Assalomu alaykum! Siz stadion adminisiz.

Mavjud komandalar:
/schedule - Kun va vaqtlarni ko'rish
/bookings - Barcha bronlarni ko'rish
/confirm - Bronlarni tasdiqlash
        """
    else:
        text = """
🏟 **FUTBOL STADIONI**

Assalomu alaykum! 

Bizning stadionimizga xush kelibsiz!
📍 Manzil: Toshkent shahar
📞 Telefon: +998 XX XXX XX XX

**Narxlar:**
🕐 2 soat - 100,000 so'm
🕕 3 soat - 140,000 so'm
🏟 To'liq kun - 500,000 so'm

**Ish vaqti:** 08:00 - 22:00

Bron qilish uchun /schedule tugmasini bosing!
        """
    
    keyboard = [[InlineKeyboardButton("📅 Vaqtlarni ko'rish", callback_data="view_schedule")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def view_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jadval ko'rish"""
    query = update.callback_query
    await query.answer()
    
    # Keyingi 7 kunning sanalarini yaratish
    dates = []
    for i in range(7):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        dates.append(date)
    
    keyboard = []
    for date in dates:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_text = date_obj.strftime('%d.%m.%Y - %A')
        keyboard.append([InlineKeyboardButton(date_text, callback_data=f"date_{date}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "📅 **SANA TANLANG**\n\nQaysi sanaga bron qilmoqchisiz?"
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_date_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tanlangan sana uchun jadval"""
    query = update.callback_query
    await query.answer()
    
    date = query.data.split('_')[1]
    available_slots = stadium_bot.get_available_slots(date)
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_text = date_obj.strftime('%d.%m.%Y - %A')
    
    text = f"📅 **{date_text}**\n\n"
    text += "🏟 **STADION HOLATI:**\n\n"
    
    for slot in stadium_bot.time_slots:
        if slot in available_slots:
            text += f"✅ {slot} - Bo'sh\n"
        else:
            text += f"❌ {slot} - Band\n"
    
    text += f"\n💰 **NARXLAR:**\n"
    text += f"🕐 2 soat - {stadium_bot.prices['2_hours']:,} so'm\n"
    text += f"🕕 3 soat - {stadium_bot.prices['3_hours']:,} so'm\n"
    text += f"🏟 To'liq kun - {stadium_bot.prices['full_day']:,} so'm\n"
    
    keyboard = []
    if available_slots:
        keyboard.append([InlineKeyboardButton("📝 Bron qilish", callback_data=f"book_{date}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="view_schedule")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def book_stadium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stadion bronlash"""
    query = update.callback_query
    await query.answer()
    
    date = query.data.split('_')[1]
    available_slots = stadium_bot.get_available_slots(date)
    
    if not available_slots:
        text = "❌ Afsuski, bu sanada bo'sh vaqt yo'q!"
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data=f"date_{date}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_text = date_obj.strftime('%d.%m.%Y')
    
    text = f"📝 **BRON QILISH**\n\n📅 Sana: {date_text}\n\n⏰ **Bo'sh vaqtlarni tanlang:**"
    
    keyboard = []
    for slot in available_slots:
        keyboard.append([InlineKeyboardButton(f"🕐 {slot}", callback_data=f"select_{date}_{slot}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data=f"date_{date}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def select_time_slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vaqt oralig'ini tanlash"""
    query = update.callback_query
    await query.answer()
    
    data_parts = query.data.split('_')
    date = data_parts[1]
    time_slot = data_parts[2]
    
    # Bron ma'lumotlarini context'ga saqlash
    context.user_data['booking_date'] = date
    context.user_data['booking_time'] = time_slot
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_text = date_obj.strftime('%d.%m.%Y')
    
    text = f"📝 **BRON TAFSILOTLARI**\n\n"
    text += f"📅 Sana: {date_text}\n"
    text += f"⏰ Vaqt: {time_slot}\n\n"
    text += f"💰 **Narx tanlang:**"
    
    keyboard = [
        [InlineKeyboardButton(f"2 soat - {stadium_bot.prices['2_hours']:,} so'm", 
                             callback_data="price_2_hours")],
        [InlineKeyboardButton(f"3 soat - {stadium_bot.prices['3_hours']:,} so'm", 
                             callback_data="price_3_hours")],
        [InlineKeyboardButton(f"To'liq kun - {stadium_bot.prices['full_day']:,} so'm", 
                             callback_data="price_full_day")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data=f"book_{date}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def select_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Narx tanlash va bron yakunlash"""
    query = update.callback_query
    await query.answer()
    
    price_type = query.data.split('_')[1] + '_' + query.data.split('_')[2]
    context.user_data['price_type'] = price_type
    
    date = context.user_data['booking_date']
    time_slot = context.user_data['booking_time']
    price = stadium_bot.prices[price_type]
    
    # Bron yaratish
    booking_id = stadium_bot.generate_booking_id()
    user = update.effective_user
    
    booking = Booking(
        id=booking_id,
        date=date,
        time_slot=time_slot,
        duration=int(price_type.split('_')[0]) if price_type != 'full_day' else 14,
        customer_name=f"{user.first_name} {user.last_name or ''}".strip(),
        customer_phone="",  # Telefon raqamini keyinroq so'raymiz
        customer_id=user.id,
        status="pending",
        created_at=datetime.now().isoformat()
    )
    
    stadium_bot.bookings[booking_id] = booking
    stadium_bot.save_bookings()
    
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_text = date_obj.strftime('%d.%m.%Y')
    
    # Mijozga xabar
    text = f"✅ **BRON SO'ROVI YUBORILDI!**\n\n"
    text += f"📋 Bron ID: `{booking_id}`\n"
    text += f"📅 Sana: {date_text}\n"
    text += f"⏰ Vaqt: {time_slot}\n"
    text += f"💰 Narx: {price:,} so'm\n\n"
    text += f"📞 **Telefon raqamingizni yuboring** (masalan: +998901234567)\n\n"
    text += f"⏳ Tasdiqlash uchun admin bilan bog'laniladi..."
    
    keyboard = [[InlineKeyboardButton("🏠 Bosh menyu", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    # Adminga xabar yuborish
    admin_text = f"🔔 **YANGI BRON SO'ROVI!**\n\n"
    admin_text += f"📋 ID: `{booking_id}`\n"
    admin_text += f"👤 Mijoz: {booking.customer_name}\n"
    admin_text += f"📅 Sana: {date_text}\n"
    admin_text += f"⏰ Vaqt: {time_slot}\n"
    admin_text += f"💰 Narx: {price:,} so'm\n"
    
    admin_keyboard = [
        [InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"confirm_{booking_id}"),
         InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{booking_id}")]
    ]
    admin_reply_markup = InlineKeyboardMarkup(admin_keyboard)
    
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            reply_markup=admin_reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Adminga xabar yuborishda xatolik: {e}")

async def handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefon raqamini qabul qilish"""
    if update.message and update.message.text:
        phone = update.message.text.strip()
        user_id = update.effective_user.id
        
        # Oxirgi bronni topish
        user_bookings = [b for b in stadium_bot.bookings.values() 
                        if b.customer_id == user_id and b.status == "pending" and not b.customer_phone]
        
        if user_bookings:
            booking = max(user_bookings, key=lambda x: x.created_at)
            booking.customer_phone = phone
            stadium_bot.save_bookings()
            
            await update.message.reply_text(
                f"✅ Telefon raqam saqlandi: {phone}\n\n"
                f"⏳ Adminning javobini kuting..."
            )

async def admin_confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin tomonidan bronni tasdiqlash"""
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != ADMIN_ID:
        await query.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    booking_id = query.data.split('_')[1]
    
    if booking_id in stadium_bot.bookings:
        booking = stadium_bot.bookings[booking_id]
        booking.status = "confirmed"
        stadium_bot.save_bookings()
        
        # Mijozga xabar
        try:
            date_obj = datetime.strptime(booking.date, '%Y-%m-%d')
            date_text = date_obj.strftime('%d.%m.%Y')
            
            customer_text = f"🎉 **BRON TASDIQLANDI!**\n\n"
            customer_text += f"📋 Bron ID: `{booking_id}`\n"
            customer_text += f"📅 Sana: {date_text}\n"
            customer_text += f"⏰ Vaqt: {booking.time_slot}\n"
            customer_text += f"💰 To'lov: {stadium_bot.prices['2_hours' if booking.duration == 2 else '3_hours' if booking.duration == 3 else 'full_day']:,} so'm\n\n"
            customer_text += f"📍 Manzil: Stadion manzili\n"
            customer_text += f"📞 Aloqa: +998 XX XXX XX XX"
            
            await context.bot.send_message(
                chat_id=booking.customer_id,
                text=customer_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Mijozga xabar yuborishda xatolik: {e}")
        
        # Adminiga tasdiqlash
        await query.edit_message_text(
            f"✅ Bron #{booking_id} tasdiqlandi!",
            parse_mode='Markdown'
        )
    else:
        await query.answer("❌ Bron topilmadi!", show_alert=True)

async def admin_reject_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin tomonidan bronni rad etish"""
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != ADMIN_ID:
        await query.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    booking_id = query.data.split('_')[1]
    
    if booking_id in stadium_bot.bookings:
        booking = stadium_bot.bookings[booking_id]
        booking.status = "cancelled"
        stadium_bot.save_bookings()
        
        # Mijozga xabar
        try:
            await context.bot.send_message(
                chat_id=booking.customer_id,
                text=f"❌ **BRON RAD ETILDI**\n\nBron ID: `{booking_id}`\n\nQo'shimcha ma'lumot uchun aloqa: +998 XX XXX XX XX",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Mijozga xabar yuborishda xatolik: {e}")
        
        await query.edit_message_text(f"❌ Bron #{booking_id} rad etildi!")
    else:
        await query.answer("❌ Bron topilmadi!", show_alert=True)

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bosh menyuga qaytish"""
    query = update.callback_query
    await query.answer()
    
    await start(update, context)

# Callback handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha callback querylarni boshqarish"""
    query = update.callback_query
    
    if query.data == "view_schedule":
        await view_schedule(update, context)
    elif query.data.startswith("date_"):
        await show_date_schedule(update, context)
    elif query.data.startswith("book_"):
        await book_stadium(update, context)
    elif query.data.startswith("select_"):
        await select_time_slot(update, context)
    elif query.data.startswith("price_"):
        await select_price(update, context)
    elif query.data.startswith("confirm_"):
        await admin_confirm_booking(update, context)
    elif query.data.startswith("reject_"):
        await admin_reject_booking(update, context)
    elif query.data == "back_to_main":
        await back_to_main(update, context)

def main():
    """Botni ishga tushirish"""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Bot tokenini kiriting!")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Telefon raqam uchun text handler
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone_number))
    
    print("🚀 Bot ishga tushdi!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()