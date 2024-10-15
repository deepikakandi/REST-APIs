def is_positive_integer(value):
    return isinstance(value, int) and value > 0

def validate_employee_input(data):
    errors = []
    if 'first_name' not in data or not isinstance(data['first_name'], str) or not data['first_name'].strip():
        errors.append("Invalid or missing 'first_name'. Must be a non-empty string.")
    
    if 'last_name' not in data or not isinstance(data['last_name'], str) or not data['last_name'].strip():
        errors.append("Invalid or missing 'last_name'. Must be a non-empty string.")
    

    # if 'role_name' not in data or not isinstance(data['role_name'], str) or not data['role_name'].strip():
    #     errors.append("Invalid or missing 'role_name'. Must be a non-empty string.")
    
    # if 'org_name' not in data or not isinstance(data['org_name'], str) or not data['org_name'].strip():
    #     errors.append("Invalid or missing 'org_name'. Must be a non-empty string.")
    
    if 'salary' not in data or not isinstance(data['salary'], (int, float)) or data['salary'] <= 0:
        errors.append("Invalid or missing 'salary'. Must be a positive number.")
    
    return errors

