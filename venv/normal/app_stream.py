import streamlit as st

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

departments = []
appointments = []
tokens = {}

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

def main():
    st.title("Hospital Token System")

    page = st.selectbox("Select Page", ["Visitor Portal", "Hospital Portal"])
    
    if page == "Visitor Portal":
        st.header("Visitor Portal")
        department = st.selectbox("Select Department:", [department.name for department in departments])
        name = st.text_input("Name:")
        mobile = st.text_input("Mobile:")
        if st.button("Create Appointment"):
            department_obj = find_department(department)
            if department_obj:
                doctor = department_obj.doctors[tokens[department] % len(department_obj.doctors)]
                token = assign_token(department)
                appointments.append(Appointment(department, doctor, name, mobile))
                st.success(f"Appointment created. Your token: {token}")
            else:
                st.error("Department not found.")

    elif page == "Hospital Portal":
        st.header("Hospital Portal")
        
        action = st.radio("Action:", ["Add Department", "Add Doctor"])
        
        if action == "Add Department":
            new_department = st.text_input("New Department Name:")
            if st.button("Add Department"):
                departments.append(Department(new_department, []))
                st.success("Department added.")
        
        elif action == "Add Doctor":
            department = st.selectbox("Select Department:", [department.name for department in departments])
            new_doctor = st.text_input("New Doctor Name:")
            if st.button("Add Doctor"):
                department_obj = find_department(department)
                if department_obj:
                    department_obj.doctors.append(new_doctor)
                    st.success("Doctor added.")
                else:
                    st.error("Department not found.")

if __name__ == "__main__":
    departments.append(Department("Department A", ["Doctor A1", "Doctor A2"]))
    departments.append(Department("Department B", ["Doctor B1"]))
    main()
