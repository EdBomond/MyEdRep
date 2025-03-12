import base64
import quopri
from email.header import decode_header
from bs4 import BeautifulSoup
from datetime import datetime
import asyncio
import re
import config
from webdav3.client import Client
from pathlib import Path
from cryptocode import decrypt
import telebot
import os


def from_subj_decode(msg_from_subj):
    if msg_from_subj:
        encoding = decode_header(msg_from_subj)[0][1]
        msg_from_subj = decode_header(msg_from_subj)[0][0]
        if isinstance(msg_from_subj, bytes):
            msg_from_subj = msg_from_subj.decode(encoding)
        if isinstance(msg_from_subj, str):
            pass
        msg_from_subj = str(msg_from_subj).strip("<>").replace("<", "")
        return msg_from_subj
    else:
        return None
def get_letter_text_from_html(body):
    body = body.replace("<div><div>", "<div>").replace("</div></div>", "</div>")
    try:
        soup = BeautifulSoup(body, "html.parser")
        paragraphs = soup.find_all("div")
        text = ""
        for paragraph in paragraphs:
            text += paragraph.text + "\n"
        return text.replace("\xa0", " ")
    except (Exception) as exp:
        print("text ftom html err ", exp)
        return False
def letter_type(part):
    if part["Content-Transfer-Encoding"] in (None, "7bit", "8bit", "binary"):
        return part.get_payload()
    elif part["Content-Transfer-Encoding"] == "base64":
        encoding = part.get_content_charset()
        return base64.b64decode(part.get_payload()).decode(encoding)
    elif part["Content-Transfer-Encoding"] == "quoted-printable":
        encoding = part.get_content_charset()
        return quopri.decodestring(part.get_payload()).decode(encoding)
    else:  # all possible types: quoted-printable, base64, 7bit, 8bit, and binary
        return part.get_payload()

def get_letter_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            count = 0
            if part.get_content_maintype() == "text" and count == 0:
                extract_part = letter_type(part)
                if part.get_content_subtype() == "html":
                    letter_text = get_letter_text_from_html(extract_part)
                else:
                    letter_text = extract_part.rstrip().lstrip()
                count += 1
                return (
                    letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")
                )
    else:
        count = 0
        if msg.get_content_maintype() == "text" and count == 0:
            extract_part = letter_type(msg)
            if msg.get_content_subtype() == "html":
                letter_text = get_letter_text_from_html(extract_part)
            else:
                letter_text = extract_part
            count += 1
            return letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")
def get_attachments(msg):
    attachments = list()
    for part in msg.walk():
        if (
            part["Content-Type"]
            and "name" in part["Content-Type"]
            and part.get_content_disposition() == "attachment"
        ):
            str_pl = part["Content-Type"]
            str_pl = encode_att_names(str_pl)
            attachments.append(str_pl)
    return attachments
def post_construct(msg_subj, msg_from, msg_email, letter_text, attachments):
    att_txt = "\n".join(attachments)
    postparts = [
        "\U0001F4E8 <b>",
        str(msg_subj),
        "</b>\n\n",
        "<pre>",
        str(msg_from),
        "\n",
        msg_email,
        "</pre>\n\n",
        letter_text,
        "\n\n",
        "\U0001F4CE<i> вложения: </i>",
        str(len(attachments)),
        "\n\n",
        att_txt,
    ]
    txt = "".join(postparts)
    return txt

def date_parse(msg_date):
    if not msg_date:
        return datetime.now()
    else:
        dt_obj = "".join(str(msg_date[:6]))
        dt_obj = dt_obj.strip("'(),")
        dt_obj = datetime.strptime(dt_obj, "%Y, %m, %d, %H, %M, %S")
        return dt_obj
def encode_att_names(str_pl):
    enode_name = re.findall("\=\?.*?\?\=", str_pl)
    if len(enode_name) == 1:
        encoding = decode_header(enode_name[0])[0][1]
        decode_name = decode_header(enode_name[0])[0][0]
        decode_name = decode_name.decode(encoding)
        str_pl = str_pl.replace(enode_name[0], decode_name)
    if len(enode_name) > 1:
        nm = ""
        for part in enode_name:
            encoding = decode_header(part)[0][1]
            decode_name = decode_header(part)[0][0]
            decode_name = decode_name.decode(encoding)
            nm += decode_name
        str_pl = str_pl.replace(enode_name[0], nm)
        for c, i in enumerate(enode_name):
            if c > 0:
                str_pl = str_pl.replace(enode_name[c], "").replace('"', "").rstrip()
    return str_pl

def send_attach(msg, msg_subj, repl, IMEI, client, msg_date, bot, chatid, msg_datetelegramm, IMEI_name, download_folder) -> bool:
    try:
        for part in msg.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                filename = from_subj_decode(filename)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    send_document(
                        part.get_payload(decode=True), filename, IMEI, client, msg_date, bot, chatid, msg_datetelegramm, IMEI_name, download_folder
                    )
                )
                # удалим файл с диска
                download_path = f"{download_folder}/{msg_date}_{filename}"
                try:
                   os.remove(download_path)
                   print("% s removed successfully" % download_path)
                except OSError as error:
                   print(error)
                   print(f"File {download_path} can not be removed")
        return True
    except Exception:
        print(f"Не выгрузили приложения! {IMEI}-{IMEI_name} {msg_datetelegramm}")
        # пометить письмо как непрочитанное
        return False
async def send_document(document, filename, IMEI, client, msg_date, bot, chatid, msg_datetelegramm, IMEI_name,download_folder):
        download_path = f"{download_folder}/{msg_date}_{filename}"
        #print(download_path)
        #print(document)
        with open(download_path, "wb") as fp:
            fp.write(document)

        if not client.check(f"{IMEI}-{IMEI_name}"):
            client.mkdir(f"{IMEI}-{IMEI_name}")
            print(f"Создана папка {IMEI}-{IMEI_name} в облаке")
        #my_files = client.list()
        #print(my_files)
        #client.upload_sync(remote_path=f"backup/{new_folder}_{date}", local_path=sys.argv[1])

        #client.upload_sync(f"{IMEI}/", f"{config.download_folder}/{filename}")
        #print(f"{config.download_folder}/{filename}")
        client.upload_sync(f"//{IMEI}-{IMEI_name}/{msg_date}_{filename}", f"{download_folder}/{msg_date}_{filename}")
        print(f"Выгружен файл {msg_date}_{filename} в облако в папку {IMEI}-{IMEI_name}")
        #text = f"Пришло письмо с устройства IMEI: {IMEI}-{IMEI_name} {msg_datetelegramm}"
        #bot.send_message(chatid, text)
        #print(f"Направили текст в чат {chatid} телеграмма")
        img = open(download_path, 'rb')
        print(f"Открыли фотографию {download_path}")
        #bot.send_photo(chatid, img)
        print(f"Отправили фотографию {download_path} в чат телеграмма")
        fp.close()

def check_setting() -> bool:
    """
    Проверка существования файла настроек.
    """
    if not Path('setting.ini').exists():
        return False
    return True

def authorize(psw: str) -> (Client, bool):
    """
    Авторизация в облаке. Декодирование логина и пароля.
    Создание клиента с авторизацией.
    Возвращение клиента из функции для использования в других функциях.
    """
    datas = [x.strip() for x in open('setting.ini', 'r', encoding='utf-8') if x.strip()]
    login = decrypt_word(datas[0], psw)
    password = decrypt_word(datas[1], psw)
    if login:
        data = {
            'webdav_hostname': f"{config.webdav_hostname}",
            'webdav_login': f"{config.username}",
            'webdav_password': f"{config.mail_pass}"
        }

        client = Client(data)
        return client
    return False

def decrypt_word(word: str, psw: str) -> str:
    """
    Дешифрование слова, переданного в функцию.
    """
    return decrypt(word, psw)

def check_setting() -> bool:
    """
    Проверка существования файла настроек.
    """
    if not Path('setting.ini').exists():
        return False
    return True

def read_setting():
    setting={} #codecs.open('file.txt', encoding='utf-8')
    with open("setting.ini", encoding='utf-8') as file:
        for line in file:
            var , val = line.strip().split("=")
            setting[f"{var.strip()}"]=f"{val.strip()}"
    return setting

def create_telegram(token)->telebot:
    bot = telebot.TeleBot(token)
    return bot