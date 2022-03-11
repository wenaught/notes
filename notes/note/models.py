"""This module defines the models and schemas used by the 'note' entities of the API."""
import os

from umongo import Document, fields
from umongo.frameworks import PyMongoInstance, MongoMockInstance
from marshmallow.validate import Length

note_umongo_instance = PyMongoInstance() if not os.getenv("MOCK_MONGO") else MongoMockInstance()


@note_umongo_instance.register
class Note(Document):
    """A MongoDB model for the 'note' document."""
    title = fields.StrField(
        required=True,
        metadata={
            'title': 'Note title',
            'description': 'Optional title of the note'
        }
    )
    text = fields.StrField(
        required=True,
        validate=Length(min=1),
        metadata={
            'title': 'Note text',
            'description': 'Text of the note'
        }
    )
    added_timestamp = fields.DateTimeField(
        metadata={
            'title': 'Time of creation',
            'description': 'Timestamp added to the note at the time of creation'
        }
    )
    modified_timestamp = fields.DateTimeField(
        metadata={
            'title': 'Time of last modification',
            'description': 'Timestamp of the last modification'
        }
    )

    class Meta:
        collection_name = 'notes'
        indexes = ('title',)


NoteSchema = Note.schema.as_marshmallow_schema()


class InNoteSchema(NoteSchema):
    """A schema that defines input fields for a 'note' document."""

    class Meta:
        fields = ('title', 'text')


class OutNoteSchema(NoteSchema):
    """A schema that defines output fields for a 'note' document."""

    class Meta:
        fields = ('title', 'added_timestamp', 'modified_timestamp', 'text')
