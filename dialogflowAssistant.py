import argparse
import uuid

import dialogflow

import audio
from config_reader import config

PROJECT_ID = config.get('GOOGLE', 'GOOGLE_CLOUD_PROJECT_ID')


class DialogflowAssistant(object):

    def __init__(self):
        self.project_id = PROJECT_ID
        self.session_id = str(uuid.uuid4())
        self.session_client = dialogflow.SessionsClient()
        self.audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
        self.sample_rate_hertz = 44100
        self.language_code = "en-US"
        self.audio_file_path = "speech.wav"
        self.session = self.session_client.session_path(self.project_id, self.session_id)
        print('Session path: {}\n'.format(self.session))

    def detect(self):
        """Returns the result of detect intent with an audio file as input.
        Using the same `session_id` between requests allows continuation
        of the conversaion."""
        audio.record()

        with open(self.audio_file_path, 'rb') as audio_file:
            input_audio = audio_file.read()

        audio_config = dialogflow.types.InputAudioConfig(
            audio_encoding=self.audio_encoding,
            language_code=self.language_code,
            sample_rate_hertz=self.sample_rate_hertz)
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        response = self.session_client.detect_intent(
            session=self.session, query_input=query_input,
            input_audio=input_audio)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))

        return response.query_result.intent.display_name


if __name__ == '__main__':
    assistant = DialogflowAssistant()
    assistant.detect()
