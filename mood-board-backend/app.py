from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://camila:1234@localhost:5432/moodboard'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    src = db.Column(db.String(200))
    text = db.Column(db.String(200))

    def as_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'src': self.src,
            'text': self.text
        }

class MoodBoardItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    src = db.Column(db.String(200))
    text = db.Column(db.String(200))

    def as_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'src': self.src,
            'text': self.text
        }

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/api/elements', methods=['GET'])
def get_elements():
    elements = Element.query.all()
    return jsonify([element.as_dict() for element in elements])

@app.route('/api/elements', methods=['POST'])
def add_element():
    data = request.get_json()
    new_element = Element(type=data['type'], src=data['src'], text=data['text'])
    db.session.add(new_element)
    db.session.commit()
    return jsonify(new_element.as_dict()), 201

@app.route('/api/mood-board', methods=['GET'])
def get_mood_board():
    mood_board_items = MoodBoardItem.query.all()
    return jsonify([item.as_dict() for item in mood_board_items])

@app.route('/api/mood-board', methods=['POST'])
def add_to_mood_board():
    data = request.get_json()
    new_item = MoodBoardItem(type=data['type'], src=data['src'], text=data['text'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.as_dict()), 201

@app.route('/api/mood-board/<int:item_id>', methods=['DELETE'])
def remove_from_mood_board(item_id):
    item = MoodBoardItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed from mood board'}), 200

if __name__ == '__main__':
    app.run(debug=True)
