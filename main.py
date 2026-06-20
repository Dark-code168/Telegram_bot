# ================= BANNERS =================

START_BANNER = "banner_start.jpg"
BUY_BANNER = "banner_buy.jpg"
FAQ_BANNER = "banner_faq.jpg"
ПРОФИЛЬ_BANNER = "banner_profile.jpg"
import telebot
import requests
import threading
import time

from telebot.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


BOT_TOKEN = "8784582458:AAG3k2HGu_Fd6R7vxGVnBdi_QulakXNVpL0"
CRYPTO_TOKEN = "597744:AA6uxATzvqg67nJ6Zj5nXZy50KkvhqoRoAh"
MENU_BANNER = "banner_start.jpg"
PREMIUM_ID = "5442702885"


AI_LINK = "https://app.leonardo.ai/"


bot = telebot.TeleBot(BOT_TOKEN)


invoices = {}
activated = set()


# ================= MENU =================

def panel():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("ПРИОБРЕСТИ ELITE AI")
    kb.add("ПРОФИЛЬ", "F.A.Q")

    return kb


# ================= START =================

@bot.message_handler(commands=["start"])
def start(message):
    with open(START_BANNER, "rb") as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption="🏆 Добро пожаловать! в Главное меню 🏆",
            reply_markup=panel()
        )

# ================= CREATE INVOICE =================

def create_invoice(amount, user_id):

    url = "https://pay.crypt.bot/api/createInvoice"

    headers = {
        "Crypto-Pay-API-Token": CRYPTO_TOKEN
    }

    data = {
        "asset": "USDT",
        "amount": float(amount),
        "description": "ELITE AI",
        "payload": str(user_id)
    }


    r = requests.post(
        url,
        headers=headers,
        json=data
    )


    res = r.json()

    print("CREATE:", res)


    if res.get("ok"):
        return res["result"]


    return None



# ================= CHECK =================

def check_invoice(invoice_id):

    url = "https://pay.crypt.bot/api/getInvoices"


    headers = {
        "Crypto-Pay-API-Token": CRYPTO_TOKEN
    }


    params = {
        "invoice_ids": invoice_id
    }


    r = requests.get(
        url,
        headers=headers,
        params=params
    )


    res = r.json()


    print("CHECK:", res)


    if res.get("ok"):

        items = res["result"]["items"]


        if items:
            return items[0]["status"]


    return None



# ================= CHECKER =================

def checker():

    while True:

        try:

            time.sleep(5)


            for user_id in list(invoices):

                invoice_id = invoices[user_id]


                status = check_invoice(invoice_id)


                print(
                    "STATUS:",
                    status
                )


                if status == "paid":


                    if user_id not in activated:

                        activated.add(user_id)


                        kb = InlineKeyboardMarkup()


                        kb.add(
                            InlineKeyboardButton(
                                "🔓 НЕЙРОНКА",
                                url=AI_LINK
                            )
                        )


                        bot.send_message(
                            user_id,
                            "Оплата подтверждена ✅\nВаш доступ:",
                            reply_markup=kb
                        )


                    del invoices[user_id]



        except Exception as e:

            print(
                "CHECKER ERROR:",
                e
            )



threading.Thread(
    target=checker,
    daemon=True
).start()



# ================= TEXT =================

@bot.message_handler(content_types=["text"])
def handler(message):


    text = message.text
    user_id = message.from_user.id



    # BUY

    if text == "ПРИОБРЕСТИ ELITE AI":


        kb = ReplyKeyboardMarkup(
            resize_keyboard=True
        )


        kb.add(
            "0.5$",
            "2.49$"
        )

        kb.add(
            "4.99$"
        )

        kb.add(
            "⬅️ Назад"
        )


        bot.send_message(
            message.chat.id,
            "Выберите тариф",
            reply_markup=kb
        )



    # ONLY 0.5

    elif text == "0.5$":


        if user_id in activated:

            bot.send_message(
                message.chat.id,
                "У вас уже есть доступ ✅"
            )

            return



        invoice = create_invoice(
            "0.5",
            user_id
        )


        if invoice:


            invoices[user_id] = invoice["invoice_id"]


            kb = InlineKeyboardMarkup()
            kb.add(
                InlineKeyboardButton(
                    "💳 ОПЛАТИТЬ СЧЁТ",
                    url=invoice["pay_url"]
                )
            )

            # Если фото находится на вашем компьютере/сервере:
            with open('banner_buy.jpg', 'rb') as photo:
                bot.send_photo(
                    message.chat.id,
                    photo=photo,
                    caption="Счёт 0.5$ создан",
                    reply_markup=kb
                )



    elif text in ["2.49$", "4.99$"]:


        bot.send_message(
            message.chat.id,
            "Этот тариф пока в разработке ⚙️",
            reply_markup=panel()
        )



    # FAQ

        # FAQ
    elif text == "F.A.Q":


        with open('banner_faq.jpg', 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo=photo,
                caption="⚜️ 1. Что мы предлагаем? Доступ к актуальным AI-инструментам в одном месте."
                        "\n\n ⚜️ 2. Почему выбрать нас? Мы собираем лучшие нейросети и удобный доступ без лишних сложностей. "
                        "\n\n ⚜️️3. Какие нейросети доступны? Только актуальные инструменты для текста, изображений, идей и работы."
                        "\n\n ⚜️4. Это обычные нейросети? Нет. Мы отбираем решения, которые реально дают результат."
                        "\n\n ⚜️5. Для кого этот доступ? Для дизайнеров, создателей контента, предпринимателей и всех, кто работает с AI."
                        "\n\n ⚜️6. Зачем покупать доступ? Чтобы экономить время и использовать мощные инструменты в одном месте."
                        "\n\n ⚜️7. Будут ли обновления? Да. База развивается и пополняется новыми возможностями."
                        "\n\n ⚜️8. Это сложно использовать? Нет. Всё сделано максимально просто и понятно."
                        "\n\n ⚜️9. Можно ли использовать для работы? Да. AI помогает ускорять задачи и создавать больше."
                        "\n\n ⚜️10. Почему именно сейчас? AI развивается каждый день. Ранний доступ даёт преимущество.",
                reply_markup=panel()
            )







    # PROFILE

        # # PROFILE
    elif text == "ПРОФИЛЬ":

        u = message.from_user
        with open('banner_profile.jpg', 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo=photo,
                caption=f" 👤ВАШ ПРОФИЛЬ!\n\n📟ID: {u.id}\n\n🎫User: @{u.username}",
                reply_markup=panel()
            )


    elif text == "⬅️ Назад":


        bot.send_message(
            message.chat.id,
            "Главное меню",
            reply_markup=panel()
        )



print("BOT STARTED")

bot.infinity_polling()