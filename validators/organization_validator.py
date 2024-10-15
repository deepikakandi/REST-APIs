def validate_organization_input(data):
    errors = []
    if 'org_name' not in data or not isinstance(data['org_name'], str) or not data['org_name'].strip():
        errors.append("Invalid or missing 'org_name'. Must be a non-empty string.")
    
    return errors