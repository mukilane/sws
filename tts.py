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

from google_speech import Speech


def speak(text):
    lang = "en-US"
    speech = Speech(text, lang)
    # SOX Effects http://sox.sourceforge.net/sox.html#EFFECTS
    sox_effects = ("speed", "1")
    speech.play(sox_effects)


if __name__ == "__main__":
    speak("Hello world")
