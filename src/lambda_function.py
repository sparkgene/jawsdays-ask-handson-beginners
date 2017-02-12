# -*- coding: utf-8 -*-
import os

AUDIO_BUCKET = os.environ["AUDIO_BUCKET"]
AUDIO_URL = "https://s3.amazonaws.com/{}/{}"

def lambda_handler(event, context):
    print(event)

    if event['request']['type'] == "LaunchRequest":
        return on_launch()
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event["session"])


def on_launch():
    print("on_launch")
    return return_help()

def on_intent(request, session):
    print("on_intent")

    intent_name = request['intent']['name']
    print("intent name: {}".format(intent_name))

    if intent_name == "AskIntent":
        return return_question()
    elif intent_name == "HungryIntent":
        return return_eat()
    elif intent_name == "BathIntent":
        return return_bath()
    elif intent_name == "GoodbyeIntent":
        return return_goodbye()
    elif intent_name == "AMAZON.StopIntent":
        return return_cancel()
    elif intent_name == "AMAZON.HelpIntent":
        return return_help()
    else:
        return return_konwaku()


# --------------- Functions that control the skill's behavior ------------------

def return_help():
    title = "ご主人様、こんにちわ。"
    speech = "<audio src=\"{}\"></audio>".format(
        audio_url("help.mp3")
    )
    card_text = "私にお手伝いできることがあれば言ってくださいね。"
    close_session = True

    return build_speechlet_response(title, speech, card_text, close_session)

def return_question():
    title = "おかえりなさいませ、ご主人様。"
    speech = "<audio src=\"{}\"></audio><audio src=\"{}\"></audio>".format(
        audio_url("hello.mp3"),
        audio_url("question.mp3")
    )
    card_text = "お食事にしますか、お風呂にしますか？"
    close_session = False

    return build_speechlet_response(title, speech, card_text, close_session)

def return_bath():
    title = "お風呂ですね。"
    speech = "<audio src=\"{}\"></audio><audio src=\"{}\"></audio>".format(
        audio_url("bath.mp3"),
        audio_url("suffix.mp3")
    )
    card_text = "すぐ用意しますので、くつろいでおまちになってくださいね。"
    close_session = True

    return build_speechlet_response(title, speech, card_text, close_session)

def return_eat():
    title = "お食事ですね。"
    speech = "<audio src=\"{}\"></audio><audio src=\"{}\"></audio>".format(
        audio_url("eat.mp3"),
        audio_url("suffix.mp3")
    )
    card_text = "すぐ用意しますので、くつろいでおまちになってくださいね。"
    close_session = True

    return build_speechlet_response(title, speech, card_text, close_session)

def return_konwaku():
    title = "おいたは、いけませんよ。"
    speech = "<audio src=\"{}\"></audio>".format(
        audio_url("konwaku.mp3")
    )
    card_text = "おいたは、いけませんよ。"
    close_session = True

    return build_speechlet_response(title, speech, card_text, close_session)

def return_cancel():
    title = "いつでもメイドにお申し付け下さいね。"
    speech = "<audio src=\"{}\"></audio>".format(
        audio_url("cancel.mp3")
    )
    card_text = "ご主人様のおやくにたてなくて悲しいです。"
    close_session = True

    return build_speechlet_response(title, speech, card_text, close_session)

def return_goodbye():
    title = "いってらっしゃいませ、ご主人様。"
    speech = "<audio src=\"{}\"></audio>".format(
        audio_url("goodbye.mp3")
    )
    card_text = "いってらっしゃいませ、ご主人様。"
    close_session = True

    return build_speechlet_response(title, speech, card_text, close_session)

def build_speechlet_response(title, speech, card_text, close_session):

    return_message = {
        "outputSpeech": {
            "type": "SSML",
            "ssml": "<speak>{}</speak>".format(speech)
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": card_text
        },
        "shouldEndSession": close_session
    }

    return build_response(return_message)

def build_response(speechlet_response):
    response = {
        'version': '1.0',
        'response': speechlet_response
    }
    print(response)
    return response

# --------------- Utility Functions ------------------

def audio_url(file_name):
    return AUDIO_URL.format(AUDIO_BUCKET, file_name)
