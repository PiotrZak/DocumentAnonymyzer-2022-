import logging

import azure.functions as func
import json
import spacy
from spacy.matcher import Matcher
import pl_core_news_sm

nlp = pl_core_news_sm.load()
matcher = Matcher(nlp.vocab)
matcher.add("NUMBER", [[{'LIKE_NUM': True}]])


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    text = req.get_json().get('text')
    if text:
        doc = nlp(text)
        response = []
        for ent in doc.ents:
            response.append(
                {'text': ent.text, 'start_char': ent.start_char, 'end_char': ent.end_char, 'label': ent.label_})

        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            response.append(
                {'text': span.text, 'start_char': span.start_char, 'end_char': span.end_char, 'label': 'number'})

        for match in response:
            for x in range(match['start_char'], match['end_char']):
                text = text[:x] + "X" + text[x + 1:]

        return func.HttpResponse(
            json.dumps({'anonymizedText': text, 'tokens': response}),
            status_code=200,
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
            "text is missing in the body",
            status_code=400
        )
