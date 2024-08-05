import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

#GET ALL
@app.route('/members', methods=['GET'])
def handle_hello():
    try:
        members = jackson_family.get_all_members()
        return jsonify({"members": members}), 200
    except:
        return jsonify({"error": "Internal Server Error"}), 500

#ADD
@app.route('/member', methods=['POST'])
def add_new_member():
    try:
        request_body = request.json
        new_member = jackson_family.add_member(request_body)
        if "error" in new_member:
            return jsonify({"error": new_member["error"]}), 400
        return jsonify({"message": "Member added successfully", "members": jackson_family.get_all_members()}), 200
        
    except:
        return jsonify({"error": "Internal Server Error"}), 500

#DELETE
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        response = jackson_family.delete_member(id)
        if "error" in response:
            return jsonify({"error": response["error"]}), 400
        return jsonify({"message": "Member deleted successfully"}), 200
    except:
        return jsonify({"error": "Internal Server Error"}), 500

#GET ONE
@app.route('/member/<int:id>', methods=['GET']) 
def get_member(id):
    try:
        member = jackson_family.get_member(id)
        if "error" in member:
            return jsonify({"error": member["error"]}), 400
        return jsonify({"member": member}), 200
    except:
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
