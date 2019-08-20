# use this module to extract user' name
# import module
import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()

#### Entity extraction
## Using spaCy's entity recogniser

# Define included entities
include_entities = ['PERSON']

# Define extract_entities()
def extract_entities(message):
    # Create a dict to hold the entities
    ents = dict.fromkeys(include_entities)
    # Create a spacy document
    doc = nlp(message)
    for ent in doc.ents:
        if ent.label_ in include_entities:
            # Save interesting entities
            ents[ent.label_] = ent.text
    return ents

