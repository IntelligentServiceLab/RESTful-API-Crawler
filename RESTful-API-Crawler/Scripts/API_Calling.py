import requests

X_RapidAPI_Key = ""

url = "https://text-translator2.p.rapidapi.com/translate"

payload = {
	"source_language": "zh",
	"target_language": "en",
	"text": "今天是星期几？"
}
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
}

response = requests.post(url, data=payload, headers=headers)

url = "https://open-ai21.p.rapidapi.com/qa"

payload = {
	"question": response.json()['data']['translatedText'],
	"context": "The current date is November 17, year 2023."
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())