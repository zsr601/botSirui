# To train and rasa interpreter
# The model will be saved in the path you set
# Import necessary modules
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer, Interpreter
from rasa_nlu import config

# Generate a interpreter than can extract intent and entities
def get_rasa_interpreter(path = "/home/sirui/Chatbot/docs/rasa"):
    # Create a trainer that uses this config
    trainer = Trainer(config.load(path + "/config_spacy.yml"))

    # Load the training data
    training_data = load_data(path + "/demo-rasa.json")

    # Create an interpreter by training the model
    trainer.train(training_data)
    dictionary = trainer.persist(path)
    # return the interpreter
    return dictionary


