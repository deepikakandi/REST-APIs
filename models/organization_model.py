from db import get_db_connection
import logging
from validators.organization_validator import validate_organization_input
from flask import jsonify

def get_organization():

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM organization")
        organization = cursor.fetchall()
        cursor.close()
        connection.close()
        return organization

    except Exception as e:
        logging.error(f"Error fetching organization: {e}")
        raise


def create_organization(new_org):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        validation_errors = validate_organization_input(new_org)
        if validation_errors:
            logging.warning(f"Validation errors: {validation_errors}")
            return jsonify({'errors': validation_errors}), 400

        sql = "INSERT INTO organization (org_name) VALUES (%s) RETURNING org_id"
        cursor.execute(sql, (new_org['org_name'],))
        connection.commit()

        new_id = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return new_id
    
    except Exception as e:
        logging.error(f"Error creating organization: {e}")
        raise


def update_organization(org_id, updated_org):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        validation_errors = validate_organization_input(updated_org)
        if validation_errors:
            logging.warning(f"Validation errors: {validation_errors}")
            return jsonify({'errors': validation_errors}), 400 

        sql = "UPDATE organization SET org_name = %s WHERE org_id = %s"
        cursor.execute(sql, (updated_org['org_name'], org_id))
        connection.commit()

        if cursor.rowcount > 0:
            logging.info(f"Org ID {org_id} successfully updated.")
            response = jsonify({'message': f'Org ID {org_id} successfully updated'}), 200
        else:
            logging.warning(f"Org ID {org_id} not found for update.")
            response = jsonify({'message': f'Org ID {org_id} not found'}), 404

        cursor.close()
        connection.close()
        return response

    except Exception as e:
        logging.error(f"Error updating organization ID {org_id}: {e}")
        raise


def delete_organization(org_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM organization WHERE org_id = %s", (org_id,))
        connection.commit()

        if cursor.rowcount > 0:
            logging.info(f"Org ID {org_id} successfully deleted.")
            response = jsonify({'message': f'Org ID {org_id} successfully deleted'}), 200
        else:
            logging.warning(f"Org ID {org_id} not found for deleted.")
            response = jsonify({'message': f'Org ID {org_id} not found'}), 404

        cursor.close()
        connection.close()
        return response

    except Exception as e:
        logging.error(f"Error deleting employee: {e}")
        return jsonify({'error': str(e)}), 500
