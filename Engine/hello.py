import flask
from flask import request, jsonify
from flask_cors import CORS
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from file import to_txt

app = flask.Flask(__name__)

CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})

nlp = spacy.load("pl_core_news_sm")
matcher = Matcher(nlp.vocab)
# matcher.add("NUMBER", [[{'LIKE_NUM': True}]])

matcher.add("Pesel", [[{"TEXT": {"REGEX": "^\d{11}$"}}]])
matcher.add("NIP", [[{"TEXT": {"REGEX": "^\d{10}$"}}]])
matcher.add("REGON", [[{"TEXT": {"REGEX": "^\d{9}$"}}]])
patternZipCode = [{"TEXT": {"REGEX": "^\d{2}$"}},
                {"IS_PUNCT": True},
                {"TEXT": {"REGEX": "^\d{3}$"}}]
matcher.add("KodPocztowy", [patternZipCode])

patternDate = [{"TEXT": {"REGEX": "^\d{2}$"}},
            {"IS_PUNCT": True},
            {"TEXT": {"REGEX": "^\d{2}$"}},
            {"IS_PUNCT": True},
            {"TEXT": {"REGEX": "^\d{4}$"}}]
matcher.add("Data", [patternDate])

matcher.add("EMAIL", [[{'LIKE_EMAIL': True}]])

@app.route('/api/v1/ner', methods=['POST'])
def api_all():
    text = request.json['text']
    doc = nlp(text)
    response = []
    for ent in doc.ents:
        response.append({'text': ent.text, 'start_char': ent.start_char, 'end_char': ent.end_char, 'label': ent.label_})

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        response.append(
            {'text': span.text, 'start_char': span.start_char, 'end_char': span.end_char, 'label': 'number'})

    return jsonify(response)

@app.route('/api/v1/pdfToText', methods=['POST'])
def convert_pdf_to_text():

    file = request.files['file']
    text = to_txt(file)
    return jsonify(text)


@app.route('/api/v1/switch', methods=['POST'])
def api_switch():
    text = request.json['text']
    doc = nlp(text)
    response = []
    for ent in doc.ents:
        response.append({'text': ent.text, 'start_char': ent.start_char, 'end_char': ent.end_char, 'label': ent.label_})

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        response.append(
            {'text': span.text, 'start_char': span.start_char, 'end_char': span.end_char, 'label': 'number'})

    for match in response:
        for x in range(match['start_char'], match['end_char']):
            if match['label'] == 'persName':
                initials = getFirstLetterOfWordInSentence(match['text'])
                if x == match['start_char']:
                    text = text[:x] + initials[0] + text[x + 1:]
                elif x == match['start_char'] + 1:
                    text = text[:x] + "." + text[x + 1:]
                elif x == match['start_char'] + 2:
                    text = text[:x] + initials[2] + text[x + 1:]
                elif x == match['start_char'] + 3:
                    text = text[:x] + "."+ text[x + 1:]
                else:
                    text = text[:x] + " " + text[x + 1:]
            else:
                text = text[:x] + "X" + text[x + 1:]

    return jsonify(text)

def getFirstLetterOfWordInSentence(sentence):
    words = sentence.split()
    letters = [word[0] for word in words]
    return " ".join(letters)



app.run(
    host="0.0.0.0"
)
