import json

from flask import Blueprint, Flask, abort, jsonify, request

from config.ResponseBuilder import ReponseBuilder

from service.stock_account_service import stock_em_account_detail

account_app = Blueprint('account', __name__, url_prefix='/api/account')




@account_app.route('/detail', methods={'get'})
def stock_em_account():
    c = stock_em_account_detail();
    response = ReponseBuilder(True, c.dump_options_with_quotes());
    return json.dumps(response.__dict__);

