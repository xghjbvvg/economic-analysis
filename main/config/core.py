from flask import Response, jsonify
import json


def res(builder):
    return jsonify(str(builder));