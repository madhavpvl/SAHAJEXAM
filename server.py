from flask import Flask, request, jsonify

app = Flask(__name__)

employees = {}

employee_id_counter = 1

# Create Employee
@app.route('/employee', methods=['POST'])
def create_employee():
    global employee_id_counter

    data = request.get_json()

    name = data.get("name")
    city = data.get("city")

    if not name or not city:
        return jsonify({"error": "Name and city are required"}), 400

    employee_id = str(employee_id_counter)
    employee_id_counter += 1

    employee = {
        "employeeId": employee_id,
        "name": name,
        "city": city
    }

    employees[employee_id] = employee

    return jsonify({"employeeId": employee_id}), 201

# Get Employee by ID
@app.route('/employee/<string:id>', methods=['GET'])
def get_employee_by_id(id):
    employee = employees.get(id)

    if employee:
        return jsonify(employee), 200
    else:
        return jsonify({"message": f"Employee with ID {id} was not found"}), 404

# Search Employees by Name and/or City
@app.route('/employees/search', methods=['POST'])
def search_employees():
    data = request.get_json()
    fields = data.get("fields")
    condition = data.get("condition", "AND")

    if not fields:
        return jsonify({"error": "No search criteria provided"}), 400

    results = []

    for employee in employees.values():
        match = False

        for criterion in fields:
            field_name = criterion.get("fieldName")
            eq = criterion.get("eq")
            neq = criterion.get("neq")

            if field_name:
                if eq and employee.get(field_name) == eq:
                    match = True
                if neq and employee.get(field_name) != neq:
                    match = True

                if condition == "AND" and not match:
                    break
                elif condition == "OR" and match:
                    break

        if match:
            results.append(employee)

    return jsonify(results), 200

# Get All Employees
@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    return jsonify(list(employees.values())), 200

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
