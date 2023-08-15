from flask import Flask
from info_routes import info_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(info_bp)


if __name__ == '__main__':
    app.run()
