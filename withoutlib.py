from flask import Flask, request, Response, jsonify , make_response
import json


app = Flask(__name__)

@app.route('/')
def welcome():
    return "WELCOME !! GET YOUR CHEQUE BOOK DETAILS"


def testing():
    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')
    if intent_name=='Schedule_a_repair':
        
        #return { 'FulfillmentMessages': [
           # fulfillmentMessages ]}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(testing()))


# run the app
if __name__ == '__main__':
   app.run()

"""
fulfillmentMessages = {
  "payload": {
    "google": {
      #"expectUserResponse": true,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "These are suggestion chips."
            }
          },
          {
            "simpleResponse": {
              "textToSpeech": "Which type of response would you like to see next?"
            }
          }
        ],
        "suggestions": [
          {
            "title": "Suggestion 1"
          },
          {
            "title": "Suggestion 2"
          },
          {
            "title": "Suggestion 3"
          }
        ],
        "linkOutSuggestion": {
          "destinationName": "Suggestion Link",
          "url": "https://assistant.google.com/"
        }
      }
    }
  }
}




"""
