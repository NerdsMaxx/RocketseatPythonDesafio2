from flask import Flask

from src.database import db
from src.routes import main_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/refeicao-crud'
db.init_app(app)
app.register_blueprint(main_bp)

# login_manager = LoginManager()
# login_manager.init_app(src)
# login_manager.login_view = 'login'

if __name__ == '__main__':
    app.run(debug=True)