from chatbot import robotConf, chatting, food, tg
from rasa_nlu.model import Interpreter
def main():
    #------------------------------------------------------------------
    # Initialize
    #------------------------------------------------------------------

    # Bot
    bot = tg.telegram.Bot(token=robotConf.TOKEN)
    update = bot.get_updates()
    chat_id = update[-1].message.chat_id
    length = len(update)


    # Part1: Chatting
    chat = chatting.Chat()

    # Part2: Search recipe
    interpreter = Interpreter.load(robotConf.rasa_model_dictionary)
    info = food.GetSearchInfo()
    fd = food.Food()
    pending = None
    params = {"food":None, "health":None, "calories":None, "rangefrom":None, "rangeto":None}
    state = info.INIT

    #------------------------------------------------------------------
    # Bot service begin
    #------------------------------------------------------------------
    tg.bot_speak(bot, "hello I'm " + robotConf.bot_name +", your recipe searching assistant.", chat_id)
    while(True):
        message, length = tg.get_user_words(bot, length)

        # Part1: Chatting
        if chat.IsTeacher(message):
            tg.toTeacher(bot, chat_id)
            continue
        response = chat.respond(message)
        if response is not None:
            tg.bot_speak(bot, response, chat_id)
            continue

        # Part2: Food
        # To control state change
        response, state, pending = info.state_change(state, pending, message)
        # Food related function
        if state == info.RECIPES_SEARCH:
            # Parse the message
            parse_result = interpreter.parse(message)
            intent = parse_result["intent"]["name"]
            # part1: Recommend
            if intent == "recommend":
                ani, text = fd.get_recomand_url_and_text()
                tg.bot_recommand(bot, ani, text, chat_id)
            # part2: Help
            elif intent == "help":
                tg.bot_speak(bot, fd.get_help(), chat_id)
            # part3: Search recipes
            elif intent == "recipes_search":
                # To update the params and get hint message

                message, params = info.get_serch_params(message, params, parse_result["entities"])
                if params["food"] is None:
                    tg.bot_speak(bot, info.no_food_response(), chat_id)
                    continue
                fd.set_params(params)
                recipe = fd.get_recipe()
                tg.bot_speak(bot, message, chat_id)
                tg.bot_send_recipe(bot, recipe, chat_id)
            # Default
            else:
                tg.bot_speak(bot, "I can't understand", chat_id)
        else:
            tg.bot_speak(bot, response, chat_id)


if __name__ == "__main__":
    main()
