import os
import sys
import vk_api
import random
from dotenv import load_dotenv
from google.cloud import dialogflow
from vk_api.longpoll import VkLongPoll, VkEventType


# def echo(event, api):
#     api.messages.send(
#         user_id=event.user_id,
#         message=event.text,
#         random_id=random.randint(1, 1000)
#     )


def get_dialogflow_response(project_id, session_id, text, lang_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=lang_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input})

    if response.query_result.intent.is_fallback:
        return None
    return response.query_result.fulfillment_text


def handle_message(event, api, project_id, lang_code):
    session_id = event.user_id
    text = event.text
    response_text = get_dialogflow_response(
        project_id, session_id, text, lang_code)
    if response_text:
        api.messages.send(
            user_id=session_id,
            message=response_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    token = os.getenv("VK_TOKEN")
    if not token:
        sys.exit("Нет vk token")

    project_id = os.getenv("PROJECT_DIALOGFLOW_ID")
    if not project_id:
        sys.exit("Нет id dialogflow")

    lang_code = "ru"

    vk_session = vk_api.VkApi(token=token)
    api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, api, project_id, lang_code)


if __name__ == "__main__":
    main()
