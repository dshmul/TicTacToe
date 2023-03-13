from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Score(db.Model): #TODO: change to "Score"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    date = db.Column(db.String())
    score = db.Column(db.Integer)
    grid_size = db.Column(db.Integer, nullable=False) # 3: 3x3, 10: 10x10

'''To init db from python terminal
from api import db
db.create_all()
'''

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing.'}, 401)
        
        try: # TODO: fix error
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"]) # resulting in jwt.exceptions.ExpiredSignatureError: Signature has expired
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message', 'Token is invalid.'}, 401)
        
        return f(current_user, *args, **kwargs)

    return decorated
    
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        output.append(user_data)

    return jsonify({'users': output})

@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found.'})
    
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    
    return jsonify({'user': user_data})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json() # expects {"name": <name>, "password": <password>}

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found.'})
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted.'})

@app.route('/login')
def login():
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Requred."'})
    
    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Requred."'})
    
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token})
    
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Requred."'})

@app.route('/score', methods=['POST'])
@token_required
def add_score(current_user):
    data = request.get_json() # expects {"score": <score>, "grid_size": <grid_size>} 

    new_score = Score(user_id=current_user.public_id, date=datetime.datetime.now(), score=data['score'], grid_size=data['grid_size'])
    db.session.add(new_score)
    db.session.commit()

    return jsonify({'message': 'New score added.'})

@app.route('/score', methods=['GET'])
def get_all_scores():
    scores = Score.query.all()

    output = []
    for score in scores:
        score_data = {}
        score_data['user_id'] = score.user_id
        score_data['date'] = score.date
        score_data['score'] = score.score
        score_data['grid_size'] = score.grid_size
        output.append(score_data)

    return jsonify({'scores': output})

@app.route('/score/<grid_size>', methods=['GET'])
@token_required
def get_user_score(current_user, grid_size):
    scores = Score.query.filter_by(user_id=current_user.public_id, grid_size=grid_size).order_by(Score.date.desc()).all()

    output = []
    for score in scores:
        score_data = {}
        score_data['date'] = score.date
        score_data['score'] = score.score
        output.append(score_data)

    return jsonify({'scores': output})

@app.route('/scoreboard/<grid_size>', methods=['GET']) # scoreboard defines queries with join
def get_grid_scoreboard(grid_size):
    entries = db.session.query(Score.user_id, Score.date, Score.score, Score.grid_size, User.public_id, User.name)\
        .select_from(Score).join(User, Score.user_id==User.public_id).order_by(Score.score.desc()).limit(10).all()

    if not entries:
        return jsonify({'message': 'No entries found.'})

    output = []
    for entry in entries:
        entry_data = {}
        entry_data['user_id'] = entry.user_id
        entry_data['user_name'] = entry.name
        entry_data['date'] = entry.date
        entry_data['score'] = entry.score
        output.append(entry_data)

    return jsonify({'scoreboard': output})


@app.route('/score/<user_id>', methods=['DELETE'])
def delete_user_entries(user_id):
    entries = Score.query.filter_by(user_id=user_id).all()

    if not entries:
        return jsonify({'message': 'No user entries found.'})

    for entry in entries:
        db.session.delete(entry)
    db.session.commit()

    return jsonify({'message': 'User entries deleted.'})

if __name__ == '__main__':
    app.run(port=8000, debug=True)