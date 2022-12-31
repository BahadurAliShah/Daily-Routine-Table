from flask_restful import Resource, Api, request
from db import conn
import json
from datetime import datetime

Days = {
    'monday': 2,
    'tuesday': 3,
    'wednesday': 4,
    'thursday': 5,
    'friday': 6,
    'saturday': 7,
    'sunday': 8
}

class Dailies(Resource):
    def __init__(self):
        notes = conn.execute("SELECT * FROM Notes").fetchall()
        if len(notes) == 0:
            conn.execute("INSERT INTO Notes (type, monday, tuesday, wednesday, thursday, friday, saturday, sunday) VALUES ('default', '', '', '', '', '', '', '')")
            conn.commit()

        sections = conn.execute("SELECT * FROM Sections").fetchall()
        if len(sections) == 0:
            notesID = conn.execute("SELECT id FROM Notes WHERE type = 'default'").fetchall()[0][0]
            conn.execute("INSERT INTO Sections (type, notesId) VALUES ('default', ?)", (notesID,))
            conn.commit()



    def get(self):
        dailies = conn.execute("SELECT * FROM dailies").fetchall()
        dict_dailies = []
        if len(dailies) > 0:
            for daily in dailies:
                dict_dailies.append({
                    'id': daily[0],
                    'title': daily[1],
                    'monday': daily[2].split(','),
                    'tuesday': daily[3].split(','),
                    'wednesday': daily[4].split(','),
                    'thursday': daily[5].split(','),
                    'friday': daily[6].split(','),
                    'saturday': daily[7].split(','),
                    'sunday': daily[8].split(','),
                    'type': daily[9]
                })

        notes = conn.execute("SELECT * FROM Notes").fetchall()
        dict_notes = []
        if len(notes) > 0:
            for note in notes:
                dict_notes.append({
                    'id': note[0],
                    'type': note[1],
                    'monday': note[2],
                    'tuesday': note[3],
                    'wednesday': note[4],
                    'thursday': note[5],
                    'friday': note[6],
                    'saturday': note[7],
                    'sunday': note[8]
                })

        sections = conn.execute("SELECT * FROM Sections").fetchall()
        dict_sections = []
        if len(sections) > 0:
            for section in sections:
                dict_sections.append({
                    'id': section[0],
                    'type': section[1],
                    'notesID': section[2]
                })
        return {'todos': dict_dailies, 'notes': dict_notes, 'sections': dict_sections}, 200

    def post(self):
        try:
            data = request.get_json()
            taskId = data['taskId']
            day = data['day']
            index = int(data['index'])
            isChecked = data['isChecked']
            dailies = conn.execute("SELECT * FROM dailies WHERE id = ?", (taskId,)).fetchall()
            if len(dailies) == 0:
                return {'message': 'Task not found'}, 404
            nday = Days[day]

            TaskUpdated = dailies[0][nday].split(',')
            if isChecked:
                TaskUpdated[index] = '1'
            else:
                TaskUpdated[index] = '0'
            TaskUpdated = ','.join(TaskUpdated)
            query = f"UPDATE dailies SET {day} = '{TaskUpdated}' WHERE id = {taskId}"
            conn.execute(query)
            conn.commit()
            return {'message': 'Task updated successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Invalid data'}, 400

    def put(self):
        try:
            data = request.get_json()
            title = data['title']
            section = data['section']
            monday = ['0' for i in range(int(data['monday']))]
            tuesday = ['0' for i in range(int(data['tuesday']))]
            wednesday = ['0' for i in range(int(data['wednesday']))]
            thursday = ['0' for i in range(int(data['thursday']))]
            friday = ['0' for i in range(int(data['friday']))]
            saturday = ['0' for i in range(int(data['saturday']))]
            sunday = ['0' for i in range(int(data['sunday']))]
            monday = ','.join(monday)
            tuesday = ','.join(tuesday)
            wednesday = ','.join(wednesday)
            thursday = ','.join(thursday)
            friday = ','.join(friday)
            saturday = ','.join(saturday)
            sunday = ','.join(sunday)

            query = f"INSERT INTO dailies (title, monday, tuesday, wednesday, thursday, friday, saturday, sunday, type) VALUES ('{title}', '{monday}', '{tuesday}', '{wednesday}', '{thursday}', '{friday}', '{saturday}', '{sunday}', '{section}')"
            conn.execute(query)
            conn.commit()
            return {'message': 'Task created successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Invalid data'}, 400

    def delete(self):
        try:
            data = request.get_json()
            taskId = data['taskId']
            query = f"DELETE FROM dailies WHERE id = {taskId}"
            conn.execute(query)
            conn.commit()
            return {'message': 'Task deleted successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Invalid data'}, 400
