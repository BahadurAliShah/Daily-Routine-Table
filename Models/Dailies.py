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
    'sunday': 1
}

class Dailies(Resource):
    def get(self):
        dailies = conn.execute("SELECT * FROM dailies").fetchall()
        dict_dailies = []
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
                'sunday': daily[8].split(',')
            })
        return dict_dailies

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
            monday = ['0' for i in range(int(data['monday']))]
            monday = ','.join(monday)
            tuesday = ['0' for i in range(int(data['tuesday']))]
            tuesday = ','.join(tuesday)
            wednesday = ['0' for i in range(int(data['wednesday']))]
            wednesday = ','.join(wednesday)
            thursday = ['0' for i in range(int(data['thursday']))]
            thursday = ','.join(thursday)
            friday = ['0' for i in range(int(data['friday']))]
            friday = ','.join(friday)
            saturday = ['0' for i in range(int(data['saturday']))]
            saturday = ','.join(saturday)
            sunday = ['0' for i in range(int(data['sunday']))]
            sunday = ','.join(sunday)

            query = f"INSERT INTO dailies (title, monday, tuesday, wednesday, thursday, friday, saturday, sunday) VALUES ('{title}', '{monday}', '{tuesday}', '{wednesday}', '{thursday}', '{friday}', '{saturday}', '{sunday}')"
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
