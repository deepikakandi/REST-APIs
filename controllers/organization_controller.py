import logging
from flask import Blueprint, request, jsonify
from db import get_db_connection
from models.organization_model import get_organization,create_organization,update_organization,delete_organization
from validators.organization_validator import validate_organization_input

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='organization_api.log', format='%(asctime)s %(levelname)s: %(message)s')

organization_blueprint = Blueprint('organization_blueprint', __name__)

# Fetch all organizations
@organization_blueprint.route('/', methods=['GET'])
def get_organization_route():
    try:

        organization = get_organization()
        organization_list = [{'org_id': org[0], 'org_name': org[1]} for org in organization]
        
        logging.info("Fetched all organizations successfully.")
        return jsonify(organization_list), 200

    except Exception as e:
        logging.error(f"Error fetching organizations: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Create a new organization
@organization_blueprint.route('/', methods=['POST'])
def create_organization_route():
    try:

        new_org = request.get_json()

        new_id = create_organization(new_org)
        logging.info(f"Created new organization with org_id {new_id}.")
        return jsonify({'message': 'Organization created', 'org_id': new_id}), 201

    except Exception as e:
        logging.error(f"Error creating organization: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Update an organization by org_id
@organization_blueprint.route('/<int:org_id>', methods=['PUT'])
def update_organization_route(org_id):
    try:
        updated_org = request.get_json()

        if not updated_org:
            logging.warning("Missing required org data.")
            return jsonify({'error': 'Missing required org data.'}), 400

        success, error = update_organization(org_id, updated_org)
        if not success:
            return jsonify({'error': error}), 500

        logging.info(f"Updated organization with org_id {org_id}.")
        return jsonify({'message': 'Organization updated'}), 200

    except Exception as e:
        logging.error(f"Error updating organization with org_id {org_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Delete an organization by org_id
@organization_blueprint.route('/<int:org_id>', methods=['DELETE'])
def delete_organization_route(org_id):
    try:

        success, error = delete_organization(org_id)
        if not success:
            return jsonify({'error': error}), 500
        logging.info(f"Deleted organization with org_id {org_id}.")
        return jsonify({'message': 'Organization deleted'}), 200


    except Exception as e:
        logging.error(f"Error deleting organization with org_id {org_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500












































# # Fetch a single organization by org_id
# @organization_blueprint.route('/organization/<int:org_id>', methods=['GET'])
# def get_organization(org_id):
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM organization WHERE org_id = %s", (org_id,))
#         organization = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if organization:
#             logging.info(f"Fetched organization with org_id {org_id} successfully.")
#             return jsonify({
#                 'org_id': organization[0],
#                 'org_name': organization[1],
#                 'org_head_id': organization[2]
#             }), 200
#         else:
#             logging.warning(f"Organization with org_id {org_id} not found.")
#             return jsonify({'message': 'Organization not found'}), 404

#     except Exception as e:
#         logging.error(f"Error fetching organization with org_id {org_id}: {str(e)}")
#         return jsonify({'error': str(e)}), 500