from flask import jsonify

def NotFoundException() :
    return jsonify({"error": "Not found"}), 404

def InternalServerError(e) :
    return jsonify({"error": "Internal server error" + e}), 500