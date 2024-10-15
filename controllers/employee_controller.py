from flask import Blueprint, jsonify, request
from db import get_db_connection
from models.employee_model import get_employee, create_employee, delete_employee, update_employee
from validators.employee_validator import validate_employee_input, is_positive_integer
import logging

employee_blueprint = Blueprint('employee_blueprint', __name__)

@employee_blueprint.route('/', methods=['GET'])
def get_employee_route():
    
    logging.info("Received GET request to fetch all employees.")

    try:

        employee = get_employee()

        employee_list = []
        for emp in employee:
            logging.info(f'Processing employee: {emp}')
            employee_list.append({
                'emp_id': emp[0],
                'first_name': emp[1],
                'last_name': emp[2],
                'role_id': emp[3],
                'role_name': emp[4],
                'org_id': emp[5],
                'org_name': emp[6],
                'salary': emp[7],
                'isactive': emp[8]
                
            })

        logging.info('Employee data processing completed.')
        return jsonify(employee_list)

    except Exception as e:
        logging.error(f"Error fetching employee data: {e}")
        return jsonify({'error': str(e)}), 500


# Route to create a new employee
@employee_blueprint.route('/', methods=['POST'])
def create_employee_route():
    
    logging.info("Received POST request to create a new employee.")

    try:

        new_employee = request.get_json()
        new_employee_id = create_employee(new_employee)
        return jsonify({'message': 'Employee created', 'emp_id': new_employee_id}), 201
    except Exception as e:
        logging.error(f"Error creating employee: {e}")
        return jsonify({'error': str(e)}), 500

# # Route to delete an employee
@employee_blueprint.route('/<int:emp_id>', methods=['DELETE'])
def delete_employee_route(emp_id):

    logging.info(f"Received DELETE request for employee ID: {emp_id}")

    try:

        success, error = delete_employee(emp_id)
        if not success:
            return jsonify({'error': error}), 500
        logging.info(f"Employee {emp_id} deleted successfully.")
        return jsonify({'message': f'Employee {emp_id} deleted'}), 200 if cursor.rowcount > 0 else 404
    
    except Exception as e:
        logging.error(f"Error deleting employee ID {emp_id}: {e}")
        return jsonify({'error': str(e)}), 500

# # Route to update an employee
@employee_blueprint.route('/<int:emp_id>', methods=['PUT'])
def update_employee_route(emp_id):

    try:
        updated_employee = request.get_json()

        if not updated_employee:
            logging.warning("Missing required employee data.")
            return jsonify({'error': 'Missing required employee data.'}), 400

        success, error = update_employee(emp_id, updated_employee)
        if not success:
            return jsonify({'error': error}), 500

        logging.info(f"Employee {emp_id} updated successfully.")
        return jsonify({'message': f'Employee {emp_id} updated successfully.'}), 200
    except Exception as e:
        logging.error(f"Error updating employee: {str(e)}")
        return jsonify({'error': str(e)}), 500
