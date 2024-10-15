def is_positive_integer(value):
    return isinstance(value, int) and value > 0

def validate_team_input(data):
    errors = []
    if 'team_name' not in data or not isinstance(data['team_name'], str) or not data['team_name'].strip():
        errors.append("Invalid or missing 'team_name'. Must be a non-empty string.")
    
    if 'org_id' not in data or not is_positive_integer(data['org_id']):
        errors.append("Invalid or missing 'org_id'. Must reference a valid organization.")

    if 'manager_id' not in data or not is_positive_integer(data['manager_id']):
        errors.append("Invalid or missing 'manager_id'. Must reference a valid employee as team head.")
    
    return errors