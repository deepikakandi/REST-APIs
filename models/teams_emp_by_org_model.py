from db import get_db_connection
import logging

def get_teams_and_employees_by_org(org_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        
        team_sql = """
            SELECT team.team_id, team.team_name, org.org_name, emp.first_name, emp.last_name 
            FROM team
            INNER JOIN organization org ON team.org_id = org.org_id
            INNER JOIN employee emp ON team.manager_id = emp.emp_id
            WHERE team.org_id = %s
        """
        logging.info(f"Executing SQL to fetch teams and managers: {team_sql} with org_id={org_id}")
        cursor.execute(team_sql, (org_id,))
        teams = cursor.fetchall()

        if not teams:
            logging.warning(f"No teams found for organization ID {org_id}")
            return [], []

        teams_data = []
        employees_data = []

        for team in teams:
            team_id, team_name, org_name, manager_first_name, manager_last_name = team

          
            emp_sql = """
                SELECT emp.emp_id, emp.first_name, emp.last_name, assignment.start_date, assignment.end_date
                FROM employee_team_assignment assignment
                INNER JOIN employee emp ON assignment.emp_id = emp.emp_id
                WHERE assignment.team_id = %s
            """
            logging.info(f"Executing SQL to fetch employees for team_id={team_id}")
            cursor.execute(emp_sql, (team_id,))
            employees = cursor.fetchall()

           
            teams_data.append({
                'team_id': team_id,
                'team_name': team_name,
                'organization_name': org_name,
                'manager_name': f'{manager_first_name} {manager_last_name}'
            })

            employees_data.append(employees)

        cursor.close()
        connection.close()

        return teams_data, employees_data

    except Exception as e:
        logging.error(f"Error fetching teams and employees: {e}")
        raise



