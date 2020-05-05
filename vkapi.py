import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def upload_photo(vk_session, event, x):
    upload = vk_api.VkUpload(vk_session)
    for i in range(1, 3):
        photo = upload.photo_messages([f'timetable\{x}{i}.jpg'])
        vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
        vk = vk_session.get_api()
        vk.messages.send(user_id=event.obj.message['from_id'],
                         attachment=vk_photo_id, message='',
                         random_id=random.randint(0, 2 ** 64))


def timet(vk, longpoll, vk_session):
    for event in longpoll.listen():
        text = event.obj.message['text'].lower()
        if event.type == VkBotEventType.MESSAGE_NEW:
            if 'стоп' in text:
                break
            if ('понедельник' in text) or ('пн' in text):
                upload_photo(vk_session, event, 'пн')
            elif ('вт' in text) or ('вторник' in text):
                upload_photo(vk_session, event, 'вт')
            elif ('ср' in text) or ('сред' in text):
                upload_photo(vk_session, event, 'ср')
            elif ('чт' in text) or ('четверг' in text):
                upload_photo(vk_session, event, 'чт')
            elif ('пт' in text) or ('пятниц' in text):
                upload_photo(vk_session, event, 'пт')
            elif ('сб' in text) or ('суббот' in text) or ('вс' in text) or ('воскресенье' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Кайф! Уроков нет!',
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Какой день недели?',
                                 random_id=random.randint(0, 2 ** 64))


def main():
    vk_session = vk_api.VkApi(
        token='1fcd036663cf0104cf09ecce90a3f5730755ba1d554a4e6b1aa3fd89c1117441a4961e7bd7cda4de441c7')
    longpoll = VkBotLongPoll(vk_session, 174388874)
    m = 0
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            text = event.obj.message['text'].lower()
            if m == 0:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Добрый день. Я очень рад, что Вы написали мне! Как я могу к Вам обращаться?",
                                 random_id=random.randint(0, 2 ** 64))
            elif m == 1:
                name = event.obj.message['text']
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Приятно познакомиться, {name}. Меня зовут Иннокентий, для друзей просто Кеша. Я проводник по миру ФМШ",
                                 random_id=random.randint(0, 2 ** 64))
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f'{name}, если хочешь поболтать - напиши "Хочу поговорить",\n '
                                         f'ищешь актуальное расписание - "Расписание",\n '
                                         f'нужна помощь в фмшатской сети - пиши "Соц сеть",\n '
                                         f'изменить имя - "Другое имя"',
                                 random_id=random.randint(0, 2 ** 64))
            elif 'расписание' in text:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f'{name}, теперь вы в блоке расписание. Чтобы выйти, напишите "стоп", Если хотите продолжить - "ок"',
                                 random_id=random.randint(0, 2 ** 64))
                timet(vk, longpoll, vk_session)


            elif '' in text:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f'{name}, я не понял... Заново, пожалйста.',
                                 random_id=random.randint(0, 2 ** 64))
            m += 1


if __name__ == '__main__':
    main()
