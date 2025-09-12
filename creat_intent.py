import os
import sys
import json
import requests
from dotenv import load_dotenv
from google.cloud import dialogflow


def load_file(full_path):
    url = "https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json"

    response = requests.get(url=url)
    response.raise_for_status()

    with open(full_path, "wb") as file:
        file.write(response.content)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )
    intents_client.create_intent(request={"parent": parent, "intent": intent})


def main():
    load_dotenv()
    project_id = os.getenv("PROJECT_DIALOGFLOW_ID")
    if not project_id:
        sys.exit("Нет id dialogflow")

    base_dir = os.path.dirname(__file__)
    file_name = "questions.json"
    full_path = os.path.join(base_dir, file_name)

    load_file(full_path)

    with open(full_path, "r", encoding="utf-8") as file:
        questions_file = json.load(file)

    for display_name, content in questions_file.items():
        training_phrases_parts = content["questions"]
        message_texts = [content["answer"]]
        create_intent(project_id, display_name,
                      training_phrases_parts, message_texts)


if __name__ == "__main__":
    main()
