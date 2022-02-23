"""This module defines the models and schemas used by the API."""

from umongo import Document, fields
from umongo.frameworks import PyMongoInstance

instance = PyMongoInstance()


@instance.register
class Note(Document):
    """A MongoDB model for the 'note' document."""
    name = fields.StrField()
    added_timestamp = fields.DateTimeField()
    modified_timestamp = fields.DateTimeField()
    text = fields.StrField()

    class Meta:
        collection_name = 'notes'
        indexes = ('name',)


NoteSchema = Note.schema.as_marshmallow_schema()


class InNoteSchema(NoteSchema):
    """A schema that defines input fields for a 'note' document."""

    class Meta:
        fields = ('name', 'text')


class OutNoteSchema(NoteSchema):
    """A schema that defines output fields for a 'note' document."""

    class Meta:
        fields = ('name', 'added_timestamp', 'modified_timestamp', 'text')
