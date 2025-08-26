import imaplib
import email
import traceback
from email.header import decode_header
import config
import function
import traceback
from webdav3.client import Client
from datetime import datetime, timedelta
import datetime
import os

ENCODING = config.encoding

mail_pass = config.mail_pass
username = config.username
imap_server = config.imap_server
download_folder=config.download_folder
webdav_hostname=config.webdav_hostname
send_attach = config.send_attach #пересылка вложений, чтобы отключить нужен параметр False
encoding=config.encoding
repl=config.repl  # сохранять файлы из писем
fromadr=config.fromadr
tokenbot=config.tokenbot
chatid=config.chatid
IMEIS=config.IMEIS
try:
    if not function.check_setting():
       print("Отсутсвует файл настроек setting.ini!")
       exit()
    setting=function.read_setting()
    #print(setting)
    for var, val in setting.items():
        #print(f"var: {var}, val: {val}")
        if var=="mail_pass":
            mail_pass=val
        if var=="username":
            username=val
        if var=="imap_server":
            imap_server=val
        if var=="download_folder":
            download_folder = val
        if var=="webdav_hostname":
            webdav_hostname=val
        if var=="send_attach":
            send_attach=val
        if var=="encoding":
            encoding=val
        if var=="repl":
            repl=val
        if var=="fromadr":
            fromadr=val
        if var=="tokenbot":
            tokenbot=val
        if var=="chatid":
            chatid=val
        if var=="IMEIS":
            IMEIS_str=val
            list_ITEM = IMEIS_str.split(",")
            IMEIS.clear()
            IMEIS_name=[]
            IMEIS_chatid=[]
            for item in list_ITEM:
                item_num=item.split(":")[0]
                item_name = item.split(":")[1]
                item_chatid = item.split(":")[2]
                if (item_chatid==""):
                    item_chatid = chatid
                print(f"{item_name} {item_chatid}")
                IMEIS.append(f"{item_num}")
                IMEIS_name.append(f"{item_name}")
                IMEIS_chatid.append(f"{item_chatid}")
    print("Проверка устройств:")
    for IMEI_item in IMEIS:
        print(f"IMEI: {IMEI_item}")
    imap = imaplib.IMAP4_SSL(imap_server)
    print(f"Подключились к серверу mail.ru: {imap}")
    ok=imap.login(username, mail_pass)
    if ok=="OK":
      print(f"Подключились к серверу mail.ru логином: {username}")
    data = {
            'webdav_hostname': f"{webdav_hostname}",
            'webdav_login': f"{username}",
            'webdav_password': f"{mail_pass}"
            }
    client = Client(data)
    print(f"Подключились к облаку: {client}")
    # подключаем телеграммбота
    bot = function.create_telegram(tokenbot)
    print(bot)
    if (not bot):
        print("Отсутсвует соединение с телеграмм!")
        exit()
    #chatid = '-1002055707690'

    #bot.polling()
except (Exception) as exp:
    text = str("ошибка: " + str(exp))
    print(traceback.format_exc())
    print("Нет соединения с почтой!")
    exit(0)

imap.select("INBOX")
#result, data = imap.uid('search', "UNSEEN", "ALL")
#result, data = imap.uid('search', None, 'ALL')

date = (datetime.date.today() - datetime.timedelta(0)).strftime("%d-%b-%Y")
result, data = imap.uid('search', None, '(SENTSINCE {date})'.format(date=date))
print(result)
print(data)

unseen_msg = data[0].decode(ENCODING).split(" ")
if unseen_msg[0]:
    print(f"Найдено писем: {len(unseen_msg)}")
    for letter in unseen_msg: ###############################################
       #print(letter)
       #latest_email_uid = data[0].split()[-1]
       res, msg  = imap.uid('fetch', letter, '(RFC822)')
       if res == "OK":
            msg = email.message_from_bytes(msg[0][1])
            msg_date = function.date_parse(email.utils.parsedate_tz(msg["Date"]))
            msg_date = msg_date + timedelta(hours=2)
            msg_datestr=msg_date.strftime("%d%m%Y_%H_%M_%S")
            msg_datetelegramm=msg_date.strftime("%d.%m.%Y %H:%M:%S")
            msg_from = function.from_subj_decode(msg["From"])
            msg_subj = function.from_subj_decode(msg["Subject"])
            if msg["Message-ID"]:
                msg_id = msg["Message-ID"].lstrip("<").rstrip(">")
            else:
                msg_id = msg["Received"]
            if msg["Return-path"]:
                msg_email = msg["Return-path"].lstrip("<").rstrip(">")
            else:
                msg_email = msg_from

            if not msg_email:
                encoding = decode_header(msg["From"])[0][1]  # не проверено
                msg_email = (
                    decode_header(msg["From"])[1][0]
                    .decode(encoding)
                    .replace("<", "")
                    .replace(">", "")
                    .replace(" ", "")
                )

            letter_text = function.get_letter_text(msg)
            #print(letter_text)
            values = letter_text.split('\n')
            #print(values)
            batery="-"
            for value in values:
                var , val = value.strip().split(":")
                print(f"{var} {val}")
                if var=="Battery":
                   batery=f"Батарея {val}"
            print(batery)       
            attachments = function.get_attachments(msg)
            post_text = function.post_construct(
                        msg_subj, msg_from, msg_email, letter_text, attachments)
            IMEI=""
            i=0
            for IMEI_item in IMEIS:
                #print(IMEI_item)
                if IMEI_item in post_text:
                    IMEI=IMEI_item
                    IMEI_name=IMEIS_name[i]
                    IMEI_chatid=IMEIS_chatid[i]
                i=i+1
            if IMEI!="":
                if len(post_text) > 4000:
                    post_text = post_text[:4000]
                print(f"IMEI: {IMEI} Тема:{msg_subj} от {msg_from} для {msg_email} с вложением {attachments}")
                Send_ok = True;
                if attachments:
                    Send_ok=function.send_attach(msg, msg_subj, repl, IMEI, client, msg_datestr, bot, IMEI_chatid, msg_datetelegramm, IMEI_name, download_folder, batery)
                if not Send_ok:
                   # imap.uid('STORE', letter, '-FLAGS', '(\Seen)')
                   print(f"Пометили письмо {letter} как непрочитанное, так как не смоглм выгрузить вложения!")
                # if res == "OK":
        # if res == "OK":
    #for letter in unseen_msg:
else:
  print(f"Найдено писем: {len(unseen_msg)-1}")
#if unseen_msg[0]:

print(f"Обработка писем закончена!")
#bot.polling()

