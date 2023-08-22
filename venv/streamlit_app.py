import streamlit as st
import requests

def register_department():
    department_name = st.text_input('Enter Department Name:')
    departments = requests.get('http://localhost:5000/get_departments').json()
    if department_name in departments:
        st.warning('This department is already registered. But U can change the doctors list')
    
    department_doctors=[]
    if department_name:
        department_doctors = requests.get(f'http://localhost:5000/get_doctors/{department_name}').json()
    
    doctors = st.text_area('Enter Doctors (comma-separated):',value=', '.join(map(str, department_doctors)))
    doctors = [doctor.strip() for doctor in doctors.split(',')]
    
    if st.button('Register Department'):
        data = {
            'department_name': department_name,
            'doctors': doctors
        }
        response = requests.post('http://localhost:5000/register_department', json=data)
        st.write(response.json())

def hospital_portal():
    st.header('ALL Appointments')
    departments = requests.get('http://localhost:5000/get_departments').json()
    department_name = st.selectbox('Select Department:', departments+['All'])
    
    appointments = requests.get(f'http://localhost:5000/appointments/{department_name}').json()
    
    st.subheader('Appointments')
    
    search_term = st.text_input('Search by Name or Mobile Number:')
    if search_term:
        filtered_appointments = filter_appointments(appointments, search_term)
    else: 
        filtered_appointments = list(appointments.values())
    
    for appointment in filtered_appointments:
        st.write(f"Token: {appointment['token']}")
        st.write(f"Visitor Name: {appointment['visitor_name']}")
        st.write(f"Visitor Mobile: {appointment['visitor_mobile']}")
        st.write(f"Doctor: {appointment['doctor']}")
        st.write("-" * 30)

def filter_appointments(appointments, search_term):
    filtered_appointments = []
    for token, appointment in appointments.items():
        if search_term.lower() in appointment['visitor_name'].lower() or \
           search_term in appointment['visitor_mobile']:
            filtered_appointments.append(appointment)
    return filtered_appointments

def book_appointment():
    departments = requests.get('http://localhost:5000/get_departments').json()
    department_name = st.selectbox('Select Department:', departments)
    visitor_name = st.text_input('Enter Your Name:')
    visitor_mobile = st.text_input('Enter Your Mobile Number:')
    
    if st.button('Book Appointment'):
        data = {
            'department_name': department_name,
            'visitor_name': visitor_name,
            'visitor_mobile': visitor_mobile
        }
        response = requests.post('http://localhost:5000/book_appointment', json=data)
        result = response.json()
        st.write(result['message'])
        if result['message'] not in ['Department not found','Missing required data','Same name and mobile number have already fixed a appointment .. Plz check the appointments in hospital portal !!!']:
            st.write('Your Token:', result['token'])

if __name__ == '__main__':
    st.title('Hospital Portal')
    
    portal = st.radio('Select Portal:', ['Visitor', 'Hospital'])
    
    if portal == 'Visitor':
        st.header('Visitor Portal')
        book_appointment()
    elif portal == 'Hospital':
        st.header('Hospital Portal')
        register_department()
        hospital_portal()
