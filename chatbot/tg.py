# Related send message action
import telegram
import time

# To get user's words
# Use polling measure
def get_user_words(bot, length):
    #flag = True
    while(True):
        time.sleep(0.4)
        try:
            update = bot.get_updates()
        except:
            continue
        #if flag:
        #    length = len(update)
        #    flag = False
        if len(update) > length:
            message = update[-1].message.text
            # update the length
            length = len(update)
            return message, length

# Send text to user
def bot_speak(bot, message, chat_id):
    flag = True
    while(flag):
        try:
            bot.send_message(chat_id=chat_id, text=message)
            flag = False
        except:
            pass

# Send recommend to user
def bot_recommand(bot, animation, message, chat_id):
    flag = True
    while(flag):
        try:
            bot.send_message(chat_id=chat_id, text=message)
            flag = False
        except:
            pass

    flag = True
    while(flag):
        try:
            bot.send_animation(chat_id=chat_id, animation = animation)
            flag = False
        except:
            pass


# Send recipe to user
def bot_send_recipe(bot, recipe, chat_id):
    healthLabels = " ".join(recipe["healthLabels"])
    name = recipe["label"]
    text = "*RECIPE "+ name +"*\n_healthLabels: " + healthLabels +"_\n[learn more detailes in this link ^_^]" + "(" + recipe["url"] +")"

    flag = True
    while(flag):
        try:
            bot.send_message(chat_id=chat_id,
                             text=text,
                             parse_mode=telegram.ParseMode.MARKDOWN)
            flag = False
        except:
            pass



# Send message to teacher fan Zhang
def toTeacher(bot, chat_id, path = "/home/sirui/"):
    flag = True
    while(flag):
        try:
            bot.send_message(chat_id=chat_id, text="Teacher, here is a message for you.")
            flag = False
        except:
            pass
    flag = True
    while(flag):
        try:
            bot.send_voice(chat_id=chat_id, voice=open(path + 'Chatbot/docs/toTeacher.ogg', 'rb'))
            flag = False
        except:
            pass


