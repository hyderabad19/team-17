import requests

url = "https://www.fast2sms.com/dev/bulk"

payload = "sender_id=FSTSMS&message=This%20is%20a%20test%20message&language=english&route=p&numbers=8500570821"
headers = {
    'authorization': "EImk0VKlbuC29gAJU4vNzioLPGcp613eMrf8DqsFXOydWTjaxQcSCI5QRMOyTaB73v9ZJf0K2PkA1hNo",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)