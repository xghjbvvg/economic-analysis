import json

from flask import Blueprint
from flask_restful.reqparse import RequestParser

from config.ResponseBuilder import ReponseBuilder

from service.stock_account_service import stock_em_account_detail, stock_em_analyst_rank, stock_em_analyst_info, \
    stock_em_analyst_exponent

account_app = Blueprint('account', __name__, url_prefix='/api/account')

#获取每月新增投资人折线图
@account_app.route('/detail', methods={'get'})
def stock_em_account():
    c = stock_em_account_detail();
    response = ReponseBuilder(True, c.dump_options_with_quotes());
    return json.dumps(response.__dict__);
# 获取投资人排行榜
@account_app.route('/analyst_rank', methods={'get'})
def stock_em_analyst_rank_api():
    list = stock_em_analyst_rank()
    response = ReponseBuilder(True, list);
    return json.dumps(response.__dict__);

#获取投资人股票详情
@account_app.route('/analyst_info/<int:code>', methods={'get'})
def stock_em_analyst_info_api(code):
    parser = RequestParser()
    # parser.add_argument("id", location="json", action="append")

    req = parser.parse_args(strict=True)

    info = stock_em_analyst_info(code)
    response = ReponseBuilder(True, info);
    return json.dumps(response.__dict__);


# 获取投资人指数折线图
@account_app.route('/analyst_exponent/<int:code>', methods={'get'})
def stock_em_analyst_exponent_api(code):

    info = stock_em_analyst_exponent(code)
    response = ReponseBuilder(True, info);
    return json.dumps(response.__dict__);