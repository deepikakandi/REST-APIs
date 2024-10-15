def validate_role_input(data):
    errors = []
    if 'role_name' not in data or not isinstance(data['role_name'], str) or not data['role_name'].strip():
        errors.append("Invalid or missing 'role_name'. Must be a non-empty string.")
    
    return errors