from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://camila:1234@localhost:5432/molyxa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class MoodBoardItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elementCategory = db.Column(db.String(50))
    photoCategory = db.Column(db.String(50))
    src = db.Column(db.String(200))
    name = db.Column(db.String(200))
    mood_board_id = db.Column(db.Integer, db.ForeignKey('mood_board.id'))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    def as_dict(self):
        return {
            'id': self.id,
            'elementCategory': self.elementCategory,
            'photoCategory': self.photoCategory,
            'src': self.src,
            'name': self.name,
            'mood_board_id': self.mood_board_id,
            'x': self.x,
            'y': self.y
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
        new_item = MoodBoardItem(elementCategory=item_data['elementCategory'], 
                                 photoCategory=item_data['photoCategory'], 
                                 src=item_data['src'], 
                                 name=item_data['name'],
                                 x=item_data['x'],
                                 y=item_data['y'],
                                 moodboard=mood_board)
        db.session.add(new_item)
    
    db.session.commit()
    
    return jsonify(mood_board.as_dict()), 201

@app.route('/api/mood-board/<int:mood_board_id>/add-item', methods=['POST'])
def add_item_to_mood_board(mood_board_id):
    data = request.get_json()
    mood_board = MoodBoard.query.get_or_404(mood_board_id)
    
    new_item = MoodBoardItem(
        elementCategory=data['elementCategory'],
        photoCategory=data['photoCategory'],
        src=data['src'],
        name=data['name'],
        x=data['x'],
        y=data['y'],
        mood_board=mood_board
    )
    
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify(new_item.as_dict()), 201

@app.route('/api/mood-board/<int:mood_board_id>/remove-item/<int:item_id>', methods=['DELETE'])
def remove_item_from_mood_board(mood_board_id, item_id):
    mood_board = MoodBoard.query.get_or_404(mood_board_id)
    item = MoodBoardItem.query.filter_by(id=item_id, mood_board_id=mood_board_id).first_or_404()
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Item removed from moodboard'}), 200


@app.route('/api/mood-board/<int:mood_board_id>', methods=['DELETE'])
def remove_mood_board(mood_board_id):
    mood_board = MoodBoard.query.get_or_404(mood_board_id)
    db.session.delete(mood_board)
    db.session.commit()
    return jsonify({'message': 'Moodboard removed'}), 200

@app.route('/api/clear-moodboards', methods=['DELETE'])
def clear_moodboards():
    try:
        # Deleta todos os itens do moodboard primeiro
        MoodBoardItem.query.delete()
        # Em seguida, deleta todos os moodboards
        MoodBoard.query.delete()
        db.session.commit()
        return jsonify({'message': 'All moodboards cleared successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
