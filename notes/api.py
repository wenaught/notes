"""This module defines the /note routes."""

import datetime

from apiflask import APIBlueprint, input, output

from notes.models import Note, InNoteSchema, OutNoteSchema

blueprint = APIBlueprint('notes', __name__)


@blueprint.post('/notes')
@input(InNoteSchema)
@output(OutNoteSchema, 201)
def post_note(data: dict) -> Note:
    """Post a note to the API."""
    note = Note(**data)
    note.added_timestamp = note.modified_timestamp = datetime.datetime.now()
    note.commit()
    return note


@blueprint.get('/notes/<string:note_name>')
@output(OutNoteSchema)
def get_note(note_name: str) -> Note:
    """Get a note from the API."""
    note = Note.find_one({'name': note_name})
    return note


@blueprint.get('/notes')
@output(OutNoteSchema(many=True))
def get_notes() -> list[Note]:
    """Get all notes from the API."""
    return list(Note.find())
