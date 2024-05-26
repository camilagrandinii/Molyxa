from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://camila:1234@localhost:5432/moodboard'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    photoCategory = db.Column(db.String(50))
    src = db.Column(db.String(200))

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'photoCategory': self.photoCategory,
            'src': self.src
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

class MoodBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    items = db.relationship('MoodBoardItem', backref='moodboard', lazy=True)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.as_dict() for item in self.items]
        }

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/api/mood-board', methods=['GET'])
def get_mood_board():
    mood_boards = MoodBoard.query.all()
    return jsonify([mood_board.as_dict() for mood_board in mood_boards])

@app.route('/api/mood-board', methods=['POST'])
def add_to_mood_board():
    data = request.get_json()
    mood_board_name = data.get('name', 'Default Moodboard')
    mood_board_items = data.get('items', [])

    mood_board = MoodBoard(name=mood_board_name)
    db.session.add(mood_board)
    
    for item_data in mood_board_items:
        # Aqui assumimos que 'type' no seu JSON se refere ao tipo do item de moodboard,
        # então vamos usar 'type' para criar um novo item de MoodBoardItem.
        # Se o JSON fornecido se refere a um campo diferente, você precisa ajustar isso de acordo.
        new_item = MoodBoardItem(type=item_data['type'], src=item_data['src'], text=item_data['text'], moodboard=mood_board)
        db.session.add(new_item)
    
    db.session.commit()
    
    return jsonify(mood_board.as_dict()), 201

@app.route('/api/mood-board/<int:mood_board_id>', methods=['DELETE'])
def remove_mood_board(mood_board_id):
    mood_board = MoodBoard.query.get_or_404(mood_board_id)
    db.session.delete(mood_board)
    db.session.commit()
    return jsonify({'message': 'Moodboard removed'}), 200

if __name__ == '__main__':
    app.run(debug=True)
