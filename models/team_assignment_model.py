import logging
from db import get_db_connection

def get_assignments():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = """
        SELECT 
            eta.assignment_id, 
            t.team_id, 
            t.team_name, 
            e.emp_id, 
            e.first_name || ' ' || e.last_name AS emp_name, 
            o.org_id, 
            o.org_name, 
            eta.start_date, 
            eta.end_date
        FROM 
            employee_team_assignment eta
        JOIN 
            team t ON eta.team_id = t.team_id
        JOIN 
            employee e ON eta.emp_id = e.emp_id
        JOIN 
            organization o ON eta.org_id = o.org_id;
        """
        
        cursor.execute(query)
        assignments = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return assignments

    except Exception as e:
        logging.error(f"Error fetching assignments: {e}")
        raise


def create_assignment(team_id, emp_id, org_id, start_date, end_date):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO employee_team_assignment (team_id, emp_id, org_id, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s) RETURNING assignment_id;
        """, (team_id, emp_id, org_id, start_date, end_date))
        
        new_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        connection.close()

        return new_id

    except Exception as e:
        logging.error(f"Error creating assignment: {e}")
        raise


def update_assignment(assignment_id, team_id=None, emp_id=None, org_id=None, start_date=None, end_date=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "UPDATE employee_team_assignment SET "
        params = []
        
        if team_id is not None:
            query += "team_id = %s, "
            params.append(team_id)
        if emp_id is not None:
            query += "emp_id = %s, "
            params.append(emp_id)
        if org_id is not None:
            query += "org_id = %s, "
            params.append(org_id)
        if start_date is not None:
            query += "start_date = %s, "
            params.append(start_date)
        if end_date is not None:
            query += "end_date = %s, "
            params.append(end_date)
        
        query = query.rstrip(', ')
        query += " WHERE assignment_id = %s;"
        params.append(assignment_id)

        cursor.execute(query, tuple(params))
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        logging.error(f"Error updating assignment ID {assignment_id}: {e}")
        raise


def delete_assignment(assignment_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM employee_team_assignment WHERE assignment_id = %s;", (assignment_id,))
        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:
        logging.error(f"Error deleting assignment ID {assignment_id}: {e}")
        raise
