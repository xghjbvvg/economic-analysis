from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

from main.config.config import config, template_config, swagger_config, DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

db = SQLAlchemy()

def timed_task():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"));



def create_app(config_name):
    app = Flask(__name__)
    CORS(app, resources=r'/*')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app=app)
    db.init_app(app=app)

    # 创建当前线程执行的schedulers
    scheduler = BlockingScheduler()
    # 添加调度任务(timed_task),触发器选择interval(间隔性),间隔时长为5秒
    scheduler.add_job(timed_task, 'interval', seconds=5)
    # 启动调度任务
    # scheduler.start()

    Swagger(app, template=template_config, config=swagger_config)

    # 统一错误处理
    from .errors import errors
    app.register_blueprint(errors)

    # 注册到蓝图
    from main.controllers.stock_api import stock_app
    app.register_blueprint(stock_app)
    return app
