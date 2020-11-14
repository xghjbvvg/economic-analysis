from flask import Response, jsonify
import json
import redis   # 导入redis 模块

redis_menu = "stock:";
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
redis = redis.Redis(connection_pool=pool)
