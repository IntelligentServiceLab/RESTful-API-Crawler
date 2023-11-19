import requests

def translate_text(source_language, target_language, text, api_key):
    url = "https://text-translator2.p.rapidapi.com/translate"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
    }
    payload = {
        "source_language": source_language,
        "target_language": target_language,
        "text": text
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()['data']['translatedText']

def ask_question(question, context, api_key):
    url = "https://open-ai21.p.rapidapi.com/qa"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
    }
    payload = {
        "question": question,
        "context": context
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()

def main():
    X_RapidAPI_Key = "YOUR_RAPIDAPI_KEY"

    translation = translate_text("zh", "en", "今天是星期几？", X_RapidAPI_Key)
    context = "The current date is November 17, year 2023."

    question_response = ask_question(translation, context, X_RapidAPI_Key)

    print(question_response)

if __name__ == "__main__":
    main()
