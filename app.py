from flask import Flask
from info_routes import info_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 注册蓝图
app.register_blueprint(info_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
