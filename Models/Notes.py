from flask_restful import Resource, Api, request
from db import conn


class Notes(Resource):
    def post(self):
        try:
            data = request.get_json()
            type = data['type']
            id = data['id']
            monday = data['monday']
            tuesday = data['tuesday']
            wednesday = data['wednesday']
            thursday = data['thursday']
            friday = data['friday']
            saturday = data['saturday']
            sunday = data['sunday']
            conn.execute("UPDATE Notes SET monday = ?, tuesday = ?, wednesday = ?, thursday = ?, friday = ?, saturday = ?, sunday = ? WHERE id = ?", (monday, tuesday, wednesday, thursday, friday, saturday, sunday, id,))
            conn.commit()
            return {'message': 'Notes updated successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Invalid data'}, 400
