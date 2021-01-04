
import spacy 
nlp = spacy.load('en_core_web_sm')

# Create an nlp object
doc = nlp(input("Enter the query"))
 
# Iterate over the tokens
for token in doc:
    # Print the token and its part-of-speech tag
    print(token.text, "-->", token.pos_)