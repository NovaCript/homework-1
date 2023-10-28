from flask import Flask, request, jsonify
from twit import Twit
from user import User

app = Flask(__name__)

users = []
twits = []


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(len(users)+1, data['username'])
    users.append(new_user)
    return jsonify(new_user.to_dict())


@app.route('/users', methods=['GET'])
def get_users():
    serialized_users = [user.to_dict() for user in users]
    return jsonify(serialized_users)


@app.route('/twits', methods=['POST'])
def create_twit():
    data = request.get_json()
    author_id = data.get('author_id')
    author = next((user for user in users if user.id == author_id), None)
    if author:
        new_twit = Twit(len(twits)+1, data['body'], author)
        twits.append(new_twit)
        return jsonify(new_twit.to_dict())
    return jsonify({'message': 'Author not found'}), 404


@app.route('/twits', methods=['GET'])
def get_twits():
    serialized_twits = [twit.to_dict() for twit in twits]
    return jsonify(serialized_twits)


@app.route('/twits/<int:twit_id>', methods=['PUT'])
def update_twit(twit_id):
    data = request.get_json()
    twit = next((twit for twit in twits if twit.id == twit_id), None)
    if twit:
        twit.body = data.get('body', twit.body)
        return jsonify(twit.to_dict())
    return jsonify({'message': 'Twit not found'}), 404


# Route for deleting a twit
@app.route('/twits/<int:twit_id>', methods=['DELETE'])
def delete_twit(twit_id):
    global twits
    twits = [twit for twit in twits if twit.id != twit_id]
    return jsonify({'message': 'Twit deleted'})


if __name__ == '__main__':
    app.run(debug=True)
