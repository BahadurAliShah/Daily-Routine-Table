from flask_restful import Resource, Api, request
from db import conn


class Notes(Resource):
    def post(self):
        try:
            data = request.get_json()
            type = data['type']
            week = int(data['week'])
            id = data['id']
            monday = data['monday']
            tuesday = data['tuesday']
            wednesday = data['wednesday']
            thursday = data['thursday']
            friday = data['friday']
            saturday = data['saturday']
            sunday = data['sunday']
            Notes = conn.execute("SELECT * FROM Notes WHERE id = ?", (id,)).fetchall()

            newMonday = Notes[0][2].split(chr(255))
            newTuesday = Notes[0][3].split(chr(255))
            newWednesday = Notes[0][4].split(chr(255))
            newThursday = Notes[0][5].split(chr(255))
            newFriday = Notes[0][6].split(chr(255))
            newSaturday = Notes[0][7].split(chr(255))
            newSunday = Notes[0][8].split(chr(255))

            newMonday[week] = monday
            newTuesday[week] = tuesday
            newWednesday[week] = wednesday
            newThursday[week] = thursday
            newFriday[week] = friday
            newSaturday[week] = saturday
            newSunday[week] = sunday

            newMonday = chr(255).join(newMonday)
            newTuesday = chr(255).join(newTuesday)
            newWednesday = chr(255).join(newWednesday)
            newThursday = chr(255).join(newThursday)
            newFriday = chr(255).join(newFriday)
            newSaturday = chr(255).join(newSaturday)
            newSunday = chr(255).join(newSunday)

            conn.execute("UPDATE Notes SET monday = ?, tuesday = ?, wednesday = ?, thursday = ?, friday = ?, saturday = ?, sunday = ? WHERE id = ?", (newMonday, newTuesday, newWednesday, newThursday, newFriday, newSaturday, newSunday, id))
            conn.commit()

            return {'message': 'Notes updated successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Invalid data'}, 400
