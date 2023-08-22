from flask import Flask, request, render_template

app = Flask(__name__)

departments = []
appointments = []
tokens = {}

class Department:
    def __init__(self, name, doctors):
        self.name = name
        self.doctors = doctors

class Appointment:
    def __init__(self, department, doctor, name, mobile):
        self.department = department
        self.doctor = doctor
        self.name = name
        self.mobile = mobile

@app.route('/visitor', methods=['GET', 'POST'])
def visitor_portal():
    # methods=input(str)
    # print(methods)
    if request.method == 'POST':
        department_name = request.form['department']
        name = request.form['name']
        mobile = request.form['mobile']
        
        department = find_department(department_name)
        if department:
            doctor = department.doctors[tokens[department_name] % len(department.doctors)]
            token = assign_token(department_name)
            appointments.append(Appointment(department_name, doctor, name, mobile))
            return f"Appointment created. Your token: {token}"
        else:
            return "Department not found."

    return render_template('visitor.html', departments=departments)

@app.route('/hospital', methods=['GET', 'POST'])
def hospital_portal():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_department':
            department_name = request.form['department']
            departments.append(Department(department_name, []))
            return "Department added."
        elif action == 'add_doctor':
            department_name = request.form['department']
            doctor_name = request.form['doctor']
            department = find_department(department_name)
            if department:
                department.doctors.append(doctor_name)
                return "Doctor added."
            else:
                return "Department not found."

    search_query = request.args.get('search', '').lower()
    group_by_doctor = request.args.get('group_by_doctor', False)

    filtered_appointments = filter_appointments(search_query, group_by_doctor)
    return render_template('hospital.html', appointments=filtered_appointments, departments=departments)

def find_department(department_name):
    for department in departments:
        if department.name == department_name:
            return department
    return None

def assign_token(department_name):
    if department_name not in tokens:
        tokens[department_name] = 0
    tokens[department_name] += 1
    return tokens[department_name]

def filter_appointments(search_query, group_by_doctor):
    filtered = appointments
    if search_query:
        filtered = [appointment for appointment in filtered if
                    search_query in appointment.name.lower() or search_query in appointment.mobile]
    if group_by_doctor:
        grouped = {}
        for appointment in filtered:
            if appointment.doctor not in grouped:
                grouped[appointment.doctor] = []
            grouped[appointment.doctor].append(appointment)
        return grouped
    return filtered

if __name__ == '__main__':
    departments.append(Department("Department A", ["Doctor A1", "Doctor A2"]))
    departments.append(Department("Department B", ["Doctor B1"]))
    app.run()
