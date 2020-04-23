import os
import logging
import re
import unicodedata
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from tempfile import gettempdir
from contextlib import closing

from aqt import gui_hooks
from aqt import mw
from anki.media import MediaManager


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def button_pressed(self):
    """
    The button hook
    """
    cfg = mw.addonManager.getConfig(__name__)
    txt = self.note.fields[field_name_to_idx(self.note, cfg["txt_field"])]
    audio = please_say(txt)
    if audio is not None:
        add_sound_to_field(self.note, cfg['audio_field'], audio)
        self.loadNoteKeepingFocus()


def add_audio_button(buttons, editor):
    """
    Add the button to the gui
    """
    buttons.append(
        editor.addButton(icon="paperclip", cmd="add_audio",
                         func=button_pressed, label="Add audio"),
    )
    return buttons


def field_name_to_idx(note, field):
    """
    Transforms fieldname of a node to it's index
    """
    note_model = note.model()
    note_fields = mw.col.models.fieldNames(note_model)
    return note_fields.index(field)


def import_file(file_path):
    """
    Imports the image; Returns the filename
    """
    media_mgt = MediaManager(mw.col, False)
    return media_mgt.addFile(file_path)


def add_sound_to_field(note, fieldname, file_path):
    """
    Adds an image to a field and returns the filename
    """
    filename = import_file(file_path)
    field_idx = field_name_to_idx(note, fieldname)
    note.fields[field_idx] = f'[sound:{filename}]'
    return filename


def please_say(text):
    cfg = mw.addonManager.getConfig(__name__)
    polly_client = boto3.Session(
                    aws_access_key_id=cfg['access_id'],
                    aws_secret_access_key=cfg['access_key'],
                    region_name=cfg['region']).client('polly')

    try:
        # Request speech synthesis
        response = polly_client.synthesize_speech(VoiceId=cfg['voice'],
                        OutputFormat='mp3',
                        Text = text,
                        Engine = cfg['engine'])
    except (BotoCoreError, ClientError) as error:
        logging.error(error)
        return None

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), slugify(text) + '.mp3')

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
                return output
            except IOError as error:
                # Could not write to file, exit gracefully
                logging.error(error)
                return None
    return None


gui_hooks.editor_did_init_buttons.append(add_audio_button)
