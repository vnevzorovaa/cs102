import datetime
import json
import urllib.error
import urllib.request
from datetime import datetime, timedelta  # type: ignore

import gspread  # type: ignore
import pandas as pd  # type: ignore
import telebot  # type: ignore
from dateutil.parser import parse  # type: ignore
from google.oauth2.gdch_credentials import ServiceAccountCredentials

bot = telebot.TeleBot("6007313686:AAGmqO01oyg2E1CyFfTKMONrx__6udFs4Lk")


def is_valid_date(date: str = "01/01/00", delimiter: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата  не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    """Конвертируем дату из строки в datetime"""
    # Получаем текущую дату
    current_date = datetime.now().date()

    # Проверяем что дан правильный (хотя бы на 50% делимитер)
    if not delimiter in date:
        return False

    try:
        deadline_date = convert_date(date).date()
    except ValueError:
        return False

    # Проверяем, что дата не может быть до текущей
    if deadline_date < current_date:
        print("Дедлайн уже прошел")
        return False

    # Проверяем, что дата не может быть позже, чем через год
    if deadline_date > current_date + timedelta(days=365):
        print("Дедлайн должен быть меньше чем через год")
        return False

    # Возвращаем True, если дата прошла все проверки
    return True


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    try:
        request = urllib.request.urlopen(url)
        if request.getcode() == 200:
            return True
    except (ValueError, urllib.error.URLError):
        pass
    return False


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    try:
        # Пробуем распарсить дату с помощью функции parse
        datetime_obj = parse(date)
    except ValueError:
        # Если не удалось распарсить, бросаем исключение
        raise ValueError("Некорректный формат даты")
    return datetime_obj


def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    sheet_id = "1kfiBPneblVX0hKnPkJllA1TLiAJwEjw3nZ85EgCbHdQ"
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    df = pd.DataFrame(worksheet.get_values(""), columns=worksheet.row_values(1))
    df = df.drop(0)
    df.index -= 1
    return worksheet, tables[max(tables)]["url"], df


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        connect_table(message)
    elif message.text == "Редактировать предметы":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить")
        start_markup.row("Редактировать")
        start_markup.row("Удалить одно")
        start_markup.row("Удалить ВСЕ")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)
    elif message.text == "Редактировать дедлайны":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить дату")
        start_markup.row("Изменить дату")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_deadline_action)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        today = datetime.today()
        week = today + timedelta(days=7)
        a, b, df = access_current_sheet()
        mes = f""
        for i in range(2, len(a.col_values(1)) + 1):
            for ddl in a.row_values(i)[2:]:
                if convert_date(ddl) <= week and convert_date(ddl) >= today:
                    mes += f"{a.cell(i, 1).value}: {ddl}\n"
        bot.send_message(message.chat.id, mes)
        start(message)


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Добавить":
        message = bot.send_message(message.chat.id, "Напишите название и ссылку через пробел")
        bot.register_next_step_handler(message, add_new_subject)
    elif message.text == "Редактировать":
        a, b, c = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in c.subject:
            mrkp.row(f"{el}")
        inf = bot.send_message(message.chat.id, "Какой предмет редактируем?", reply_markup=mrkp)
        bot.register_next_step_handler(inf, update_subject)
    elif message.text == "Удалить одно":
        a, b, c = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in c.subject:
            mrkp.row(f"{el}")
        inf = bot.send_message(message.chat.id, "Какой предмет удаляем?", reply_markup=mrkp)
        bot.register_next_step_handler(inf, delete_subject)
    elif message.text == "Удалить ВСЕ":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Да")
        start_markup.row("Нет")
        start_markup.row("Не знаю")
        info = bot.send_message(message.chat.id, "Вы точно хотите удалить ВСЕ?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_removal_option)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    if message.text == "Добавить дату":
        a, b, c = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in c.subject:
            mrkp.row(f"{el}")
        inf = bot.send_message(message.chat.id, "Какому предмету добавляем?", reply_markup=mrkp)
        bot.register_next_step_handler(inf, add_subject_deadline)
    elif message.text == "Изменить дату":
        a, b, c = access_current_sheet()
        mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in c.subject:
            mrkp.row(f"{el}")
        inf = bot.send_message(message.chat.id, "Для какого предмета изменяем?", reply_markup=mrkp)
        bot.register_next_step_handler(inf, update_subject_deadline)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    global magic_box
    magic_box = []
    magic_box.append(message.text)
    inf = bot.send_message(message.chat.id, "Введите время в формате 'dd.mm.yyyy'")
    bot.register_next_step_handler(inf, add_subject_deadline2)


def add_subject_deadline(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    global magic_box
    magic_box = []
    magic_box.append(message.text)
    inf = bot.send_message(message.chat.id, "Введите дату и ее разделитель")
    bot.register_next_step_handler(inf, add_subject_deadline2)


def add_subject_deadline2(message):
    global magic_box
    spt = message.text.split()
    if len(spt) == 1:
        date, delimiter = spt[0], "/"
    else:
        date, delimiter = spt[0], spt[1]
    if not is_valid_date(date, delimiter):
        inf = bot.send_message(message.chat.id, "Неправильно введена дата")
        bot.register_next_step_handler(inf, add_subject_deadline2)
    else:
        a, b, c = access_current_sheet()
        row = a.find(f"{magic_box[0]}").row
        n = len(a.row_values(row))
        a.update_cell(row, n + 1, date)
        if not a.cell(1, n + 1).value:
            num = int(a.cell(1, n).value)
            a.update_cell(1, n + 1, num + 1)
        bot.send_message(message.chat.id, "Изменено!")
        start(message)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    if message.text == "Да":
        clear_subject_list(message)
    elif message.text == "Нет":
        start(message)
    elif message.text == "Не знаю":
        start(message)
        bot.send_message(message.chat.id, "Определись!!")


def update_subject(message):  # type: ignore
    """Обновляем информацию о предмете в Google-таблице"""
    global magic_box
    magic_box = []
    magic_box.append(message.text)
    inf = bot.send_message(
        message.chat.id,
        "Введите новую информацию в формате 'название ссылка'. Если что-то из этого не должно измениться напишите его без изменений",
    )
    bot.register_next_step_handler(inf, update_subject2)


def update_subject2(message):  # type: ignore
    global magic_box
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        worksheet, b, df = access_current_sheet()
        ind = df.loc[df.isin(magic_box).any(axis=1)].index[0] + 2
        cell_list = worksheet.range(f"A{ind}:B{ind}")
        cell_list[0].value = name
        cell_list[1].value = url
        worksheet.update_cells(cell_list)
        bot.send_message(message.chat.id, "Изменено!")
    except IndexError:
        inf = bot.send_message(
            message.chat.id, "Название и ссылка должны быть в одном сообщении и разделены пробелом!!"
        )
        bot.register_next_step_handler(inf, update_subject2)
    start(message)


def update_subject_deadline(message):
    """Обновляем дедлайн"""
    global magic_box
    magic_box = []
    magic_box.append(message.text)
    a, b, c = access_current_sheet()
    mrkp = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for el in c.columns[2:]:
        mrkp.row(f"{el}")
    inf = bot.send_message(message.chat.id, "Для какой лабы изменяем?", reply_markup=mrkp)
    bot.register_next_step_handler(inf, update_subject_deadline2)


def update_subject_deadline2(message):
    global magic_box
    magic_box.append(message.text)
    inf = bot.send_message(message.chat.id, "Введите дату и разделитель для нее через пробел")
    bot.register_next_step_handler(inf, update_subject_deadline3)


def update_subject_deadline3(message):
    global magic_box
    spt = message.text.split()
    if len(spt) == 1:
        date, delimiter = spt[0], "/"
    else:
        date, delimiter = spt[0], spt[1]
    if not is_valid_date(date, delimiter):
        inf = bot.send_message(message.chat.id, "Неправильно введена дата")
        bot.register_next_step_handler(inf, add_subject_deadline2)
    else:
        a, b, c = access_current_sheet()
        row = a.find(f"{magic_box[0]}").row
        col = a.find(f"{magic_box[1]}").col
        a.update_cell(row, col, date)
        bot.send_message(message.chat.id, "Изменено!")
        start(message)


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        worksheet, b, c = access_current_sheet()
        worksheet.append_row([name, url])
        bot.send_message(message.chat.id, "Добавлено!")
        start(message)
    except IndexError:
        inf = bot.send_message(
            message.chat.id, "Название и ссылка должны быть в одном сообщении и разделены пробелом!!"
        )
        bot.register_next_step_handler(inf, add_new_subject)


def add_new_subject_url(message):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    # Set up the Google Sheets API client
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)  # тут убрала Google-
    client = gspread.authorize(credentials)

    # Open the subject table spreadsheet
    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit")
    worksheet = spreadsheet.worksheet("Subjects")

    # Parse the message to extract the subject and URL
    parts = message.split()
    subject = parts[0]
    url = parts[1]

    # Find the row for the subject and update the URL
    cell_list = worksheet.findall(subject)
    if len(cell_list) == 1:
        cell = cell_list[0]
        row = cell.row
        worksheet.update_cell(row, 2, url)
    else:
        # Handle the case where the subject is not found
        print("Subject not found")


def update_subject(message):  # type: ignore
    """Обновляем информацию о предмете в Google-таблице"""
    global magic_box
    magic_box = []
    magic_box.append(message.text)
    inf = bot.send_message(
        message.chat.id,
        "Введите новую информацию в формате '{название} {ссылка}'. Если что-то из этого не должно измениться напишите его без изменений",
    )
    bot.register_next_step_handler(inf, update_subject2)


def update_subject2(message):  # type: ignore
    global magic_box
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        worksheet, b, df = access_current_sheet()
        ind = df.loc[df.isin(magic_box).any(axis=1)].index[0] + 2
        cell_list = worksheet.range(f"A{ind}:B{ind}")
        cell_list[0].value = name
        cell_list[1].value = url
        worksheet.update_cells(cell_list)
        bot.send_message(message.chat.id, "Изменено!")
    except IndexError:
        inf = bot.send_message(
            message.chat.id, "Название и ссылка должны быть в одном сообщении и разделены пробелом!!"
        )
        bot.register_next_step_handler(inf, update_subject2)
    start(message)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    worksheet, b, df = access_current_sheet()
    ind = df.loc[df.isin([message.text]).any(axis=1)].index[0] + 2
    worksheet.delete_rows(int(ind), int(ind))
    bot.send_message(message.chat.id, "Удалено!")
    start(message)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)
    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    sh.del_worksheet(worksheet)
    start(message)


def check_table():
    global check
    try:
        file = open("tables.json")
        check = True
    except FileNotFoundError:
        check = False


@bot.message_handler(commands=["start"])
def start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row("Подключить Google-таблицу")
    start_markup.row("Посмотреть дедлайны на этой неделе")
    start_markup.row("Внести новый дедлайн")
    start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


if __name__ == "__main__":
    bot.infinity_polling()
