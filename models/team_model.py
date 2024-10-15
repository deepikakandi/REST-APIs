from db import get_db_connection
import logging
from validators.team_validator import validate_team_input
from flask import jsonify


def get_teams():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Join with employee and organization tables to get the names
        cursor.execute("""
            SELECT t.team_id, t.team_name, t.org_id, t.manager_id, 
                   e.first_name AS manager_first_name, e.last_name AS manager_last_name, 
                   o.org_name 
            FROM team t
            JOIN employee e ON t.manager_id = e.emp_id 
            JOIN organization o ON t.org_id = o.org_id
        """)
        teams = cursor.fetchall()
        cursor.close()
        connection.close()
        return teams

    except Exception as e:
        logging.error(f"Error fetching employees: {e}")
        raise

def create_team(new_team):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        validation_errors = validate_team_input(new_team)
        if validation_errors:
            logging.warning(f"Validation errors: {validation_errors}")
            return jsonify({'errors': validation_errors}), 400

        sql = """INSERT INTO team (team_name, org_id, manager_id) 
                 VALUES (%s, %s, %s) RETURNING team_id"""
        cursor.execute(sql, (new_team['team_name'], new_team['org_id'], new_team['manager_id']))
        connection.commit()

        new_id = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return new_id

    except Exception as e:
        logging.error(f"Error creating employee: {e}")
        raise


def update_team(team_id,updated_team):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        validation_errors = validate_team_input(updated_team)
        if validation_errors:
            logging.warning(f"Validation errors: {validation_errors}")
            return jsonify({'errors': validation_errors}), 400 

        sql = """UPDATE team SET team_name = %s, org_id = %s, manager_id = %s
                 WHERE team_id = %s"""
        cursor.execute(sql, (updated_team['team_name'], updated_team['org_id'], updated_team['manager_id'], team_id))
        connection.commit()

        if cursor.rowcount > 0:
            logging.info(f"Team ID {team_id} successfully updated.")
            response = jsonify({'message': f'Team ID {team_id} successfully updated'}), 200
        else:
            logging.warning(f"Team ID {team_id} not found for update.")
            response = jsonify({'message': f'Team ID {team_id} not found'}), 404

        cursor.close()
        connection.close()  
        return response

    except Exception as e:
        logging.error(f"Error updating team ID {team_id}: {e}")
        return jsonify({'error': str(e)}), 500



def delete_team(team_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM team WHERE team_id = %s", (team_id,))
        connection.commit()

        if cursor.rowcount > 0:
            logging.info(f"Team ID {team_id} successfully deleted.")
            response = jsonify({'message': f'Team ID {team_id} successfully deleted'}), 200
        else:
            logging.warning(f"Team ID {team_id} not found for delete.")
            response = jsonify({'message': f'Team ID {team_id} not found'}), 404

        cursor.close()
        connection.close()
        return response
    
    except Exception as e:
        logging.error(f"Error deleting team: {e}")
        return jsonify({'error': str(e)}), 500