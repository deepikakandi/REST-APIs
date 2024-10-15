from flask import Blueprint, request, jsonify
from models.team_assignment_model import get_assignments,create_assignment,update_assignment,delete_assignment
import logging

assignment_blueprint = Blueprint('assignment', __name__)

@assignment_blueprint.route('/', methods=['GET'])
def get_assignments_route():
    try:
        logging.info("Fetching employee team assignments.")
        assignments = get_assignments()

        assignment_list = []
        for a in assignments:
            assignment_list.append({
                'assignment_id': a[0],
                'team_id': a[1],
                'team_name': a[2],
                'emp_id': a[3],
                'emp_name': a[4],
                'org_id': a[5],
                'org_name': a[6],
                'start_date': a[7],
                'end_date': a[8],
            })

        logging.info("Fetched assignments successfully.")
        return jsonify(assignment_list), 200

    except Exception as e:
        logging.error(f"Error fetching assignments: {e}")
        return jsonify({'error': str(e)}), 500


@assignment_blueprint.route('/', methods=['POST'])
def create_assignment_route():
    try:
        data = request.get_json()
        
        team_id = data.get('team_id')
        emp_id = data.get('emp_id')
        org_id = data.get('org_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not team_id or not emp_id or not org_id or not start_date:
            logging.warning("Missing required fields for creating assignment.")
            return jsonify({'error': 'team_id, emp_id, org_id, and start_date are required.'}), 400

        new_assignment_id = create_assignment(team_id, emp_id, org_id, start_date, end_date)
        logging.info(f"Created new assignment with ID {new_assignment_id}.")
        return jsonify({'assignment_id': new_assignment_id}), 201

    except Exception as e:
        logging.error(f"Error creating assignment: {e}")
        return jsonify({'error': str(e)}), 500


@assignment_blueprint.route('/<int:assignment_id>', methods=['PUT'])
def update_assignment_route(assignment_id):
    try:
        data = request.get_json()
        
        team_id = data.get('team_id')
        emp_id = data.get('emp_id')
        org_id = data.get('org_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        update_assignment(assignment_id, team_id, emp_id, org_id, start_date, end_date)
        logging.info(f"Updated assignment ID {assignment_id}.")
        return jsonify({'message': f'Assignment ID {assignment_id} updated successfully.'}), 200

    except Exception as e:
        logging.error(f"Error updating assignment ID {assignment_id}: {e}")
        return jsonify({'error': str(e)}), 500


@assignment_blueprint.route('/<int:assignment_id>', methods=['DELETE'])
def delete_assignment_route(assignment_id):
    try:
        delete_assignment(assignment_id)
        logging.info(f"Deleted assignment ID {assignment_id}.")
        return jsonify({'message': f'Assignment ID {assignment_id} deleted successfully.'}), 200

    except Exception as e:
        logging.error(f"Error deleting assignment ID {assignment_id}: {e}")
        return jsonify({'error': str(e)}), 500
