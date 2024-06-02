from flask import Flask, request, jsonify,send_from_directory
from flask_restful import Api, Resource
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Traveller
from datetime import datetime, date
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app) 


@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')


class TravellerResource(Resource):
    def post(self):
        session = SessionLocal()
        data = request.json
        
        travel_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if travel_date < date.today():
            return {'details': "date should be today or a future date", 'status': 400}, 400
        

        existing_traveller = session.query(Traveller).filter_by(phone_number=data['phone_number']).first()
        if existing_traveller:
            session.close()
            return {'details': "phone number already exists", 'status': 400}, 400

        new_traveller = Traveller(
            full_name=data['full_name'],
            phone_number=data['phone_number'],
            place_from=data['place_from'],
            place_to=data['place_to'],
            date=travel_date
        )
        
        session.add(new_traveller)
        session.commit()
        

        matching_travellers = session.query(Traveller).filter(
            Traveller.date == new_traveller.date,
            Traveller.place_from == new_traveller.place_from,
            Traveller.place_to == new_traveller.place_to,
            Traveller.id != new_traveller.id
        ).all()
        
        session.close()
        
        if not matching_travellers:
            return {'details': None, 'status': 200}, 200
        
        return {
            'details': [{
                'full_name': traveller.full_name,
                'phone_number': traveller.phone_number,
                'place_from': traveller.place_from,
                'place_to': traveller.place_to,
                'date': traveller.date.strftime('%Y-%m-%d')
            } for traveller in matching_travellers],
            'status': 200
        }, 200

api.add_resource(TravellerResource, '/travellers')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
