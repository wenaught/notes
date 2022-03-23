"""This module defines the /note routes."""

import datetime

from apiflask import APIBlueprint, abort

from notes.note.models import Note, InNoteSchema, OutNoteSchema

note_blueprint = APIBlueprint('notes', __name__,
                              url_prefix='/note',
                              tag={'name': 'Notes', 'description': 'Interaction with the notes'})


@note_blueprint.post('')
@note_blueprint.input(InNoteSchema)
@note_blueprint.output(OutNoteSchema, 201, description="Newly created note")
def post_note(data: dict) -> Note:
    """Post a Note

    Post a note with given title and text to the API.
    """
    note = Note(**data)
    note.added_timestamp = note.modified_timestamp = datetime.datetime.now()
    note.commit()
    return note


@note_blueprint.get('/<string:title>')
@note_blueprint.output(OutNoteSchema)
@note_blueprint.doc(responses=[200, 404])
def get_note(title: str) -> Note:
    """Get a Note

    Get a note from the API.
    """
    note = Note.find_one({'title': title})
    if not note:
        abort(404)
    return note


@note_blueprint.get('')
@note_blueprint.output(OutNoteSchema(many=True))
def get_notes() -> list[Note]:
    """Get All Notes

    Get all notes from the API.
    """
    return list(Note.find())
