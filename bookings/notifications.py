# this is for email and SMS notofications functionality

import requests
import json
import os

firstname = 'Stanley'
service_no = '234565'
locker_number = '8089'
contact = '0200720509'
# contact = '579253016'
contacts = str(contact)

# # the HTML content of the email body
sms_body = f"Dear {firstname} \nYour Packagae has arrived at the pickup station. Kindly use {service_no} as password for the self-service locker number {locker_number}."
                


endPoint = 'https://api.mnotify.com/api/sms/quick'
bms_apiKey = 'ezCGA6a3PESqiuSFCWJtgOkxq' #ScepticLabs
data = {
  'recipient[]': contacts,
  'sender': 'EXON Labs',
  'message': sms_body,
  'is_schedule': False,
  'schedule_date': ''
}
url = endPoint + '?key=' + bms_apiKey
response = requests.post(url, data)
data = json.loads(response.text, strict=False)
print(data['status'])
