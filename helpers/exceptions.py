# -----=====|  |=====-----
# Create by Jules - 12/2023
# -----=====|  |=====-----

# Import library
from flask import jsonify

def NotFoundException() :
    return jsonify({"error": "Not found"}), 404

def InternalServerError(e) :
    return jsonify({"error": f"Internal server error{e}"}), 500