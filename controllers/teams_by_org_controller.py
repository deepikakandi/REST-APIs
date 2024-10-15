from flask import Blueprint, jsonify, request
from db import get_db_connection  
import logging
from models.teams_by_org_model import get_teams_by_org

teams_by_org_blueprint = Blueprint('teams_by_org_blueprint',__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='organization_team.log', format='%(asctime)s %(levelname)s: %(message)s')

# Get all teams under an organization by org_id
@teams_by_org_blueprint.route('/<int:org_id>/teams', methods=['GET'])
def get_teams_by_org_route(org_id):
    try:

        teams = get_teams_by_org(org_id)
        team_list = []
        for team in teams:
            team_list.append({
                'team_id': team[0],
                'team_name': team[1],
                'org_name': team[2]
            })

        logging.info(f"Teams data fetched successfully for org_id {org_id}.")
        return jsonify(team_list), 200

    except Exception as e:
        logging.error(f"Error fetching teams for org_id {org_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

  

