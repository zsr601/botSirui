# Chat part

# Import module
from chatbot import robotConf, spacyEntity
import random
import re

# Define the class to deal with chat problem.
class Chat:
    # To init information
    def __init__(self):
        # part1: Simple selective answer, responses are here
        self.responses = {
                "Who are you?":
                          ["I'm {0} ^_^ , my hobby is cooking and enjoy delicacy" # 1
                                   .format(robotConf.bot_name),
                           "haha, they call me {0}, I have a strong desire to introduce " # 2
                                   "different delicacy for you".format(robotConf.bot_name),
                           "I go by {0}, delicacy is the most wonderful thing in " # 3
                                   "the world.".format(robotConf.bot_name) ],
                "What can you do?":
                          [
                           "I can recommend dish and teach you cooking.If you " # 1
                           "are alone, I'm always here for you. :)",
                           "Try to say recommend meal or I want to learn cooking, " # 2
                           "meanwhile, the happiest thing for me is to chat with you. :) " ]
        }
        # part2: Syntantic transforation to respond, rules are here
        self.rules = {
                "I wanna (.*)":
                          ["What would it mean if you got {0}", # 1
                           "Why do you want {0}", # 2
                           "What's stopping you from getting {0}"], # 3
                "do you remember (.*)":
                          ["Did you think I would forget {0}", # 1
                           "Why haven't you been able to forget {0}", # 2
                           "What about {0}", # 3
                           "Yes .. and?"], # 4
                "do you think (.*)":
                          ["if {0}? Absolutely.", # 1
                           "No chance"], # 2
                "if (.*)":
                          ["Do you really think it's likely that {0}", # 1
                           "Do you wish that {0}", # 2
                           "What do you think about {0}", # 3
                           "Really--if {0}"] # 4
        }
        # part3: Regex respond, patterns and intent_responses are here
        self.patterns = {
                'greet':    re.compile('hello|hi|hey'),
                'thankyou': re.compile('thank|Thank|thx'),
                'goodbye':  re.compile('bye|farewell|see you|Bye'),
                'affirm':   re.compile('Great|great|nice|adorable|kind|wonderful')
        }
        self.intent_responses = {
                'greet': ['hello, have a nice day.', 'Ah! you are come.'],
                'thankyou': ['you are very welcome', 'It\'s my pleasure' ],
                'goodbye': ['goodbye for now', 'byebye'],
                'affirm': ['Thank you, It\'s very kind of you to say so.', 'I\'m flattered.']
        }

    # --------------------------------------------------------------------
    # part1: function for simple selective answer
    # --------------------------------------------------------------------

    # --------------------------------------------------------------------
    # part2: function for syntantic transforation
    # --------------------------------------------------------------------
    # Define match_rule()
    def match_rule(self, message):
        # Init
        response, phrase = "default", None
        # Iterate over the rules dictionary
        for key, value in self.rules.items():
            # Create a match object
            match = re.search(key, message)
            if match is not None:
                # Choose a random response
                response = random.choice(self.rules[key])
                if '{0}' in response:
                    phrase = match.group(1)
        # Return the response and phrase
        return response, phrase

    # Define replace_pronouns()
    def replace_pronouns(self, message):
        message = message.lower()
        if 'me' in message:
            # Replace 'me' with 'you'
            return re.sub('me', 'you', message)
        if 'my' in message:
            # Replace 'my' with 'your'
            return re.sub('my', 'your', message)
        if 'your' in message:
            # Replace 'your' with 'my'
            return re.sub('your', 'my', message)
        if 'you' in message:
            # Replace 'you' with 'me'
            return re.sub('you', 'me', message)
        # Return the message
        return message

    # --------------------------------------------------------------------
    # part3: function for regex respond
    # --------------------------------------------------------------------
    # Define match_intent()
    def match_intent(self, message):
        matched_intent = None
        for intent, pattern in self.patterns.items():
            # Check if the pattern occurs in the message
            if re.search(pattern, message):
                matched_intent = intent
        return matched_intent

    # --------------------------------------------------------------------
    # part4: function for Name entities extraction (use spacy)
    # --------------------------------------------------------------------
    # Define find_name()
    def find_name(self, message):
    # Create a pattern for checking if the keywords occur
        name_keyword = re.compile(r"(call|name|I am|i am|I'm|i'm)")
        if name_keyword.search(message):
            # Use spacy to extract name
            ents = spacyEntity.extract_entities(message)
            if ents['PERSON'] is not None:
                return "^_^ Welcome, {} I've been looking forward to meet" \
                       " you.".format(ents['PERSON'])
        return None

    # --------------------------------------------------------------------
    # part5: function for particular words
    # --------------------------------------------------------------------
    def IsTeacher(self, message):
        pattern = re.compile("((I'm|My name is) (fan|Fan) (zhang|Zhang))")
        if re.search(pattern, message):
            return True
        else:
            return False

    # --------------------------------------------------------------------
    # function for respond
    # --------------------------------------------------------------------
    # To respond the message
    def respond(self, message):
        # part1: Simple selective answer
        if message in self.responses:
            # Return a random matching response
            response = random.choice(self.responses[message])
            # return response
            return response

        # part2: Syntantic transforation
        response, phrase = self.match_rule(message)
        if '{0}' in response:
            # Replace the pronouns in the phrase
            phrase = self.replace_pronouns(phrase)
            # Include the phrase in the response
            response = response.format(phrase)
            # return response
            return response

        # part3: Regex respond
        # Call the match_intent function
        intent = self.match_intent(message)
        # Fall back to the default response
        if intent in self.intent_responses:
            response = random.choice(self.intent_responses[intent])
            return response

        # part4: Spacy entities extraction
        # Find name and response
        response = self.find_name(message)
        if response is not None:
            return response
        # default info are in the function of food
        return None

# Tests
if __name__ == "__main__":
    chat = Chat()
    print(chat.respond("what if you could be anything you wanted"))
    print(chat.respond("Who are you?"))
    print(chat.respond("What can you do?"))
    print(chat.respond("hi"))
    print(chat.respond("thank"))
    print(chat.respond("bye"))
    print(chat.respond("you are so great."))
    print(chat.respond("I'm Sirui Zhao"))

