from db import get_db_connection
import logging
from flask import jsonify

def get_teams_by_org(org_id):
    try:
        
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """SELECT team.team_id, team.team_name, org.org_name 
                 FROM team
                 INNER JOIN organization org ON team.org_id = org.org_id
                 WHERE team.org_id = %s"""

        logging.info(f"Executing SQL: {sql} with org_id={org_id}")
        cursor.execute(sql, (org_id,))
        teams = cursor.fetchall()
        if not teams:
            logging.warning(f"No teams found for organization ID {org_id}")
            return jsonify({'message': f'No teams found for organization ID {org_id}'}), 404

        cursor.close()
        connection.close()
        return teams

    except Exception as e:
        logging.error(f"Error fetching employees: {e}")
        raise

