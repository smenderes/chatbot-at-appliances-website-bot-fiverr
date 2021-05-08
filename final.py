from dialogflow_fulfillment import QuickReplies, WebhookClient
from flask import Flask, request, Response, jsonify , make_response
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = 'google-sheet-key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1DxYub7bbxV_h2AR2lAp8aaTyuy52bmKNsKY8nPTHCnw'
service = build('sheets', 'v4', credentials=creds)

def handler(agent: WebhookClient) :
    """Handle the webhook request.."""

    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')

    if intent_name == 'welcome':
        agent.add('Hi! Welcome to AT Appliances - your # 1 place for all things your appliance services needs. We’re dedicated to providing you the very best of service repair for your appliances.')
        agent.add('I am the chatbot of this page. Ready to assist you with anything you need. What would you like to do?')
        agent.add(QuickReplies(quick_replies=['About us','Schedule a repair','Check your order status','Call us','Talk to a live agent']))

    if intent_name == 'Check_your_order_status':
        link2 = 'https://atservicefl.com/order-status//'
        agent.add('To get a quick update on your order please use the form below')
        agent.add(link2)

    if intent_name == 'Schedule_a_repair':
        link2 = 'https://atservicefl.com/appointment-schedule/'
        agent.add('To schedule an appointment please use the form below and we will be in touch shortly')
        agent.add(link2)

    if intent_name == 'call_us':
        agent.add('(754) 202-2000') 

    if intent_name == 'Talk_to_a_live_agent':
        agent.add('Please  give a heads up on what you would like to chat about, by typing it below')

    if intent_name == 'user_input':
        global user_input
        user_input = req.get('queryResult').get('queryText')
        agent.add('Please enter your name and phone # in case we get disconnected')
        
    if intent_name == 'name_number':
        name = req.get('queryResult').get('parameters').get('person').get('name')
        number = req.get('queryResult').get('parameters').get('phone-number')
        from datetime import datetime, date
        today = date.today()
        date = today.strftime("%b-%d-%Y")
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        sheett= [[date, time, user_input, name, number]]
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="O_Tacos!A1",valueInputOption="USER_ENTERED", body={"values" : sheett}).execute()



@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Handle webhook requests from Dialogflow."""
    # Get WebhookRequest object
    req = request.get_json(force=True)
    # Handle request
    agent = WebhookClient(req)
    agent.handle_request(handler)
    return agent.response

if __name__ == '__main__':
    app.run(debug=True)
