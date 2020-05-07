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


def site(vk, longpoll):
    for event in longpoll.listen():
        text = event.obj.message['text'].lower()
        if event.type == VkBotEventType.MESSAGE_NEW:
            if ('1.1' in text) or ('условия' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Стать участниками социальной сети ФМШ могут все обладатели корпоративной '
                                         'почты ГАОУ ТО "Физико-математическая школа" вида mail@fmschool72.ru: ученики,'
                                         ' учителя, администрация. Для регистрации необходимо указать адрес электронной'
                                         ' почты ФМШ, фамилию, имя, телефон и придумать пароль, также можно ввести '
                                         'информацию в поле "О себе"',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('1.2' in text) or ('зарегистрир' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Для регистрации необходимо указать адрес электронной почты ФМШ вида '
                                         'mail@fmschool72.ru, фамилию и имя с большой буквы в иминительном падеже, '
                                         'телефон. Вы можете указать дополнительную информацию в поле "О себе". Помните'
                                         ', она видна всем зарегистрированным пользователям!\nПри регистрации '
                                         'необходимо придумать пароль (если необходима помощь в создании пароля, '
                                         'напишите "пароль"), а затем ввести его повторно. Так мы проверяем его '
                                         'корректность.\nПосле нажатия кнопки "Зарегистрироваться", вы сможете '
                                         'использовать все возможности социальной сети!',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('2.1' in text) or ('новости' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='В этой социальной сети реализован новостной канал. Чтобы чем-то поделиться, '
                                         'надо зайти в свой профиль или ленту новостей, нажать на кнопку "Добавить '
                                         'новость" и дать волю фантазии! Вы можете написать все, о чем сейчас трепещет '
                                         'душа или чем хочется поделиться со своими подписчиками. Для выражения эмоций '
                                         'в более наглядной форме - вставь картинку. Пока можно вставить только ее URL,'
                                         ' но мы над этим работаем, и скоро можно будет загружать с устройства.\nЧтобы '
                                         'опубликовать запиь, нажмите на кнопку "Submit". Автоматически будет указана '
                                         'дата и время добавления новости. Вы можете не только добавлять новости, но и'
                                         ' редактировать и удалять их. \nНовая новость добавится в личную (на '
                                         'странице профиля) и в новостную (на странице "Новости") ленты. Есть '
                                         'возможность смотреть не только свои, но и новости тех, на кого подписаны. '
                                         'Всегда хорошо получать обратную связь - для этого есть лайки❤',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('2.2' in text) or ('сообщения' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Вкладка "Сообщения" в левом меню откроет замечательный способ связи с '
                                         'друзьями, учителями и вообще всей школой.\nПри нажатии на нее появится '
                                         'список начатых чатов. Выбирайте, с кем пообщаться сейчас) Если нет '
                                         'желаемой переписки - достаточно на странице "Подписки" выбрать того, с кем '
                                         'хочется пообщаться, нажав на кнопку "Написать". \nОткроется чат: В длинном '
                                         'поле в нижней части страницы вводится сообщение, нажатием на стрелочку - '
                                         'отправляется. Можно вводить сообщения любой длины, а если вводить число пи '
                                         'без точки "314159265358979323946", оно заменится на '
                                         '"3.1415926535897933e+32"🤓. \nПерейти в список чатов можно нажатием кнопки '
                                         '"Назад" в левой верхней части вкладки или "Сообщения" в левом меню.\nВ списке '
                                         'чатов отражены пользователи, с которыми вы общались, дата последнего с'
                                         'ообщения (по ней сортируется список), само сообщение, сокращенное до 50 '
                                         'символов (если сообщение больше появляется "..."). \nЕсли вам пришло новое '
                                         'сообщение, рядом с пользователем появляется кружок с количеством '
                                         'непрочитанных сообщений, который после открытия чата с этим пользователем '
                                         'исчезает. Если же сообщение не прочитано тем, кому вы его отправили - '
                                         'оно зеленое, прочитанное - серое.',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('2.3' in text) or ('подписк' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Много друзей? Подписывайтесь на всех нажтием кнопки "Подписаться" в профиле '
                                         'друзей и знакомых. А посмотреть список подписок и подписчиков можно на '
                                         'странице "Подписчики". Тут же можно отписаться или подписаться на '
                                         'пользователя или написать сообщение, нажав на кнопку "Написать". ',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('2.4' in text) or ('чат-бот' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Чат-бот ВКонтакте - это я, Иннокентий. Всегда готов прийти на помощь, '
                                         'подсказать при работе в социальной сети ФМШ и просто поболтать о жизни👋🏻',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('2.5' in text) or ('пригла' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='По моему мнению, кнопка "Пригласить друзей" - волшебная. Она настолько '
                                         'волшебна, что ее работа неподвластна моим создателям. Однако, они постоянно '
                                         'трудятся над совершенствованием своих знаний, навыко и возможностей, '
                                         'постепенно улучшая и увеличивая функционал социальной сети и чат-бота. '
                                         'Не переживайте, я уверен, скоро эта кнопка будет работать, а я объясню, как '
                                         'ей пользоваться!',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('2.6' in text) or ('профиль' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Перейти в свой профиль можно нажатием на свой ник в правом верхнем углу любой'
                                         ' страницы. Вы можете изменить свой профиль нажатием на кнопку "Редактировать"'
                                         '. Можно смотреть свою ленту - те новости, которые выложили вы. Тут, как и в '
                                         'новостной ленте, можно добавлять, редактировать и удалять новости. \n'
                                         'Нажав на другого пользователя (в новостной ленте, в списке '
                                         'подписок/подписчиков, в чате), вы перейдете в профиль этого пользователя. '
                                         'Можно увидеть информацию о нем, его новости. Так как чужие новости удалять '
                                         'нельзя, вы можете только просматривать и лайкать их.',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('1.3' in text) or ('возможност' in text) or ('2' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Как классно, что соц.сеть ФМШ интересна! Теперь можно узнать о ней все (или '
                                         'почти все (или чуточку больше😂))',
                                 random_id=random.randint(0, 2 ** 64))
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Что интересного я могу рассказать:\n2.1. Новости\n2.2. Сообщения\n'
                                         '2.3. Подписки\n2.4. Чат-бот ВК \n2.5 .Пригласить друзей \n'
                                         '2.6. Профиль',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('1' in text) or ('регистрация' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='1.1. Условия регистрации\n1.2. Как зарегистрироваться\n1.3. Возможности '
                                         'социальной сети',
                                 random_id=random.randint(0, 2 ** 64))

            elif '3' in text:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Хорошо, скоро наш менеджер свяжется с вами',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('полное меню' in text) or ('4.2' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Вот, в чем я могу помочь относительно социальной сети ФМШ:'
                                         '\n1. регистрация'
                                         '\n  1.1. Условия регистрации'
                                         '\n  1.2. Как зарегистрироваться'
                                         '\n  1.3. Возможности социальной сети'
                                         '\n2. Возможности социальной сети'
                                         '\n  2.1. Новости'
                                         '\n  2.2. Сообщения'
                                         '\n  2.3. Подписки'
                                         '\n  2.4. Чат-бот ВК '
                                         '\n  2.5 .Пригласить друзей '
                                         '\n  2.6. Профиль'
                                         '\n3. Подождать ответа менеджера'
                                         '\n4. Возможные действия - меню'
                                         '\n  4.1. Краткое меню'
                                         '\n  4.2. Полное меню'
                                         '\n5. Выход - стоп\n\n\n\n\n\n\n',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('4' in text) or ('4.1' in text) or ('меню' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Что вас интересует:\n1. Регистрация'
                                         '\n2. Возможности социальной сети\n'
                                         '3. Подождать ответа менеджера\n'
                                         '4. Возможные действия - меню\n'
                                         '4.2. Полное меню\n'
                                         '5. Выйти - напишите "стоп"',
                                 random_id=random.randint(0, 2 ** 64))

            elif ('стоп' in text) or ('5' in text) or ('выход' in text) or ('выйти' in text):
                break
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Я не понял... Повторите, пожалуйста.\nЧтобы выбрать действие, напишите '
                                         '"меню"',
                                 random_id=random.randint(0, 2 ** 64))


def upload_mem(vk_session, event, dict, x):
    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_messages([f'{dict}\{random.randint(1, x)}.jpg'])
    vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    vk = vk_session.get_api()
    vk.messages.send(user_id=event.obj.message['from_id'],
                     attachment=vk_photo_id, message='',
                     random_id=random.randint(0, 2 ** 64))


def talk(vk, longpoll, name, vk_session):
    n = 0
    yes = ['Это замечательно!', 'Классно!', 'Положительный ответ - сладость для моих ушей', 'Вот это превосходно!',
           '👍🏻', '🙏🏻', '🤘']
    no = ['Ваша правда, соглашаться нужно не всегда!', 'Всякое бывает', 'Лучше горькая правда, чем сладкая лесть',
          'Я полностью с тобой согласен', '🤔', '😲']

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.obj.message['text'].lower()


            if ('да' in text) or ('yes' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=yes[random.randint(0, 6)],
                                 random_id=random.randint(0, 2 ** 64))
            elif ('нет' in text) or ('no' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=no[random.randint(0, 6)],
                                 random_id=random.randint(0, 2 ** 64))


            if ('выйти' in text) or ('стоп' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Было приятно с Вами пообщаться! До встречи, {name}",
                                 random_id=random.randint(0, 2 ** 64))

            elif n == 0:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Это прекрано, {name}! А я - чат-бот, и мне это ужасно нравится! А Вы любите "
                                         "то, что делаете?",
                                 random_id=random.randint(0, 2 ** 64))

            elif (n == 1) or ('мем' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Возможно, Вы захотите посмеяться? Доказано, что смех продлевает жизнь!\n'
                                         'Недавно в Яндекс.Лицее проходил конкурс на лучший мем, ребята присылали '
                                         'столько смешных шуток😂 Показать Вам парочку? (да/нет)',
                                 random_id=random.randint(0, 2 ** 64))

            elif (n == 2) and ('да' in text):
                upload_mem(vk_session, event, 'yand_mem', 27)
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Чтобы посмотреть еще мемов, напишите: "еще"',
                                 random_id=random.randint(0, 2 ** 64))
                n -= 1

            elif (n == 2) and (('еще' in text) or ('ещё' in text)):
                upload_mem(vk_session, event, 'yand_mem', 27)
                n -= 1

            elif n == 2:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f'Еще у меня есть подборка смешных картинок. {name}, посмотрите?(да/нет)',
                                 random_id=random.randint(0, 2 ** 64))
                upload_mem(vk_session, event, 'yand_mem', 27)

            elif (n == 3) and ('да' in text):
                upload_mem(vk_session, event, 'else_mem', 40)
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Чтобы посмотреть еще мемов, напишите: "еще"',
                                 random_id=random.randint(0, 2 ** 64))
                n -= 1

            elif (n == 3) and (('еще' in text) or ('ещё' in text)):
                upload_mem(vk_session, event, 'else_mem', 40)
                n -= 1

            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f'Было приятно с Вами пообщаться! До встречи, {name}!',
                                 random_id=random.randint(0, 2 ** 64))
                break
            n += 1


def apivk():
    vk_session = vk_api.VkApi(
        token='1fcd036663cf0104cf09ecce90a3f5730755ba1d554a4e6b1aa3fd89c1117441a4961e7bd7cda4de441c7')
    longpoll = VkBotLongPoll(vk_session, 174388874)
    m = 0
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
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
                                 message=f'{name}, теперь вы в блоке расписание. Чтобы выйти, напишите "стоп", если хотите продолжить - "ок"',
                                 random_id=random.randint(0, 2 ** 64))
                timet(vk, longpoll, vk_session)
            elif 'соц' in text:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f'Теперь {name} в блоке социальной сети ФМШ. Чтобы выйти, напишите "стоп". '
                                         f'Что вас интересует:\n1. Регистрация\n2. Действия внутри сети\n'
                                         f'3. Подождать ответа менеджера',
                                 random_id=random.randint(0, 2 ** 64))
                site(vk, longpoll)
            elif 'имя' in text:
                m = 0
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Как я могу к Вам обращаться?",
                                 random_id=random.randint(0, 2 ** 64))
            elif 'заново' in text:
                m = -1
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Хорошо, начнем же все с чистого листа!",
                                 random_id=random.randint(0, 2 ** 64))
            elif 'меню' in text:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Вот, что я могу:'
                                         '\nПоказать расписание на неделю'
                                         '\nРассказать про социальную сеть ФМШ'
                                         '\nПоболтать'
                                         '\nТакже можно:'
                                         '\nПоказать меню'
                                         '\nИзменить имя'
                                         '\nНачать разговор заново',
                                 random_id=random.randint(0, 2 ** 64))
            elif ('болтать' in text) or ('говор' in text):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Давайте пообщаемся! Расскажите о себе. Кто вы?',
                                 random_id=random.randint(0, 2 ** 64))
                talk(vk, longpoll, name, vk_session)
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f'{name}, я не понял... Заново, пожалуйста.',
                                 random_id=random.randint(0, 2 ** 64))
            m += 1


if __name__ == '__main__':
    apivk()
