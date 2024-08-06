import os
import telebot
import speech_recognition
from pydub import AudioSegment

token = 'tocke here' 

bot = telebot.TeleBot(token)


def oga2wav(file):
    new_file = file.replace('.oga', '.wav')
    audio = AudioSegment.from_file(file)
    audio.export(new_file, format='wav')
    return new_file


def recognize_speech(oga_filename):
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='ru')

    if os.path.exists(oga_filename):
        os.remove(oga_filename)
    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text


def download_file(bot, file_id):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file = file_id + file_info.file_path
    file = file.replace('/', '_')
    with open(file, 'wb') as f:
        f.write(downloaded_file)
    return file


@bot.message_handler(commands=['start'])
def start_function(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, 'Привет ' + str(name) + '! \nЯ умею переводить голосовые сообщения в текст. Просто запиши мне голосовое, либо перешли из любого чата, а я в ответ пришлю тебе текст сообщения. \nПомни, что я не могу гарантировать 100% совпадение с голосовым сообщением, в виду особенностей речи/восприятия и т.д., но я буду стараться! \nЖду твое голосовое!) ')



@bot.message_handler(content_types=['voice'])
def transcript(message):
    file = download_file(bot, message.voice.file_id)
    text = recognize_speech(file)
    bot.send_message(message.chat.id, text)


bot.polling()
