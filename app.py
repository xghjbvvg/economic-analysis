from pathlib import Path

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

from config.errors import errors
from main.config.config import config, template_config, swagger_config
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pymongo

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["economic_analysis"]

stock_zh_a_new_col = mongodb["stock_zh_a_new"];
stock_analyst_rank_col = mongodb["stock_analyst_rank"];

db = SQLAlchemy()
rootpath = str((Path(__file__).parent).absolute());
app_port = 5000;
def timed_task():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"));


def create_app(config_name):
    app = Flask(__name__)
    CORS(app, resources=r'/*')

    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}});
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

    app.register_blueprint(errors)

    # 注册到蓝图
    from main.controllers.stock_api import stock_app
    from main.controllers.stock_account_api import account_app

    app.register_blueprint(stock_app)
    app.register_blueprint(account_app);
    CORS(account_app)
    return app


app = create_app("default")

@app.route("/")
def index():
    return "hello,world"


if __name__ == '__main__':
    # app = create_app("default")
    app.run(
        host='0.0.0.0',
        port=app_port,
        debug=True
    );
