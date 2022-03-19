import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from config import TOKEN, URL, URL2
import sqlite3


bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
    conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.from_user.last_name
    markup = types.ReplyKeyboardMarkup(True)
    keyboard1 = types.KeyboardButton(text='Втрати росії ☠️')
    keyboard2 = types.KeyboardButton(text='Втрати України 🇺🇦')
    keyboard3 = types.KeyboardButton(text='Відсоткова характеристика втрат росії 📊')
    markup.add(keyboard1, keyboard2)
    markup.add(keyboard3)
    bot.send_photo(chat_id, open('dlc.png', 'rb'), caption=f'<b>Привіт, {first_name} {last_name}</b> ✌️ \nЦей бот допоможе тобі дізнатися актуальну інформацію про бойові втрати та загальні статистичні тенденції\n\n<i>Інформація обробляється в режимі реального часу. Дані звіряються з офіційними джерелами, зокрема:\nminusrus.com\nmil.gov.ua\nminfin.com.ua\nfakty.com.ua\nRussia`s war on Ukraine: Military balance of power (European Parliament, March 2022)</i>\n\nЩоб розпочати перегляд оберіть відповідну кнопку 👇', parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
    chat_id = message.chat.id
    if message.chat.type == 'private':
        if message.text == 'Втрати росії ☠️':
            url = URL
            url2 = URL2
            response1 = requests.get(url, timeout=10)
            response2 = requests.get(url2, timeout=60)
            soup1 = BeautifulSoup(response1.text, "html.parser")
            soup2 = BeautifulSoup(response2.text, "html.parser")

            title = soup1.find("div", class_="main").find("div", class_="main__part").find("div", class_="title").get_text(strip=True)
            subtitle = soup1.find("div", class_="main").find("div", class_="main__part").find("div", class_="subtitle").get_text(strip=True)

            personnel_title = soup1.find("div", class_="card card_large").find("div", class_="card__title").get_text(strip=True)
            personnel_amount = soup1.find("div", class_="card card_large").find("div", class_="card__amount").find("span", class_="card__amount-total").get_text(strip=True)
            personnel_amount_added = soup1.find("div", class_="card card_large").find("div", class_="card__amount").find("span", class_="card__amount-progress").get_text(strip=True)



            killed_title = soup1.find("div", class_="card card_large").find("div", class_="amount-details").findAll("div", class_="amount-details__item")[0].findAll("span")[0].get_text(strip=True)
            killed_amount = soup1.find("div", class_="card card_large").find("div", class_="amount-details").findAll("div", class_="amount-details__item")[0].findAll("span")[1].get_text(strip=True)
            wounded_title = soup1.find("div", class_="card card_large").find("div", class_="amount-details").findAll("div", class_="amount-details__item")[1].findAll("span")[0].get_text(strip=True)
            wounded_amount = soup1.find("div", class_="card card_large").find("div", class_="amount-details").findAll("div", class_="amount-details__item")[1].findAll("span")[1].get_text(strip=True)
            prisoners_title = soup1.find("div", class_="card card_large").find("div", class_="amount-details").findAll("div", class_="amount-details__item")[2].findAll("span")[0].get_text(strip=True)
            prisoners_amount = soup1.find("div", class_="card card_large").find("div", class_="amount-details").findAll("div", class_="amount-details__item")[2].findAll("span")[1].get_text(strip=True)

            ################################################
            prisoners_amount = 562 # тимчасово

            personnel_amount = f'~58.162' # тимчасово

            afv = soup1.find("div", class_="card__container").findAll("div", class_="card__title")[0].get_text(strip=True)
            tanks = soup1.find("div", class_="card__container").findAll("div", class_="card__title")[1].get_text(strip=True)
            artillery = soup1.find("div", class_="card__container").findAll("div", class_="card__title")[2].get_text(strip=True)
            aircrafts = soup1.find("div", class_="card__container").findAll("div", class_="card__title")[3].get_text(strip=True)
            helicopters = soup1.find("div", class_="card__container").findAll("div", class_="card__title")[4].get_text(strip=True)
            mv = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[9].find("span", class_="no-war-statistic-item-text").get_text(strip=True)
            md = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[6].find("span", class_="no-war-statistic-item-text").get_text(strip=True)
            ci = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[11].find("span", class_="no-war-statistic-item-text").get_text(strip=True)
            bpla = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[12].find("span", class_="no-war-statistic-item-text").get_text(strip=True)
            mrl = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[5].find("span", class_="no-war-statistic-item-text").get_text(strip=True)
            warships = soup1.find("div", class_="card__container").findAll("div", class_="card__title")[5].get_text(strip=True)

            afv_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[0].get_text(strip=True)
            tanks_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[1].get_text(strip=True)
            artillery_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[2].get_text(strip=True)
            aircrafts_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[3].get_text(strip=True)
            md_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[6].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            mv_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[9].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            ci_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[11].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            bpla_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[12].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            mrl_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[5].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            helicopters_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[4].get_text(strip=True)
            warships_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[5].get_text(strip=True)

            rocket_title = 'Ракети'
            rocket_amount = 1080  # ракеты

            ### ДОПОВНЕННЯ ДО ВТРАТ
            # БМП/БТР-И
            try:
                afv_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[0].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                afv_amount_added = 0

            # ТАНКИ
            try:
                tanks_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[1].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                tanks_amount_added = 0

            # АРТИЛЕРІЯ
            try:
                artillery_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[2].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                artillery_amount_added = 0

            # ЛІТАКИ
            try:
                aircrafts_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[3].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                aircrafts_amount_added = 0

            # ГЕЛІКОПТЕРИ
            try:
                helicopters_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[4].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                helicopters_amount_added = 0

            # КОРАБЛІ ТА КАТЕРИ
            try:
                warships_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[5].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                warships_amount_added = 0

            # РСЗВ
            try:
                mrl_amount_added = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[5].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if mrl_amount_added == "":
                    mrl_amount_added = 0
            except AttributeError:
                mrl_amount_added = 0

            # ППО
            try:
                md_amount_added = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[6].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if md_amount_added == "":
                    md_amount_added = 0
            except AttributeError:
                md_amount_added = 0

            # АВТОМОБІЛЬНА ТЕХНІКА
            try:
                mv_amount_added = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[9].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if mv_amount_added == "":
                    mv_amount_added = 0
            except AttributeError:
                mv_amount_added = 0

            # ЦИСТЕРНИ
            try:
                ci_amount_added = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[11].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if ci_amount_added == "":
                    ci_amount_added = 0
            except AttributeError:
                ci_amount_added = 0

            # БПЛА ОТР
            try:
                bpla_amount_added = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[12].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if bpla_amount_added == "":
                    bpla_amount_added = 0
            except AttributeError:
                bpla_amount_added = 0



            v_od = int(afv_amount) + int(mrl_amount) + int(md_amount) + int(mv_amount) + int(ci_amount) + int(bpla_amount) + int(tanks_amount) + int(artillery_amount) + int(aircrafts_amount) + int(helicopters_amount) + int(warships_amount)
            all_components = f'{title}\n<i>{subtitle}</i>\n\n🪖 <b>{personnel_title}:</b> {personnel_amount} (<i>{personnel_amount_added}</i>)\n{killed_title}: {killed_amount}\n{wounded_title}: {wounded_amount}\n{prisoners_title}: {prisoners_amount}\n\n🚛 <b>Військова техніка: </b>~{v_od}\n{afv}: {afv_amount} (<i>{afv_amount_added}</i>)\n{tanks}: {tanks_amount} (<i>{tanks_amount_added}</i>)\n{artillery}: {artillery_amount} (<i>{artillery_amount_added}</i>)\n{aircrafts}: {aircrafts_amount} (<i>{aircrafts_amount_added}</i>)\n{helicopters}: {helicopters_amount} (<i>{helicopters_amount_added}</i>)\n{mrl}: {mrl_amount} (<i>{mrl_amount_added}</i>)\n{md}: {md_amount} (<i>{md_amount_added}</i>)\n{mv}: {mv_amount} (<i>{mv_amount_added}</i>)\n{ci}: {ci_amount} (<i>{ci_amount_added}</i>)\n{bpla}: {bpla_amount} (<i>{bpla_amount_added}</i>)\n{warships}: {warships_amount} (<i>{warships_amount_added}</i>)\n{rocket_title}: {rocket_amount} (<i>немає даних</i>)\n\n @zbvUA_bot – Загальні бойові втрати <a href="https://github.com/F1-bot/zbvUA/blob/main/Materials/red11902.png?raw=true"> 🇺🇦</a>'
            bot.send_message(chat_id, all_components, parse_mode='html')

        elif message.text == 'Відсоткова характеристика втрат росії 📊':
            url = URL
            url2 = URL2
            response1 = requests.get(url, timeout=10)
            response2 = requests.get(url2, timeout=60)
            soup1 = BeautifulSoup(response1.text, "html.parser")
            soup2 = BeautifulSoup(response2.text, "html.parser")

            title = soup1.find("div", class_="main").find("div", class_="main__part").find("div", class_="title").get_text(strip=True)

            count_wd = soup2.find("div", class_="war-statistic").find("div", class_="war-statistic-header").findAll("span")[1].get_text(strip=True)
            personnel_amount = soup1.find("div", class_="card card_large").find("div", class_="card__amount").find("span", class_="card__amount-total").get_text(strip=True)
            personnel_amount_added = soup1.find("div", class_="card card_large").find("div",class_="card__amount").find("span", class_="card__amount-progress").get_text(strip=True)

            personnel_amount = f'~58.162'  # тимчасово


            afv_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[0].get_text(strip=True)
            tanks_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[1].get_text(strip=True)
            artillery_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[2].get_text(strip=True)
            aircrafts_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[3].get_text(strip=True)
            md_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[6].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            mv_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[9].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            ci_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[11].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            bpla_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[12].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            mrl_amount = soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[5].find("span", class_="no-war-statistic-item-number").get_text(strip=True)
            helicopters_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[4].get_text(strip=True)
            warships_amount = soup1.find("div", class_="card__container").findAll("span", class_="card__amount-total")[5].get_text(strip=True)

            ### ДОПОВНЕННЯ ДО ВТРАТ
            # БМП/БТР-И
            try:
                afv_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[0].find(
                    "span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                afv_amount_added = 0

            # ТАНКИ
            try:
                tanks_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[1].find(
                    "span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                tanks_amount_added = 0

            # АРТИЛЕРІЯ
            try:
                artillery_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[
                    2].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                artillery_amount_added = 0

            # ЛІТАКИ
            try:
                aircrafts_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[
                    3].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                aircrafts_amount_added = 0

            # ГЕЛІКОПТЕРИ
            try:
                helicopters_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[
                    4].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                helicopters_amount_added = 0

            # КОРАБЛІ ТА КАТЕРИ
            try:
                warships_amount_added = soup1.find("div", class_="card__container").findAll("div", class_="card")[
                    5].find("span", class_="card__amount-progress").get_text(strip=True)
            except AttributeError:
                warships_amount_added = 0

            # РСЗВ
            try:
                mrl_amount_added = \
                soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[
                    5].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if mrl_amount_added == "":
                    mrl_amount_added = 0
            except AttributeError:
                mrl_amount_added = 0

            # ППО
            try:
                md_amount_added = \
                soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[
                    6].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if md_amount_added == "":
                    md_amount_added = 0
            except AttributeError:
                md_amount_added = 0

            # АВТОМОБІЛЬНА ТЕХНІКА
            try:
                mv_amount_added = \
                soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[
                    9].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if mv_amount_added == "":
                    mv_amount_added = 0
            except AttributeError:
                mv_amount_added = 0

            # ЦИСТЕРНИ
            try:
                ci_amount_added = \
                soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[
                    11].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if ci_amount_added == "":
                    ci_amount_added = 0
            except AttributeError:
                ci_amount_added = 0

            # БПЛА ОТР
            try:
                bpla_amount_added = \
                soup2.find("div", class_="no-war-statistic mobile").findAll("div", class_="no-war-statistic-item")[
                    12].find("span", class_="no-war-statistic-item-delta").get_text(strip=True)
                if bpla_amount_added == "":
                    bpla_amount_added = 0
            except AttributeError:
                bpla_amount_added = 0

            start_position_local = 140000
            position_local_description = 'призначеного для вторгнення'
            start_position_global = 900000
            position_global_description = 'загального складу збройних сил рф'

            q = personnel_amount.replace("~", "")
            b = personnel_amount_added.replace("~", "")

            stat1 = ((float(q) / start_position_local) * 100000)
            stat2 = ((float(q) / start_position_global) * 100000)

            stat1_td = ((float(b) / start_position_local) * 100)
            stat2_td = ((float(b) / start_position_global) * 100)
            afv_start_position_local = 2900
            tanks_start_position_local = 1200
            artillery_start_position_local = 1600
            aircrafts_start_position_local = 330
            helicopters_start_position_local = 240
            warships_start_position_local = 75

            afv_start_position_global = 13758
            tanks_start_position_global = 3300
            artillery_start_position_global = 5689
            aircrafts_start_position_global = 1379
            helicopters_start_position_global = 961
            warships_start_position_global = 519

            afv_stat1 = ((float(afv_amount) / afv_start_position_local) * 100)
            afv_stat2 = ((float(afv_amount) / afv_start_position_global) * 100)

            tanks_stat1 = ((float(tanks_amount) / tanks_start_position_local) * 100)
            tanks_stat2 = ((float(tanks_amount) / tanks_start_position_global) * 100)

            artillery_stat1 = ((float(artillery_amount) / artillery_start_position_local) * 100)
            artillery_stat2 = ((float(artillery_amount) / artillery_start_position_global) * 100)

            aircrafts_stat1 = ((float(aircrafts_amount) / aircrafts_start_position_local) * 100)
            aircrafts_stat2 = ((float(aircrafts_amount) / aircrafts_start_position_global) * 100)

            helicopters_stat1 = ((float(helicopters_amount) / helicopters_start_position_local) * 100)
            helicopters_stat2 = ((float(helicopters_amount) / helicopters_start_position_global) * 100)

            warships_stat1 = ((float(warships_amount) / warships_start_position_local) * 100)
            warships_stat2 = ((float(warships_amount) / warships_start_position_global) * 100)

            afv_stat1_td = ((float(afv_amount_added) / afv_start_position_local) * 100)
            afv_stat2_td = ((float(afv_amount_added) / afv_start_position_global) * 100)

            tanks_stat1_td = ((float(tanks_amount_added) / tanks_start_position_local) * 100)
            tanks_stat2_td = ((float(tanks_amount_added) / tanks_start_position_global) * 100)

            artillery_stat1_td = ((float(artillery_amount_added) / artillery_start_position_local) * 100)
            artillery_stat2_td = ((float(artillery_amount_added) / artillery_start_position_global) * 100)

            aircrafts_stat1_td = ((float(aircrafts_amount_added) / aircrafts_start_position_local) * 100)
            aircrafts_stat2_td = ((float(aircrafts_amount_added) / aircrafts_start_position_global) * 100)

            helicopters_stat1_td = ((float(helicopters_amount_added) / helicopters_start_position_local) * 100)
            helicopters_stat2_td = ((float(helicopters_amount_added) / helicopters_start_position_global) * 100)

            warships_stat1_td = ((float(warships_amount_added) / warships_start_position_local) * 100)
            warships_stat2_td = ((float(warships_amount_added) / warships_start_position_global) * 100)


            all_components_statistics = f'📊 <b>Відсоткова характеристика втрат росії ({title[16:]}):</b>\n\nОсобовий склад: \n<b>– {round(stat1, 2)}%</b> | від {position_local_description} (<i>{start_position_local} од.</i>)\n<b>– {round(stat2, 2)}%</b> | від {position_global_description} (<i>{start_position_global} од.</i>)\n<b>– {round(stat1_td, 2)}%</b> | добовий відсоток знищення від {position_local_description} (<i>{start_position_local} од.</i>)\n<b>– {round(stat2_td, 2)}%</b> | добовий відсоток знищення від {position_global_description} (<i>{start_position_global} од.</i>)\n\nБойові броньовані машини:\n<b>– {round(afv_stat1, 2)}%</b> | від {position_local_description} (<i>{afv_start_position_local} од.</i>)\n<b>– {round(afv_stat2, 2)}%</b> | від {position_global_description} (<i>{afv_start_position_global} од.</i>)\n<b>– {round(afv_stat1_td, 2)}%</b> | добовий відсоток знищення від {position_local_description} (<i>{afv_start_position_local} од.</i>)\n<b>– {round(afv_stat2_td, 2)}%</b> | добовий відсоток знищення від {position_global_description} (<i>{afv_start_position_global} од.</i>)\n\nТанки:\n<b>– {round(tanks_stat1, 2)}%</b> | від {position_local_description} (<i>{tanks_start_position_local} од.</i>)\n<b>– {round(tanks_stat2, 2)}%</b> | від {position_global_description} (<i>{tanks_start_position_global} од.</i>)\n<b>– {round(tanks_stat1_td, 2)}%</b> | добовий відсоток знищення від {position_local_description} (<i>{tanks_start_position_local} од.</i>)\n<b>– {round(tanks_stat2_td, 2)}%</b> | добовий відсоток знищення від {position_global_description} (<i>{tanks_start_position_global} од.</i>)\n\nАртилерія:\n<b>– {round(artillery_stat1, 2)}%</b> | від {position_local_description} (<i>{artillery_start_position_local} од.</i>)\n<b>– {round(artillery_stat2, 2)}%</b> | від {position_global_description} (<i>{artillery_start_position_global} од.</i>)\n<b>– {round(artillery_stat1_td, 2)}%</b> | добовий відсоток знищення від {position_local_description} (<i>{artillery_start_position_local} од.</i>)\n<b>– {round(artillery_stat2_td, 2)}%</b> | добовий відсоток знищення від {position_global_description} (<i>{artillery_start_position_global} од.</i>)\n\nЛітаки:\n<b>– {round(aircrafts_stat1, 2)}%</b> | від {position_local_description} (<i>{aircrafts_start_position_local} од.</i>)\n<b>– {round(aircrafts_stat2, 2)}%</b> | від {position_global_description} (<i>{aircrafts_start_position_global} од.</i>)\n<b>– {round(aircrafts_stat1_td, 2)}%</b> | добовий відсоток знищення від {position_local_description} (<i>{aircrafts_start_position_local} од.</i>)\n<b>– {round(aircrafts_stat2_td, 2)}%</b> | добовий відсоток знищення від {position_global_description} (<i>{aircrafts_start_position_global} од.</i>)\n\nГелікоптери:\n<b>– {round(helicopters_stat1, 2)}%</b> | від {position_local_description} (<i>{helicopters_start_position_local} од.</i>)\n<b>– {round(helicopters_stat2, 2)}%</b> | від {position_global_description} (<i>{helicopters_start_position_global} од.</i>)\n<b>– {round(helicopters_stat1_td, 2)}%</b> | добовий відсоток знищення від {position_local_description} (<i>{helicopters_start_position_local} од.</i>)\n<b>– {round(helicopters_stat2_td, 2)}%</b> | добовий відсоток знищення від {position_global_description} (<i>{helicopters_start_position_global} од.</i>)\n\nМорський флот:\n<b>– {round(warships_stat1, 2)}%</b> | від {position_local_description} (<i>{warships_start_position_local} од.</i>)\n<b>– {round(warships_stat2, 2)}%</b> | від {position_global_description} (<i>{warships_start_position_global} од.</i>)\n<b>– {round(warships_stat1_td, 2)}%</b> | добовий відсоток знищення від {position_local_description} (<i>{warships_start_position_local} од.</i>)\n<b>– {round(warships_stat2_td, 2)}%</b> | добовий відсоток знищення від {position_global_description} (<i>{warships_start_position_global} од.</i>)\n\nРСЗВ, Засоби ППО, Автомобільна техніка, цистерни, БпЛА ОТР: <i>Немає даних</i>\n\n @zbvUA_bot – Загальні бойові втрати <a href="https://github.com/F1-bot/zbvUA/blob/main/Materials/red31943.png?raw=true"> 🇺🇦</a>'

            bot.send_message(chat_id, all_components_statistics, parse_mode='html')

        elif message.text == 'Втрати України 🇺🇦':
            url = URL
            url2 = URL2
            response1 = requests.get(url, timeout=10)
            response2 = requests.get(url2, timeout=60)
            soup1 = BeautifulSoup(response1.text, "html.parser")
            soup2 = BeautifulSoup(response2.text, "html.parser")
            count_wd = soup2.find("div", class_="war-statistic").find("div", class_="war-statistic-header").findAll("span")[1].get_text(strip=True)
            dead_ch = soup2.find("div", class_="war-statistic").findAll("div", class_="war-statistic-item")[0].find("div", class_="war-statistic-item-data").find("span", class_="war-statistic-item-number").get_text(strip=True)
            wounded_ch = soup2.find("div", class_="war-statistic").findAll("div", class_="war-statistic-item")[1].find("div", class_="war-statistic-item-data").find("span", class_="war-statistic-item-number").get_text(strip=True)
            title = soup1.find("div", class_="main").find("div", class_="main__part").find("div", class_="title").get_text(strip=True)

            ua_info = f'Втрати України станом на {title[16:]} \n<i>Орієнтовна оцінка ЗСУ з 24.02.2022</i>\n\n👨‍✈️ <b>Особовий склад:</b> ~1.300 (<i>12.03.2022</i>)\n\n👨‍👩‍👧‍👦 <b>Цивільні втрати:</b>\nВбиті мирні громадяни: >3.000 (<i>17.03.2022</i>)\nВбиті діти: ~{dead_ch} (<i>{title[16:]}</i>)\nПоранені діти: {wounded_ch} (<i>{title[16:]}</i>)\n\nІнша інформація, з міркувань безпеки, - не обробляється!\n\nСлава Героям України!\nНіколи не пробачимо!\n\n @zbvUA_bot – Загальні бойові втрати <a href="https://github.com/F1-bot/zbvUA/blob/main/Materials/red21903.png?raw=true"> 🇺🇦</a>'
            bot.send_message(chat_id, ua_info, parse_mode='html')
        else:
            not_found = f'<b>Здається Ви заблукали</b> 🤔'
            bot.send_message(chat_id, not_found, parse_mode='html')



bot.polling(none_stop=True)