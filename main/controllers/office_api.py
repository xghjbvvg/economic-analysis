
from flask import Blueprint, Flask, abort, jsonify, request
from main.config import db
from main.dto.userDto import UserDto
import akshare as ak

from main.models.StockAhNameDict import StockAhNameDict

office_app = Blueprint('office_bp', __name__, url_prefix='/api/office')

session = db.session


@office_app.route('/', methods={'get'})
def offices():
    # abort(403)
    return 'Hello World! my office我的'


@office_app.route('/user/<int:user_id>', methods={'get'})
def get(user_id):
    print(user_id)
    user = UserDto(id=4, name="hcx", password="123456")
    print(type(user))
    session.add(user)
    session.commit()
    return "success";


@office_app.route('/stock_zh_ah_name_dict', methods={'get'})
def stock_zh_ah_name_dict():
    print(6)
    stock_zh_ah_name_dict = ak.stock_zh_ah_name();
    stock_list = [];
    for key in stock_zh_ah_name_dict:
        dict_item = StockAhNameDict();
        dict_item.code = key;
        dict_item.name = stock_zh_ah_name_dict[key];
        stock_list.append(dict_item);
    print(stock_list);
    session.add_all(stock_list)
    session.commit()
    return "success"



