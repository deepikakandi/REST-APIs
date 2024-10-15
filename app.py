from flask import Flask
from flasgger import Swagger
from controllers.employee_controller import employee_blueprint
from controllers.role_controller import role_blueprint
from controllers.team_controller import team_blueprint
from controllers.organization_controller import organization_blueprint
from controllers.employee_team_assignment_controller import assignment_blueprint
from controllers.teams_by_org_controller import teams_by_org_blueprint
from controllers.teams_emp_by_org_controller import teams_emp_by_org_blueprint
app = Flask(__name__)
swagger = Swagger(app)

# Register blueprints
app.register_blueprint(employee_blueprint, url_prefix='/employee')
app.register_blueprint(role_blueprint, url_prefix='/role')
app.register_blueprint(team_blueprint, url_prefix='/team')
app.register_blueprint(organization_blueprint, url_prefix='/organization')
app.register_blueprint(assignment_blueprint, url_prefix='/assignment')
app.register_blueprint(teams_by_org_blueprint, url_prefix='/organizations')
app.register_blueprint(teams_emp_by_org_blueprint, url_prefix='/organizations')
if __name__ == '__main__':
    app.run(debug=True)







