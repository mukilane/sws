# Copyright (C) 2018 Mukil Elango
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module to invoke Google Assistant
"""
import concurrent.futures
import json
import logging
import os
import os.path
import sys
import uuid

import click
import grpc
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
import dialogflowtext

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)
from tenacity import retry, stop_after_attempt, retry_if_exception

try:
    from helpers import (
        assistant_helpers,
        audio_helpers,
        device_helpers
    )
except (SystemError, ImportError):
    import assistant_helpers
    import audio_helpers
    import device_helpers


ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
END_OF_UTTERANCE = embedded_assistant_pb2.AssistResponse.END_OF_UTTERANCE
DIALOG_FOLLOW_ON = embedded_assistant_pb2.DialogStateOut.DIALOG_FOLLOW_ON
CLOSE_MICROPHONE = embedded_assistant_pb2.DialogStateOut.CLOSE_MICROPHONE
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5

class SimpleAssistant(object):

    def __init__(self, language_code, device_model_id, device_id,
                 conversation_stream,
                 channel, deadline_sec, device_handler):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_stream = conversation_stream
        self.conversation_state = None
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(
            channel
        )
        self.deadline = deadline_sec
        self.device_handler = device_handler

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False
        self.conversation_stream.close()

    def is_grpc_error_unavailable(e):
        is_grpc_error = isinstance(e, grpc.RpcError)
        if is_grpc_error and (e.code() == grpc.StatusCode.UNAVAILABLE):
            logging.error('grpc unavailable error: %s', e)
            return True
        return False

    @retry(reraise=True, stop=stop_after_attempt(3),
           retry=retry_if_exception(is_grpc_error_unavailable))
    def assist(self):
        """Send a voice request to the Assistant and playback the response.
        Returns: True if conversation should continue.
        """
        continue_conversation = False
        device_actions_futures = []
        transcript = ''

        self.conversation_stream.start_recording()
        logging.info('Recording audio request.')

        def iter_assist_requests():
            for c in self.gen_assist_requests():
                assistant_helpers.log_assist_request_without_audio(c)
                yield c
            self.conversation_stream.start_playback()

        # This generator yields AssistResponse proto messages
        # received from the gRPC Google Assistant API.
        for resp in self.assistant.Assist(iter_assist_requests(),
                                          self.deadline):

            if resp.event_type == END_OF_UTTERANCE:
                logging.info(transcript)
                # print(dialogflowtext.get_intent(str(transcript)))
                self.conversation_stream.stop_recording()
            if resp.speech_results:
                transcript = ''.join(r.transcript for r in resp.speech_results)
            if len(resp.audio_out.audio_data) > 0:
                self.conversation_stream.write(resp.audio_out.audio_data)
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                logging.debug('Updating conversation state.')
                self.conversation_state = conversation_state
            if resp.dialog_state_out.volume_percentage != 0:
                volume_percentage = resp.dialog_state_out.volume_percentage
                logging.info('Setting volume to %s%%', volume_percentage)
                self.conversation_stream.volume_percentage = volume_percentage
            if resp.dialog_state_out.microphone_mode == DIALOG_FOLLOW_ON:
                continue_conversation = True
                logging.info('Expecting follow-on query from user.')
            elif resp.dialog_state_out.microphone_mode == CLOSE_MICROPHONE:
                continue_conversation = False
            if resp.device_action.device_request_json:
                device_request = json.loads(
                    resp.device_action.device_request_json
                )
                fs = self.device_handler(device_request)
                if fs:
                    device_actions_futures.extend(fs)

        if len(device_actions_futures):
            logging.info('Waiting for device executions to complete.')
            concurrent.futures.wait(device_actions_futures)

        logging.info('Finished playing assistant response.')
        self.conversation_stream.stop_playback()
        return continue_conversation

    def gen_assist_requests(self):
        """Yields: AssistRequest messages to send to the API."""

        dialog_state_in = embedded_assistant_pb2.DialogStateIn(
            language_code=self.language_code,
            conversation_state=b''
        )
        if self.conversation_state:
            logging.debug('Sending conversation state.')
            dialog_state_in.conversation_state = self.conversation_state
        config = embedded_assistant_pb2.AssistConfig(
            audio_in_config=embedded_assistant_pb2.AudioInConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
            ),
            audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
                volume_percentage=self.conversation_stream.volume_percentage,
            ),
            dialog_state_in=dialog_state_in,
            device_config=embedded_assistant_pb2.DeviceConfig(
                device_id=self.device_id,
                device_model_id=self.device_model_id,
            )
        )
        # The first AssistRequest must contain the AssistConfig
        # and no audio data.
        yield embedded_assistant_pb2.AssistRequest(config=config)
        for data in self.conversation_stream:
            # Subsequent requests need audio data, but not config.
            yield embedded_assistant_pb2.AssistRequest(audio_in=data)

class ActionAssistant(object):

    def __init__(self, language_code, device_model_id, device_id,
                 conversation_stream,
                 channel, deadline_sec, device_handler):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_stream = conversation_stream
        self.conversation_state = None
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(
            channel
        )
        self.deadline = deadline_sec
        self.device_handler = device_handler

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False
        self.conversation_stream.close()

    def is_grpc_error_unavailable(e):
        is_grpc_error = isinstance(e, grpc.RpcError)
        if is_grpc_error and (e.code() == grpc.StatusCode.UNAVAILABLE):
            logging.error('grpc unavailable error: %s', e)
            return True
        return False

    @retry(reraise=True, stop=stop_after_attempt(3),
           retry=retry_if_exception(is_grpc_error_unavailable))
    def assist(self):
        """Send a voice request to the Assistant and playback the response.
        Returns: True if conversation should continue.
        """
        continue_conversation = False
        device_actions_futures = []
        transcript = ''

        self.conversation_stream.start_recording()
        logging.info('Recording audio request.')

        def iter_assist_requests():
            for c in self.gen_assist_requests():
                assistant_helpers.log_assist_request_without_audio(c)
                yield c
            self.conversation_stream.start_playback()

        # This generator yields AssistResponse proto messages
        # received from the gRPC Google Assistant API.
        for resp in self.assistant.Assist(iter_assist_requests(),
                                          self.deadline):

            if resp.event_type == END_OF_UTTERANCE:
                logging.info(transcript)
                print(dialogflowtext.get_intent(str(transcript)))
                self.conversation_stream.stop_recording()
            if resp.speech_results:
                transcript = ''.join(r.transcript for r in resp.speech_results)
            if len(resp.audio_out.audio_data) > 0:
                self.conversation_stream.write(resp.audio_out.audio_data)
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                logging.debug('Updating conversation state.')
                self.conversation_state = conversation_state
            if resp.dialog_state_out.volume_percentage != 0:
                volume_percentage = resp.dialog_state_out.volume_percentage
                logging.info('Setting volume to %s%%', volume_percentage)
                self.conversation_stream.volume_percentage = volume_percentage
            if resp.dialog_state_out.microphone_mode == DIALOG_FOLLOW_ON:
                continue_conversation = True
                logging.info('Expecting follow-on query from user.')
            elif resp.dialog_state_out.microphone_mode == CLOSE_MICROPHONE:
                continue_conversation = False
            if resp.device_action.device_request_json:
                device_request = json.loads(
                    resp.device_action.device_request_json
                )
                fs = self.device_handler(device_request)
                if fs:
                    device_actions_futures.extend(fs)

        if len(device_actions_futures):
            logging.info('Waiting for device executions to complete.')
            concurrent.futures.wait(device_actions_futures)

        logging.info('Finished playing assistant response.')
        self.conversation_stream.stop_playback()
        return continue_conversation

    def gen_assist_requests(self):
        """Yields: AssistRequest messages to send to the API."""

        dialog_state_in = embedded_assistant_pb2.DialogStateIn(
            language_code=self.language_code,
            conversation_state=b''
        )
        if self.conversation_state:
            logging.debug('Sending conversation state.')
            dialog_state_in.conversation_state = self.conversation_state
        config = embedded_assistant_pb2.AssistConfig(
            audio_in_config=embedded_assistant_pb2.AudioInConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
            ),
            audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
                volume_percentage=self.conversation_stream.volume_percentage,
            ),
            dialog_state_in=dialog_state_in,
            device_config=embedded_assistant_pb2.DeviceConfig(
                device_id=self.device_id,
                device_model_id=self.device_model_id,
            )
        )
        # The first AssistRequest must contain the AssistConfig
        # and no audio data.
        yield embedded_assistant_pb2.AssistRequest(config=config)
        for data in self.conversation_stream:
            # Subsequent requests need audio data, but not config.
            yield embedded_assistant_pb2.AssistRequest(audio_in=data)


def main(once, action, *args, **kwargs):
    api_endpoint = ASSISTANT_API_ENDPOINT
    credentials = os.path.join(click.get_app_dir('google-oauthlib-tool'),
                               'credentials.json')
    project_id = 'project-harmony'
    device_model_id = 'base-model'
    device_id = str(uuid.uuid1())
    device_config = os.path.join(
        click.get_app_dir('googlesamples-assistant'),
        'device_config.json')
    lang = 'en-US'
    verbose = False
    audio_sample_rate = audio_helpers.DEFAULT_AUDIO_SAMPLE_RATE
    audio_sample_width = audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH
    audio_iter_size = audio_helpers.DEFAULT_AUDIO_ITER_SIZE
    audio_block_size = audio_helpers.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE
    audio_flush_size = audio_helpers.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE
    grpc_deadline = DEFAULT_GRPC_DEADLINE
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    try:
        with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        logging.error('Error loading credentials: %s', e)
        logging.error('Run google-oauthlib-tool to initialize '
                      'new OAuth 2.0 credentials.')
        sys.exit(-1)

    # Create an authorized gRPC channel.
    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, api_endpoint)
    logging.info('Connecting to %s', api_endpoint)

    # Configure audio source and sink.
    audio_device = None
    audio_source = audio_device = (
        audio_device or audio_helpers.SoundDeviceStream(
            sample_rate=audio_sample_rate,
            sample_width=audio_sample_width,
            block_size=audio_block_size,
            flush_size=audio_flush_size
        )
    )
    audio_sink = audio_device = (
        audio_device or audio_helpers.SoundDeviceStream(
            sample_rate=audio_sample_rate,
            sample_width=audio_sample_width,
            block_size=audio_block_size,
            flush_size=audio_flush_size
        )
    )
    # Create conversation stream with the given audio source and sink.
    conversation_stream = audio_helpers.ConversationStream(
        source=audio_source,
        sink=audio_sink,
        iter_size=audio_iter_size,
        sample_width=audio_sample_width,
    )

    device_handler = device_helpers.DeviceRequestHandler(device_id)

    @device_handler.command('action.devices.commands.OnOff')
    def onoff(on):
        if on:
            logging.info('Turning device on')
        else:
            logging.info('Turning device off')
    if action:
        assistant = ActionAssistant(lang, device_model_id, device_id,
                                conversation_stream,
                                grpc_channel, grpc_deadline,
                                device_handler)
    else:
        assistant = SimpleAssistant(lang, device_model_id, device_id,
                                conversation_stream,
                                grpc_channel, grpc_deadline,
                                device_handler)

    return assistant
    # wait_for_user_trigger = not once
    # while True:
    #     if wait_for_user_trigger:
    #         click.pause(info='Press Enter to send a new request...')
    #     continue_conversation = assistant.assist()
    #     # wait for user trigger if there is no follow-up turn in
    #     # the conversation.
    #     wait_for_user_trigger = not continue_conversation

    #     # If we only want one conversation, break.
    #     if once and (not continue_conversation):
    #         break       


if __name__ == '__main__':
    assistant = main(False, False)
    print("Ready")
    while True:
        continue_conversation = assistant.assist()

        if not continue_conversation:
            break
