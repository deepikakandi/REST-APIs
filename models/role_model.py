from db import get_db_connection
import logging
from validators.role_validator import validate_role_input
from flask import jsonify

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_roles():

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        logger.info('Executing SQL: SELECT * FROM role')
        cursor.execute("SELECT * FROM role")
        role = cursor.fetchall()
        logger.info(f'Number of roles fetched: {len(role)}')

        cursor.close()
        connection.close()
        return role

    except Exception as e:
        logging.error(f"Error fetching role: {e}")
        raise

    
def create_role(new_role):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        
        validation_errors = validate_role_input(new_role)
        if validation_errors:
            logging.warning(f"Validation errors: {validation_errors}")
            return jsonify({'errors': validation_errors}), 400  
        
        logger.debug(f"Role data received: {new_role}")

        sql = "INSERT INTO role (role_name) VALUES (%s) RETURNING role_id"
        cursor.execute(sql, (new_role['role_name'],))
        connection.commit()
        
        new_role_id = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return new_role_id

    except Exception as e:
        logging.error(f"Error creating role: {e}")
        raise   


def update_role(role_id,updated_role):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        validation_errors = validate_role_input(updated_role)
        if validation_errors:
            logging.warning(f"Validation errors: {validation_errors}")
            return jsonify({'errors': validation_errors}), 400 
        
        logger.debug(f"Updating role {role_id} with data: {updated_role}")

        sql = "UPDATE role SET role_name = %s WHERE role_id = %s"
        cursor.execute(sql, (updated_role['role_name'], role_id))
        connection.commit()

        if cursor.rowcount > 0:
            logging.info(f"Role ID {role_id} successfully updated.")
            response = jsonify({'message': f'Role ID {role_id} successfully updated'}), 200
        else:
            logging.warning(f"Role ID {role_id} not found for update.")
            response = jsonify({'message': f'Role ID {role_id} not found'}), 404

        cursor.close()
        connection.close()
        return response

    except Exception as e:
        logging.error(f"Error updating role ID {role_id}: {e}")
        raise


def delete_role(role_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM role WHERE role_id = %s", (role_id,))
        connection.commit()

        if cursor.rowcount > 0:
            logging.info(f"Role ID {role_id} successfully deleted.")
            response = jsonify({'message': f'Role ID {role_id} successfully deleted'}), 200
        else:
            logging.warning(f"Role ID {role_id} not found for delete.")
            response = jsonify({'message': f'Role ID {role_id} not found'}), 404

        cursor.close()
        connection.close()
        return response

    except Exception as e:
        logging.error(f"Error deleting role: {e}")
        return jsonify({'error': str(e)}), 500
    