from flask import Flask, request, jsonify

app = Flask(__name__)

hospital_data = {
    'departments': {},
    'appointments': {},
    'tokens': {}
}
name_number_list=[]

#{ departments : {'A': ['D1', 'D2'], 'B': ['D3', 'D4']}, 'appointments': {'A': {}}, 'tokens': {'A': 1}}   }
# hospital_data['departments']['A']='D1'

@app.route('/register_department', methods=['POST'])
def register_department():
    data = request.get_json()
    department_name = data.get('department_name')
    doctors = data.get('doctors')
    
    if department_name and doctors:
        hospital_data['departments'][department_name] = doctors
        hospital_data['appointments'][department_name] = {}
        hospital_data['tokens'][department_name] = 1
        return jsonify({'message': 'Department registered successfully!'})
    else:
        return jsonify({'error': 'Missing department name or doctors list'}), 400

@app.route('/get_departments', methods=['GET'])
def get_departments():
    return jsonify(list(hospital_data['departments'].keys()))

@app.route('/get_doctors/<department>', methods=['GET'])
def get_doctors(department):
    doctors = hospital_data['departments'].get(department, [])
    return jsonify(doctors)

@app.route('/appointments/<department>', methods=['GET'])
def get_appointments(department):
    appointments = hospital_data['appointments'].get(department, {})
    return jsonify(appointments)


@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.get_json()
    department_name = data.get('department_name')
    visitor_name = data.get('visitor_name')
    visitor_mobile = data.get('visitor_mobile')
    name_number=(visitor_name,visitor_mobile)
    if name_number not in name_number_list:
        name_number_list.append(name_number)
    else:
        return jsonify({'message': 'Same name and mobile number have already fixed a appointment .. Plz check the appointments in hospital portal !!!'}), 400

    if department_name and visitor_name and visitor_mobile:
        department_doctors = hospital_data['departments'].get(department_name)
        if department_doctors:
            doctor = department_doctors[hospital_data['tokens'][department_name] % len(department_doctors)]
            token = hospital_data['tokens'][department_name]
            
            appointment = {
                'visitor_name': visitor_name,
                'visitor_mobile': visitor_mobile,
                'doctor': doctor,
                'token': token
            }
            
            hospital_data['appointments'][department_name][token] = appointment
            hospital_data['tokens'][department_name] += 1
            
            return jsonify({'message': 'Appointment booked successfully!', 'token': token})
        else:
            return jsonify({'message': 'Department not found'}), 404
    else:
        return jsonify({'message': 'Missing required data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
