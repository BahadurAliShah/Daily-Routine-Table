from flask_restful import Resource, Api, request
from db import conn
import json
from datetime import datetime
from .constants import Days, TotalWeeks

class Dailies(Resource):
    # def get(self, week=0):
    #     dailies = conn.execute("SELECT * FROM dailies").fetchall()
    #     dict_dailies = []
    #     if len(dailies) > 0:
    #         for daily in dailies:
    #             dict_dailies.append({
    #                 'id': daily[0],
    #                 'title': daily[1],
    #                 'monday': daily[2].split(chr(255))[week].split(','),
    #                 'tuesday': daily[3].split(chr(255))[week].split(','),
    #                 'wednesday': daily[4].split(chr(255))[week].split(','),
    #                 'thursday': daily[5].split(chr(255))[week].split(','),
    #                 'friday': daily[6].split(chr(255))[week].split(','),
    #                 'saturday': daily[7].split(chr(255))[week].split(','),
    #                 'sunday': daily[8].split(chr(255))[week].split(','),
    #                 'type': daily[9]
    #             })
    #
    #     notes = conn.execute("SELECT * FROM Notes").fetchall()
    #     dict_notes = []
    #     if len(notes) > 0:
    #         for note in notes:
    #             dict_notes.append({
    #                 'id': note[0],
    #                 'type': note[1],
    #                 'monday': note[2].split(chr(255))[week],
    #                 'tuesday': note[3].split(chr(255))[week],
    #                 'wednesday': note[4].split(chr(255))[week],
    #                 'thursday': note[5].split(chr(255))[week],
    #                 'friday': note[6].split(chr(255))[week],
    #                 'saturday': note[7].split(chr(255))[week],
    #                 'sunday': note[8].split(chr(255))[week]
    #             })
    #
    #     sections = conn.execute("SELECT * FROM Sections").fetchall()
    #     dict_sections = []
    #     if len(sections) > 0:
    #         for section in sections:
    #             dict_sections.append({
    #                 'id': section[0],
    #                 'type': section[1],
    #                 'notesID': section[2]
    #             })
    #     return {'todos': dict_dailies, 'notes': dict_notes, 'sections': dict_sections}, 200

    def post(self):
        try:
            data = request.get_json()
            taskId = data['taskId']
            week = int(data['week'])
            day = data['day']
            index = int(data['index'])
            isChecked = data['isChecked']
            dailies = conn.execute("SELECT * FROM dailies WHERE id = ?", (taskId,)).fetchall()
            if len(dailies) == 0:
                return {'message': 'Task not found'}, 404
            nday = Days[day]

            TaskUpdated = dailies[0][nday].split(chr(255))
            for i in range(0, TotalWeeks):
                TaskUpdated[i] = TaskUpdated[i].split(',')
            if isChecked:
                TaskUpdated[week][index] = '1'
            else:
                TaskUpdated[week][index] = '0'
            for i in range(0, TotalWeeks):
                TaskUpdated[i] = ','.join(TaskUpdated[i])
            TaskUpdated = chr(255).join(TaskUpdated)
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
            monday = [monday for i in range(TotalWeeks)]
            monday = chr(255).join(monday)
            tuesday = ','.join(tuesday)
            tuesday = [tuesday for i in range(TotalWeeks)]
            tuesday = chr(255).join(tuesday)
            wednesday = ','.join(wednesday)
            wednesday = [wednesday for i in range(TotalWeeks)]
            wednesday = chr(255).join(wednesday)
            thursday = ','.join(thursday)
            thursday = [thursday for i in range(TotalWeeks)]
            thursday = chr(255).join(thursday)
            friday = ','.join(friday)
            friday = [friday for i in range(TotalWeeks)]
            friday = chr(255).join(friday)
            saturday = ','.join(saturday)
            saturday = [saturday for i in range(TotalWeeks)]
            saturday = chr(255).join(saturday)
            sunday = ','.join(sunday)
            sunday = [sunday for i in range(TotalWeeks)]
            sunday = chr(255).join(sunday)
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


class Daily(Resource):
    def __init__(self):
        notes = conn.execute("SELECT * FROM Notes").fetchall()
        if len(notes) == 0:
            conn.execute("INSERT INTO Notes (type, monday, tuesday, wednesday, thursday, friday, saturday, sunday) VALUES ('default', ?, ?, ?, ?, ?, ?, ?)", (chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks, chr(255)*TotalWeeks))
            conn.commit()

        sections = conn.execute("SELECT * FROM Sections").fetchall()
        if len(sections) == 0:
            notesID = conn.execute("SELECT id FROM Notes WHERE type = 'default'").fetchall()[0][0]
            conn.execute("INSERT INTO Sections (type, notesId) VALUES ('default', ?)", (notesID,))
            conn.commit()

    def get(self, week=0):
            dailies = conn.execute("SELECT * FROM dailies").fetchall()
            dict_dailies = []
            if len(dailies) > 0:
                for daily in dailies:
                    dict_dailies.append({
                        'id': daily[0],
                        'title': daily[1],
                        'monday': daily[2].split(chr(255))[week].split(','),
                        'tuesday': daily[3].split(chr(255))[week].split(','),
                        'wednesday': daily[4].split(chr(255))[week].split(','),
                        'thursday': daily[5].split(chr(255))[week].split(','),
                        'friday': daily[6].split(chr(255))[week].split(','),
                        'saturday': daily[7].split(chr(255))[week].split(','),
                        'sunday': daily[8].split(chr(255))[week].split(','),
                        'type': daily[9]
                    })

            notes = conn.execute("SELECT * FROM Notes").fetchall()
            dict_notes = []
            if len(notes) > 0:
                for note in notes:
                    dict_notes.append({
                        'id': note[0],
                        'type': note[1],
                        'monday': note[2].split(chr(255))[week],
                        'tuesday': note[3].split(chr(255))[week],
                        'wednesday': note[4].split(chr(255))[week],
                        'thursday': note[5].split(chr(255))[week],
                        'friday': note[6].split(chr(255))[week],
                        'saturday': note[7].split(chr(255))[week],
                        'sunday': note[8].split(chr(255))[week]
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
