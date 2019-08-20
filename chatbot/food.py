# Food's part

# Import module
import requests
import string
from chatbot import robotConf, rasaInterpreter, Translate
import random

class Food:
    # Init
    def __init__(self):
        # Define searching params
        self.food = None
        self.health = None
        self.calories = None
        self.rangefrom = None
        self.rangeto = None

        # Gif for recommand function
        self.food_gif_list =[
            ("http://wx3.sinaimg.cn/mw690/eb5c94aegy1g4tvij8pqkg20ak05yqv5.gif", "泡椒蛤蜊"),
            ("http://wx3.sinaimg.cn/mw690/eb5c94aegy1g41ku262i5g20ak05yu0x.gif", "生煎包"),
            ("http://wx1.sinaimg.cn/mw690/eb5c94aegy1g3yhcjgff0g20ak05yqv9.gif", "麻辣小龙虾"),
            ("http://wx1.sinaimg.cn/mw690/eb5c94aegy1g32a8dy7o7g20ak05yqv5.gif", "咖喱豆腐拌红豆饭"),
            ("http://wx2.sinaimg.cn/mw690/eb5c94aegy1g1fhduhn15g20ak05ykjl.gif", "部队锅泡面"),
            ("http://wx3.sinaimg.cn/mw690/eb5c94aegy1g0r0e4gwf6g20ak05yu0x.gif", "牛奶醪糟鸡蛋"),
            ("http://wx1.sinaimg.cn/mw690/eb5c94aegy1fxwzmf301tg20ak05yqv5.gif", "大闸蟹"),
            ("http://wx3.sinaimg.cn/mw690/eb5c94aegy1fx8peqrdgfg20ak05yu0x.gif", "炒饭"),
            ("http://wx2.sinaimg.cn/mw690/eb5c94aegy1g5pyau55dig20ak05y1j4.gif", "莲花酥"),
            ("http://wx3.sinaimg.cn/mw690/eb5c94aegy1g50rf3eahjg20g40921l2.gif", "杏仁豆腐")
        ]
        self.response = [
            ":) haha, how about {} ? ",
            "emmmmm, this dish {} looks so delicious. hope you like it. :) ",
            "would you like this dish {} ? :) ",
            "we call it {},vmy friend  told me this dish is wonderful, hope you like :) "]
        # Help menu
        self.help_menu = "1.I can search recipe for you.\n " \
                         "Try to ask me ""in this way: I want juice, alcohol-free, calories range" \
                         " is 100-300 kcal per serving.\n" \
                         "2.If you do not have idea for what to eat, \n" \
                         "try to ask me , can you recommend some food for me?)"
    #---------------------------------------------------------------------------------
    # Part1: function for Recommend
    #---------------------------------------------------------------------------------
    # Define get_recomand_url_and_text()
    def get_recomand_url_and_text(self):

        animation, message = random.choice(self.food_gif_list)
        text=random.choice(self.response).format(Translate.translate(message)) + \
             "( In chinese we call it " + message + " )"
        return animation, text

    #---------------------------------------------------------------------------------
    # Part2: function for Help
    #---------------------------------------------------------------------------------
    # Define get_help()
    def get_help(self):
        return self.help_menu
    #---------------------------------------------------------------------------------
    # Part3: function for Search recipes
    #---------------------------------------------------------------------------------
    # Define set_params()
    def set_params(self, params):
            self.food = params["food"]
            self.health = params["health"]
            self.calories = params["calories"]
            self.rangefrom = params["rangefrom"]
            self.rangeto = params["rangeto"]

    # Define get_recipe()
    def get_recipe(self):
        # Make the basic url
        url = "http://api.edamam.com/search?q=" + self.food + \
              "&app_id=" + robotConf.food_app_id + \
              "&app_key=" + robotConf.food_app_key
        # Add searching terms
        if self.health is not None:
            # Diet label: 'alcohol-free' and so on
            url += "&health=" + self.health
        if self.calories is not None:
            # Examples: “100-300” will return all recipes with which
            # have between 100 and 300 kcal per serving.
            url += "&calories=" + self.calories
        if self.rangefrom is not None and self.rangeto is not None:
            url += "&from=" + str(self.rangefrom) + "&to=" + str(self.rangeto)

        flag = True
        while(flag):
            try:
                # Use requests to get info, api: https://api.edamam.com/
                response = requests.get(url)
                recipe = random.choice(response.json()["hits"])["recipe"]
                flag = False
            except:
                pass

        # Return the a recipe
        return recipe

class GetSearchInfo:
    # Define States

    # To init information
    def __init__(self):
        self.INIT = 0
        self.AUTHED=1
        self.RECIPES_SEARCH=2
        # Define the policy rules
        self.policy_rules = {
            (self.INIT, "recipes_search"): (self.INIT, "emmm, please tell me your phone number at first "
                                                       "because I need to confirm who are you", self.AUTHED),
            (self.INIT, "number"): (self.AUTHED, "Perfect, welcome back! ", None),
            (self.AUTHED, "recipes_search"): (self.RECIPES_SEARCH, "I can recommend, search recipes for you,"
                                                                   " you can see more info ask me for help.", None),
            (self.RECIPES_SEARCH, "recipes_search"): (self.RECIPES_SEARCH, "", None)
        }

    #---------------------------------------------------------------------------------
    # function for state machine
    #---------------------------------------------------------------------------------
    # Define interpret()
    def interpret(self, message):
        msg = message.lower()
        if any([d in msg for d in string.digits]):
            return 'number'
        else:
            return "recipes_search"

    # Define state_change()
    def state_change(self, state, pending, message):
        new_state, response, pending_state = self.policy_rules[(state, self.interpret(message))]

        if pending is not None:
            # new_state, r, pending_state = self.policy_rules[pending]
            _, r, pending_state = self.policy_rules[pending]
            response += r
        if pending_state is not None:
            pending = (pending_state, self.interpret(message))
        else:
            pending = None
        return response, new_state, pending

    #---------------------------------------------------------------------------------
    # function for negated and rounds search
    #---------------------------------------------------------------------------------
    # Define negated_ents()
    def negated_ents(self, phrase, ent_vals):
        ents = [e for e in ent_vals if e in phrase]
        ends = sorted([phrase.index(e) + len(e) for e in ents])
        start = 0
        chunks = []
        for end in ends:
            chunks.append(phrase[start:end])
            start = end
        result = {}
        for chunk in chunks:
            for ent in ents:
                if ent in chunk:
                    if "not" in chunk or "n't" in chunk:
                        result[ent] = False
                    else:
                        result[ent] = True
        return result

    # Define no_food_response()
    def no_food_response(self):
        response = random.choice(["At least I need to now the food you are looking for.",
                       "Which food would you like?",
                       "food you'd like to eat ?",
                       "Which food you are searching for ?"])
        return response
    # Define get_serch_params()
    def get_serch_params(self, message, params, entities):

        ent_vals = [e["value"] for e in entities]

        # Look for negated entities
        negated = self.negated_ents(message, ent_vals)
        for ent in entities:
            if ent["value"] in negated and not negated[ent["value"]] and ent["value"] == params[ent["entity"]]:
                params[ent["entity"]] = None
            else:
                params[ent["entity"]] = ent["value"]

        if params["food"] is not None:

            response = random.choice(["here is a recipe, {}, hope you like it.",
                                      "{}, this dish is suitable , looks very delicious ^_^ .",
                                      "haha, I have searched one, {}",
                                      "This menu is my favourite one, {}"])
            item = []
            for par in params:
                if params[par] is not None:
                    params[par] = params[par].replace(" ", "") # to clear blank
                    item.append(params[par])

            return response.format(",".join(item)), params
        else:
            return "", params

if __name__ == "__main__":
    fd =Food()
    info = GetSearchInfo()
    pending = None
    params = {"food":None, "health":None, "calories":None, "rangefrom":None, "rangeto":None}
    state = info.INIT

    while(True):
        message = input("USER : ")

        # Change state
        response, state, pending = info.state_change(state, pending, message)
        # Food related function
        if state == info.RECIPES_SEARCH:
            # Parse the message
            parse_result = rasaInterpreter.interpreter.parse(message)
            intent = parse_result["intent"]["name"]
            # part1: Recommend
            if intent == "recommend":
                ani, text = fd.get_recomand_url_and_text()
                print(ani, text)
            # part2: Help
            elif intent == "help":
                print("BOT : " + fd.get_help())
            # part3: Search recipes
            elif intent == "recipes_search":
                # To update the params and get hint message
                message, params = info.get_serch_params(message, params, parse_result["entities"])
                print("BOT : " + message)
            # default
            else:
                print(robotConf.bot_name + " likes all kinds of delicacy most")
        else:
            print("Bot : " + response)

