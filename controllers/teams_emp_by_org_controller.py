from flask import Blueprint, jsonify, request
from models.teams_emp_by_org_model import get_teams_and_employees_by_org 
import logging

teams_emp_by_org_blueprint = Blueprint('teams_emp_by_org_blueprint', __name__)

logging.basicConfig(level=logging.DEBUG, filename='organization_teams_employees.log', format='%(asctime)s %(levelname)s: %(message)s')

@teams_emp_by_org_blueprint.route('/<int:org_id>/teams-employees', methods=['GET'])
def get_teams_and_employees_by_org_route(org_id):
    try:
        
        teams_data, employees_data = get_teams_and_employees_by_org(org_id)

        if not teams_data:
            return jsonify({'message': f'No teams found for organization ID {org_id}'}), 404

        
        final_response = []
        for i, team in enumerate(teams_data):
            employee_list = []
            for emp in employees_data[i]:
                employee_list.append({
                    'emp_id': emp[0],
                    'first_name': emp[1],
                    'last_name': emp[2],
                    'start_date': emp[3],
                    'end_date': emp[4]
                })

            team['employees'] = employee_list
            final_response.append(team)

        logging.info(f"Team and employee data fetched successfully for org_id {org_id}.")
        return jsonify(final_response), 200

    except Exception as e:
        logging.error(f"Error fetching teams and employees for org_id {org_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500
