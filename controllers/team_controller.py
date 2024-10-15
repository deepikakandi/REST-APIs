import logging
from flask import Blueprint, request, jsonify
from validators.team_validator import validate_team_input
from models.team_model import get_teams, create_team, update_team, delete_team
from db import get_db_connection

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='team_api.log', format='%(asctime)s %(levelname)s: %(message)s')

team_blueprint = Blueprint('team_blueprint', __name__)

# Get all teams with manager name and organization name
@team_blueprint.route('/', methods=['GET'])
def get_teams_route():
    try:

        teams = get_teams()
        team_list = []
        for team in teams:
            logging.info(f'Processing team: {team}')
            team_list.append({
                'team_id': team[0],
                'team_name': team[1],
                'org_id': team[2],
                'manager_id': team[3],
                'manager_first_name': team[4],
                'manager_last_name': team[5],
                'organization_name': team[6]
            })
        logging.info('Team data processing completed.')
        return jsonify(team_list), 200

    except Exception as e:
        logging.error(f"Error fetching teams: {str(e)}")
        return jsonify({'error': str(e)}), 500

# # Create a new team
@team_blueprint.route('/', methods=['POST'])
def create_team_route():
    try:

        new_team = request.get_json()

        new_id = create_team(new_team)
        logging.info(f"Created new team with team_id {new_id}.")
        return jsonify({'message': 'Team created', 'team_id': new_id}), 201

    except Exception as e:
        logging.error(f"Error creating team: {str(e)}")
        return jsonify({'error': str(e)}), 500

# # Update a team by team_id
@team_blueprint.route('/<int:team_id>', methods=['PUT'])
def update_team_route(team_id):
    try:

        updated_team = request.get_json()

        if not updated_team:
            logging.warning("Missing required team data.")
            return jsonify({'error': 'Missing required team data.'}), 400

        success, error = update_team(team_id, updated_team)
        if not success:
            return jsonify({'error': error}), 500


        logging.info(f"Updated team with team_id {team_id}.")
        return jsonify({'message': 'Team updated'}), 200

    except Exception as e:
        logging.error(f"Error updating team with team_id {team_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

# # Delete a team by team_id
@team_blueprint.route('/<int:team_id>', methods=['DELETE'])
def delete_team_route(team_id):
    try:
        
        success, error = delete_team(team_id)
        if not success:
            return jsonify({'error': error}), 500
        logging.info(f"Deleted team with team_id {team_id}.")
        return jsonify({'message': 'Team deleted'}), 200

    except Exception as e:
        logging.error(f"Error deleting team with team_id {team_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

