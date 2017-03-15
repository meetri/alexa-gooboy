"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

import certifi
from elasticsearch import Elasticsearch

class Gooboy(object):

    def __init__(self, elasticnodes, index ):
        self.index = index
        self.title = "Gooboy"
        self.output = '<speak>Barney error 9 9 9 9 9 9</speak>'
        self.reprompt_text = ""
        self.endsession = True

        self.es = Elasticsearch( elasticnodes )


    def process_intent( self, intent ):
        question = ""
        if "slots" in intent and "Question" in intent["slots"] and "value" in intent["slots"]["Question"]:
            question = intent["slots"]["Question"]["value"]
            query = {
                "size": 1,
                "query": {
                    "match": {
                        "phrase": question
                    }
                }
            }

        res = self.es.search(index=self.index,doc_type="",body=query)
        if res != None and "hits" in res and res['hits']['total'] > 0:
            src = res['hits']['hits'][0]["_source"]
            self.output = src['response']
            self.endsession = src['endsession']
            if "reprompt" in src:
                self.reprompt_text = src['reprompt']


    def build_response( self ):
        speechlet_resp = Speech.build_speechlet_response(self.title,self.output,self.reprompt_text,self.endsession)

        return Speech.build_response( {}, speechlet_resp )




class Speech(object):

    @staticmethod
    def build_speechlet_response(title, output, reprompt_text, should_end_session):
        return {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': output
            },
            'card': {
                'type': 'Simple',
                'title': "SessionSpeechlet - " + title,
                'content': "SessionSpeechlet - " + output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }

    @staticmethod
    def build_response(session_attributes, speechlet_response):
        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': speechlet_response
        }

