import boto3
import json
import requests

# You change these
new_Epicor_id = 9999
PORTAL_ID = 1088



AWS_SECRET_ARN = 'arn:aws:secretsmanager:us-middle-1:095943432212:secret:automation'

AWS_ACCESS_KEY_ID="AKIAJTLC:)CHSEOITF44"
aws_secret_access_key='EhzqQduNQZ9bfqz:)hiWso0AWB9RSp4emmuDksdjl'


session = boto3.session.Session()
client = session.client(service_name='secretsmanager',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=aws_secret_access_key)

secret_stuff = json.loads(client.get_secret_value(SecretId=AWS_SECRET_ARN)['SecretString'])

keys = []
for key, value in secret_stuff.items():
    keys.append(key)

url = "https://api.heartland.com/lakestreet/login/"
accessKey = requests.post(url, json={"u": secret_stuff["dnn_username"], "p": secret_stuff["dnn_password"] }).json()['accessToken']
print(accessKey)


url = "https://api.heartland.com/lakestreet/{}/metadata/".format(PORTAL_ID)
req = requests.get(url, headers={"Content-Type": "application/json", 'Authorization': "Bearer {}".format(accessKey)})
print(req.status_code)

print("Epicor Id:", req.json()["result"]["epicor_id"])


while req.json()["result"]["epicor_id"] != str(new_Epicor_id):
    print("Updating Epicor Id...")
    url = "https://api.heartland.com/lakestreet/{}/metadata/".format(PORTAL_ID)
    req = requests.put(
        url,
        headers={
            "Content-Type": "application/json",
            'Authorization': "Bearer {}".format(accessKey)
        },
        json={"epicor_id": new_Epicor_id}
    )
    print(req.status_code)

    req = requests.get(url, headers={"Content-Type": "application/json", 'Authorization': "Bearer {}".format(accessKey)})

print("Epicor is changed")
