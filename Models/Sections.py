from flask_restful import Resource, Api, request
from db import conn
from .constants import Days, TotalWeeks


class Sections(Resource):
    def put(self):
        try:
            data = request.get_json()
            type = data['section']
            sections = conn.execute("SELECT * FROM sections WHERE type = ?", (type,)).fetchall()
            if len(sections) > 0:
                return {'message': 'Section already exists'}, 400
            conn.execute("INSERT INTO Notes (type, monday, tuesday, wednesday, thursday, friday, saturday, sunday) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (type, chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks))
            notesId = conn.execute("SELECT id FROM Notes WHERE type = ?", (type,)).fetchall()[0][0]
            conn.execute("INSERT INTO Sections (type, notesId) VALUES (?, ?)", (type, notesId))
            conn.commit()
            return {'message': 'Section created successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Invalid data'}, 400

    def delete(self):
        try:
            data = request.get_json()
            type = data['section']
            sections = conn.execute("SELECT * FROM sections WHERE type = ?", (type,)).fetchall()
            if len(sections) == 0:
                return {'message': 'Section not found'}, 404
            conn.execute("DELETE FROM sections WHERE type = ?", (type,))
            conn.execute("DELETE FROM notes WHERE type = ?", (type,))
            conn.commit()
            return {'message': 'Section deleted successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Invalid data'}, 400
