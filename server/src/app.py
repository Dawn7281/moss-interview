from flask import Flask
from flask_cors import CORS
from src.utils.extensions import db
from src.routes.user_routes import user_bp
from src.routes.file_routes import file_bp
from src.routes.experience_routes import experience_bp
from src.routes.interview_routes import interview_bp
from src.routes.search_routes import search_bp
from src.routes.job_routes import job_bp
import os

def create_app():
    app = Flask(__name__)

    CORS_ORIGIN = os.getenv('CORS_ORIGIN')
    CORS(app, supports_credentials=True, origins=[CORS_ORIGIN], expose_headers=['Content-Disposition'])

    HOSTNAME = os.getenv('DB_HOSTNAME')
    PORT = os.getenv('DB_PORT')
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE = os.getenv('DATABASE')

    # MySQL 配置
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(user_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(experience_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(job_bp)

    return app

app = create_app()

# 提前加载模型
with app.app_context():
    # 如果数据库不存在，可以创建
    db.create_all()
    print("数据库已初始化")

if __name__ == '__main__':
    host = os.getenv('RUN_HOST')
    port = os.getenv('RUN_PORT')

    app.run(host=host, port=port, debug=True)
