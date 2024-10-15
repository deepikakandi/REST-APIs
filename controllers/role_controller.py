from flask import Blueprint, request, jsonify
from db import get_db_connection  
from validators.role_validator import validate_role_input
from models.role_model import get_roles, create_role, update_role, delete_role
import logging

# Create a Blueprint for role APIs
role_blueprint = Blueprint('role_blueprint', __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Route to get all roles
@role_blueprint.route('/', methods=['GET'])
def get_roles_route():

    logger.info("Received GET request to fetch all roles.")

    try:

        role = get_roles()
        role_list = []
        for roles in role:
            logger.info(f'Processing employee: {roles}')
            role_list.append({
                'role_id': roles[0],
                'role_name': roles[1]
            })
        logger.info('role data processing completed.')
        return jsonify(role_list)

    except Exception as e:
        logger.error(f"Error fetching roles: {e}")
        return jsonify({'error': str(e)}), 500


# Route to create a new role
@role_blueprint.route('/', methods=['POST'])
def create_role_route():
    try:

        new_role = request.get_json()  # Get the new role data from the request body

        new_role_id = create_role(new_role)
        logger.info(f"New role created with ID: {new_role_id}")
        return jsonify({'message': 'Role created', 'role_id': new_role_id}), 201
    except Exception as e:
        logger.error(f"Error creating role: {e}")
        return jsonify({'error': str(e)}), 500


# Route to update a role by ID
@role_blueprint.route('/<int:role_id>', methods=['PUT'])
def update_role_route(role_id):
    try:

        updated_role = request.get_json()  # Get updated role data from the request body

        if not updated_role:
            logging.warning("Missing required role data.")
            return jsonify({'error': 'Missing required role data.'}), 400

        success, error = update_role(role_id,updated_role)
        if not success:
            return jsonify({'error': error}), 500

        logger.info(f"Role with ID {role_id} updated")
        return jsonify({'message': 'Role updated'})
    except Exception as e:
        logger.error(f"Error updating role: {e}")
        return jsonify({'error': str(e)}), 500

# Route to delete a role by ID
@role_blueprint.route('/<int:role_id>', methods=['DELETE'])
def delete_role_route(role_id):
    try:

        success, error = delete_role(role_id)
        if not success:
            return jsonify({'error': error}), 500
      
        logger.info(f"Role with ID {role_id} deleted")
        return jsonify({'message': 'Role deleted'})
    except Exception as e:
        logger.error(f"Error deleting role: {e}")
        return jsonify({'error': str(e)}), 500















































































# Route to get a specific role by ID
# @role_blueprint.route('/<int:role_id>', methods=['GET'])
# def get_role(role_id):
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()

#         cursor.execute("SELECT * FROM role WHERE role_id = %s", (role_id,))
#         role = cursor.fetchone()

#         cursor.close()
#         connection.close()

#         if role:
#             role_data = {'role_id': role[0], 'role_name': role[1]}
#             logger.debug(f"Role fetched: {role_data}")
#             return jsonify(role_data)
#         else:
#             logger.warning(f"Role with ID {role_id} not found")
#             return jsonify({'message': 'Role not found'}), 404
#     except Exception as e:
#         logger.error(f"Error fetching role: {e}")
#         return jsonify({'error': str(e)}), 500