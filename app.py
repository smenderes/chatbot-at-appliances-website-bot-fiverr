from dialogflow_fulfillment import QuickReplies, WebhookClient, Payload
from flask import Flask, request, Response, jsonify , make_response
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = 'google-sheet-key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_SPREADSHEET_ID = '1IYNYC65qKSSQQiPM2lZs0NN9v9SZhNt2FwdnAvJ2Vhw'
service = build('sheets', 'v4', credentials=creds)

def handler(agent: WebhookClient) :
    """Handle the webhook request.."""

    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')

    if intent_name == 'welcome_0':
        agent.add('Hi! Welcome to AT Appliances - your # 1 place for all things your appliance services needs. We’re dedicated to providing you the very best of service repair for your appliances.')
        agent.add('I am the chatbot of this page. Ready to assist you with anything you need. What would you like to do?')
        agent.add(QuickReplies(quick_replies=['About us','Schedule a repair','Check your order status','Call us','Talk to a live agent']))

    if intent_name == 'welcome_1':
        agent.add('Hi! Welcome to ADA Repair - your # 1 place for all things your appliance services needs. We’re dedicated to providing you the very best of service repair for your appliances.')
        agent.add('I am the chatbot of this page. Ready to assist you with anything you need. What would you like to do?')
        agent.add(QuickReplies(quick_replies=['About us','Schedule a repair','Check your order status','Call us','Talk to a live agent']))

    if intent_name == 'welcome_2':
        agent.add('Hi! Welcome to ACCORD Appliances - your # 1 place for all things your appliance services needs. We’re dedicated to providing you the very best of service repair for your appliances.')
        agent.add('I am the chatbot of this page. Ready to assist you with anything you need. What would you like to do?')
        agent.add(QuickReplies(quick_replies=['About us','Schedule a repair','Check your order status','Call us','Talk to a live agent']))

    if intent_name== 'hello':
        agent.add('Please make a choice from the options below')
        agent.add(QuickReplies(quick_replies=['About us','Schedule a repair','Check your order status','Call us','Talk to a live agent']))
        
    if intent_name == 'call_us':
        agent.add("Hello, Contact us on")
        agent.add('(754) 202-2000') 

    if intent_name == 'Talk_to_a_live_agent':
        agent.add('Please give a heads up on what you would like to chat about, by typing it below')

    if intent_name == 'user_input':
        agent.add('Please type your name below')
        
    if intent_name == 'name_number_0':
        name = req.get('queryResult').get('parameters').get('name')
        number = req.get('queryResult').get('parameters').get('phone-number') 
        user_concern = agent.context.get('awaiting_user_info').get('parameters').get('any')[0] 
        from datetime import datetime, date
        today = date.today()
        date = today.strftime("%b-%d-%Y")
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        sheett= [[date, time, user_concern, name, number]]
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="AT_Appliances",valueInputOption="USER_ENTERED", body={"values" : sheett}).execute()
        agent.add("dummy")
        agent.set_followup_event("follow_up_agent")

    if intent_name == 'name_number_1':
        name = req.get('queryResult').get('parameters').get('name')
        number = req.get('queryResult').get('parameters').get('phone-number') 
        user_concern = agent.context.get('awaiting_user_info').get('parameters').get('any')[0] 
        from datetime import datetime, date
        today = date.today()
        date = today.strftime("%b-%d-%Y")
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        sheett= [[date, time, user_concern, name, number]]
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="ADA_repair",valueInputOption="USER_ENTERED", body={"values" : sheett}).execute()
        agent.add("dummy")
        agent.set_followup_event("follow_up_agent")

    if intent_name == 'name_number_2':
        name = req.get('queryResult').get('parameters').get('name')
        number = req.get('queryResult').get('parameters').get('phone-number') 
        user_concern = agent.context.get('awaiting_user_info').get('parameters').get('any')[0] 
        from datetime import datetime, date
        today = date.today()
        date = today.strftime("%b-%d-%Y")
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        sheett= [[date, time, user_concern, name, number]]
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="ACCORD_Appliances",valueInputOption="USER_ENTERED", body={"values" : sheett}).execute()
        agent.add("dummy")
        agent.set_followup_event("follow_up_agent")



@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Handle webhook requests from Dialogflow."""
    req = request.get_json(force=True)
    agent = WebhookClient(req)
    agent.handle_request(handler)
    return agent.response

if __name__ == '__main__':
    app.run(debug=True)
