from db import get_db_connection
import logging
from validators.employee_validator import validate_employee_input, is_positive_integer
from flask import jsonify


def get_employee():

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Modified SQL query to join employee, role, and organization tables
        sql = """
            SELECT 
                e.emp_id, 
                e.first_name, 
                e.last_name, 
                e.role_id, 
                r.role_name, 
                e.org_id, 
                o.org_name, 
                e.salary, 
                e.isactive 
            FROM 
                employee e
            LEFT JOIN 
                role r ON e.role_id = r.role_id
            LEFT JOIN 
                organization o ON e.org_id = o.org_id
        """

        logging.info('Executing SQL: %s', sql)
        cursor.execute(sql)
        employee = cursor.fetchall()
        logging.info(f'Number of employees fetched: {len(employee)}')
        
        cursor.close()
        connection.close()
        return employee

    except Exception as e:
        logging.error(f"Error fetching employees: {e}")
        raise

def create_employee(new_employee):

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        validation_errors = validate_employee_input(new_employee)
        if validation_errors:
            logging.warning(f"Validation errors: {validation_errors}")
            return jsonify({'errors': validation_errors}), 400  

        logging.info(f"Employee data received: {new_employee}")

        if not all(key in new_employee for key in ['first_name', 'last_name', 'role_name','org_name', 'salary']):
            logging.warning('Missing required employee data.')
            return jsonify({'error': 'Missing required employee data'}), 400

        if 'role_name' not in new_employee:
            logging.error("Role name is missing in the request.")
            return jsonify({'error': 'Role name is required.'}), 400
        
        role_name = new_employee['role_name']
        cursor.execute('SELECT role_id FROM role WHERE role_name = %s', (role_name,))
        role_result = cursor.fetchone()
        print(role_result)

        if not role_result:
            logging.error(f"Invalid role name: {role_name}")
            return jsonify({'error': f"Invalid role name: {role_name}"}), 400
        
        role_id = role_result[0]
        print(role_id)

        if 'org_name' not in new_employee:
            logging.error("organization name is missing in the request.")
            return jsonify({'error': 'organization name is required.'}), 400
        
        org_name = new_employee['org_name']
        cursor.execute('SELECT org_id FROM organization WHERE org_name = %s', (org_name,))
        org_result = cursor.fetchone()
        print(org_result)

        if not org_result:
            logging.error(f"Invalid organization name: {org_name}")
            return jsonify({'error': f"Invalid organization name: {org_name}"}), 400
        
        org_id = org_result[0]
        print(org_id)

        
        sql = "INSERT INTO employee (first_name,last_name, role_id, org_id,salary) VALUES ('{}','{}',{},{},{}) RETURNING emp_id".format(new_employee["first_name"],new_employee["last_name"],role_id,org_id,new_employee["salary"])
        print(sql)
        logging.info(f"Executing SQL: {sql}")
        cursor.execute(sql, (
            new_employee["first_name"], 
            new_employee["last_name"], 
            role_id, 
            org_id, 
            new_employee["salary"]   

        ))

        connection.commit()
        new_id = cursor.fetchone()[0]
        print(new_id)
        logging.info(f"New employee created with ID: {new_id}")
        
        cursor.close()
        connection.close()
        return new_id
    
    except Exception as e:
        logging.error(f"Error creating employee: {e}")
        raise


def update_employee(emp_id, updated_employee):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Validate employee input
        validation_errors = validate_employee_input(updated_employee)
        if validation_errors:
            logging.warning(f"Validation errors: {validation_errors}")
            return jsonify({'errors': validation_errors}), 400 

        logging.info(f"Updating employee with data: {updated_employee}")

        # Check if organization name is provided instead of org_id
        if 'org_name' in updated_employee and updated_employee['org_name']:
            logging.info(f"Looking up org_id for org_name: {updated_employee['org_name']}")
            cursor.execute("SELECT org_id FROM organization WHERE org_name = %s", (updated_employee['org_name'],))
            result = cursor.fetchone()
            if result:
                updated_employee['org_id'] = result[0]
                logging.info(f"Found org_id {result[0]} for org_name {updated_employee['org_name']}")
            else:
                logging.error(f"Organization name {updated_employee['org_name']} not found.")
                return jsonify({'error': f"Organization name {updated_employee['org_name']} not found"}), 400

        # Check if role name is provided instead of role_id
        if 'role_name' in updated_employee and updated_employee['role_name']:
            logging.info(f"Looking up role_id for role_name: {updated_employee['role_name']}")
            cursor.execute("SELECT role_id FROM role WHERE role_name = %s", (updated_employee['role_name'],))
            result = cursor.fetchone()
            if result:
                updated_employee['role_id'] = result[0]
                logging.info(f"Found role_id {result[0]} for role_name {updated_employee['role_name']}")
            else:
                logging.error(f"Role name {updated_employee['role_name']} not found.")
                return jsonify({'error': f"Role name {updated_employee['role_name']} not found"}), 400

        # Check if both org_id and role_id are available (after name lookups if applicable)
        if 'org_id' not in updated_employee or 'role_id' not in updated_employee:
            return jsonify({'error': "Missing 'org_id' or 'role_id' for update."}), 400

        # Construct the SQL query to update employee
        sql = """UPDATE employee 
                 SET first_name = %s, last_name = %s, role_id = %s, org_id = %s, salary = %s 
                 WHERE emp_id = %s"""
        
        logging.info(f"Executing SQL: {sql}")
        cursor.execute(sql, (updated_employee["first_name"], 
                             updated_employee["last_name"], 
                             updated_employee["role_id"], 
                             updated_employee["org_id"], 
                             updated_employee["salary"], 
                             emp_id))
        connection.commit()

        # Check if update was successful
        if cursor.rowcount > 0:
            logging.info(f"Employee ID {emp_id} successfully updated.")
            response = jsonify({'message': f'Employee ID {emp_id} successfully updated'}), 200
        else:
            logging.warning(f"Employee ID {emp_id} not found for update.")
            response = jsonify({'message': f'Employee ID {emp_id} not found'}), 404

        cursor.close()
        connection.close()
        return response

    except Exception as e:
        logging.error(f"Error updating employee ID {emp_id}: {e}")
        return jsonify({'error': str(e)}), 500



def delete_employee(emp_id):

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        logging.info(f"Executing DELETE SQL for employee ID: {emp_id}")
        cursor.execute('DELETE FROM employee WHERE emp_id = %s', (emp_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            logging.info(f"Employee ID {emp_id} successfully deleted.")
            return jsonify({'message': 'Employee deleted successfully'}), 200
        else:
            logging.warning(f"Employee ID {emp_id} not found in the database.")
            return jsonify({'message': 'Employee not found'}), 404


        cursor.close()
        connection.close()
        return response


    except Exception as e:
        logging.error(f"Error deleting employee: {e}")
        return jsonify({'error': str(e)}), 500
     