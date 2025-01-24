
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)

class Banlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(500), nullable=True)
    added_by = db.Column(db.String(100), nullable=True)

def init_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/banlist', methods=['GET'])
def get_banlist():
    banlist = Banlist.query.all()
    return jsonify([{'id': card.id, 'card_name': card.card_name, 'reason': card.reason, 'added_by': card.added_by} for card in banlist])

@app.route('/api/banlist', methods=['POST'])
def add_card():
    data = request.get_json()
    new_card = Banlist(
        card_name=data.get('card_name'),
        reason=data.get('reason'),
        added_by=data.get('added_by')
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify({'message': 'Card added successfully!'}), 201

@app.route('/api/banlist/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = Banlist.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    return jsonify({'message': 'Card deleted successfully!'}), 200

@app.route('/api/banlist/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    data = request.get_json()
    card = Banlist.query.get_or_404(card_id)
    card.card_name = data.get('card_name', card.card_name)
    card.reason = data.get('reason', card.reason)
    card.added_by = data.get('added_by', card.added_by)
    db.session.commit()
    return jsonify({'message': 'Card updated successfully!'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    init_db()
    app.run(host='0.0.0.0', port=port, debug=True)
