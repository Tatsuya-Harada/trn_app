import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from flask_login import UserMixin,LoginManager,login_user,logout_user,current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
# ログイン機能追加に伴いcookieをフロントから送るにあたりCORS制約回避のためにsupports_credentialsを追加
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])

# SQLiteデータベースの設定、ログインユーザのセッション管理を有効にするためにシークレットキーを設定
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:////mnt/data/{os.environ.get('DATABASE_NAME', 'your-database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='mysecretkey'
# Vue + Flask のような異なるポート間（localhost:5173 → localhost:5000）の通信はクロスサイト（クロスオリジン）
# 通信に分類されるため、そのような場合にセッションを使った認証を行うには以下の設定が必要
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

db = SQLAlchemy(app)
Migrate(app, db)

# ユーザーのログイン状態を管理・維持する仕組みのセットアップ
login_manager = LoginManager()
login_manager.init_app(app)



# 記録_TRN
class TrainingRecord(db.Model):
  __tablename__ = 'training_records'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
  date = db.Column(db.Date, nullable=False)  # 記録の日付
  #リレーション　cascade="all, delete-orphan”：親テーブルのオブジェクトを削除したときに、関連する子テーブルのデータも削除 するための設定
  details = db.relationship('TrainingRecordDetail', backref='trn_record', lazy=True, cascade="all, delete-orphan") 

# 記録_TRN_詳細
class TrainingRecordDetail(db.Model):
  __tablename__ = 'training_record_details'
  id = db.Column(db.Integer, primary_key=True)
  record_id = db.Column(db.Integer, db.ForeignKey('training_records.id'), nullable=False)#記録_TRNの外部キー
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)#種目の外部キー
  weight = db.Column(db.Float, nullable=False)
  goal_reps = db.Column(db.Integer)
  goal_sets = db.Column(db.Integer)
  # リレーション
  sets = db.relationship('SetReps', backref='trn_detail', lazy=True, cascade="all, delete-orphan")
  volume = db.Column(db.Integer)

# 各セットのレップ数
class SetReps(db.Model):
  __tablename__ = 'set_reps'
  id = db.Column(db.Integer, primary_key=True)
  detail_id = db.Column(db.Integer, db.ForeignKey('training_record_details.id'), nullable=False)#記録_TRN_詳細の外部キー
  set_number = db.Column(db.Integer, nullable=False)  # 何セット目か
  reps = db.Column(db.Integer, nullable=False)  # 実際のレップ数

# 種目
class Exercise(db.Model):
  __tablename__= 'exercise'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
  name = db.Column(db.String(50), nullable=False)
  memo = db.Column(db.String(100), nullable=False)
  details = db.relationship('TrainingRecordDetail', backref='exercise_name', lazy=True) 
  details_template = db.relationship('TemplateDetail', backref='exercise_name', lazy=True) 

# TRN_テンプレート
class Template(db.Model):
  __tablename__ = 'template'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
  name = db.Column(db.String(50), nullable=False)
  details = db.relationship('TemplateDetail', backref='template_name', lazy=True, cascade="all, delete-orphan") 

# TRN_テンプレート_詳細
class TemplateDetail(db.Model):
  __tablename__ = 'template_detail'
  id = db.Column(db.Integer, primary_key=True)
  template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)#テンプレートの外部キー
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)#種目の外部キー
  weight = db.Column(db.Float, nullable=False)
  goal_reps = db.Column(db.Integer)
  goal_sets = db.Column(db.Integer)

# ユーザー
class User(db.Model, UserMixin):#UserMixinとはなんだったか
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  records = db.relationship('TrainingRecord', backref='user')
  templates = db.relationship('Template', backref='user')
  exercises = db.relationship('Exercise', backref='user')

# グラフ設定
class UserGraphSetting(db.Model):
  __tablename__ = 'user_graph_settings'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
  order = db.Column(db.Integer, nullable=False)  # 表示順や識別子用



# トレーニング記録を保存
@app.route('/api/records', methods=['POST'])
@login_required
def add_record():
  #POST リクエストが失敗したときに、何が原因なのか分かりにくいのでtry~exceptでエラーメッセージを出す
  try:
    data = request.json

    # フロントから送られる日付は文字列なので、date型に変換
    record_date = datetime.strptime(data['date'], '%Y-%m-%d').date()

    # recordを作成
    new_record = TrainingRecord(date=record_date,user_id=current_user.id)
    db.session.add(new_record)
    db.session.commit()  # ID を確定させる

    #detailsを作成
    #detailsの中はさらに種目ごとに辞書配列で入ってくることが想定されるためforループで取り出す
    for detail in data['details']:
      new_detail = TrainingRecordDetail(
        record_id=new_record.id,  # ID 確定後に取得
        exercise_id=detail['exercise_id'],
        weight=detail['weight'],
        goal_reps=detail['goal_reps'],
        goal_sets=detail['goal_sets'],
        volume=detail['volume']
      )
      db.session.add(new_detail)
      db.session.commit()  # ID を確定させる

      for i, reps in enumerate(detail['sets'], start=1):
        new_set = SetReps(
            detail_id=new_detail.id,  # ID 確定後に取得
            set_number=i,
            reps=reps
        )
        db.session.add(new_set)

      db.session.commit()  # セットデータを保存

    return jsonify({"message": "トレーニング記録を保存しました", "record_id": new_record.id}), 201

  except Exception as e:
    print(f"エラー発生: {e}")  # デバッグ用
    return jsonify({"error": "データの保存に失敗しました", "message": str(e)}), 500

# トレーニング記録を取得（進捗グラフ表示用）
@app.route('/api/records', methods=['GET'])
@login_required
def get_records():
  # モデルの定義に基づきid,日付,detailのオブジェクトリストが入ったdetails属性が入った
  # オブジェクトがレコードの数だけリストに格納されている

  # クエリパラメータ取得。取得するパラメータは文字列型なので数値型に変換する
  exercise_filter = request.args.get('exercise_id',type=int) 

  #種目で絞られてリクエストが来た場合には種目を絞る
  if exercise_filter:
    records = (
      TrainingRecord.query
      .filter_by(user_id=current_user.id)#ログインユーザの記録だけ取得
      .join(TrainingRecord.details)  # リレーションしているdetailsを取得
      .filter(TrainingRecordDetail.exercise_id == exercise_filter)
      .all()
    )
  else:
      records = TrainingRecord.query.all()
  
  data = []
  for record in records:
    record_data = {
        'date': record.date.strftime('%Y-%m-%d'),  # 日付
        'details': []
    }
    
    # 各トレーニング記録の詳細情報を取得
    for detail in record.details:
      #日付で複数種目のレコードがあってもその種目のデータだけ取得できるように条件分岐
      #このコードにより同時に空欄で種目検索しても何もデータが取得されないようにもなった
      if detail.exercise_id == exercise_filter:
        detail_data = {
          'weight': detail.weight,
          'goal_reps': detail.goal_reps,
          'goal_sets': detail.goal_sets,
          'sets': [],
          'volume': detail.volume
        }
        
        # 各セットのレップ数を取得
        for set in detail.sets:
          detail_data['sets'].append({
              'set_number': set.set_number,
              'reps': set.reps
          })
        
        record_data['details'].append(detail_data)
    
    #配列と辞書構造で網羅されたリレーショナルデータ
    data.append(record_data)
  
  print('data:{}'.format(data))
  return jsonify(data)

# グラフ表示設定の保存
@app.route('/api/graph-settings', methods=['POST'])
@login_required
def save_graph_settings():
  data = request.json
  print('data:{}'.format(data))
  user_id = current_user.id

  # 既存の設定を削除（上書きする想定）
  UserGraphSetting.query.filter_by(user_id=user_id).delete()

  # enumerateで取得するインデックスiを表示順として使用
  for i, setting in enumerate(data):  # 例: data = [{"exercise_id": 1}, {"exercise_id": 2}]
    new_setting = UserGraphSetting(
      user_id=user_id,
      exercise_id=setting['exercise_id'],
      order=i
    )
    db.session.add(new_setting)

  db.session.commit()
  return jsonify({'message': '設定を保存しました'})

# 表示順に並べ替えてグラフ表示設定の取得
@app.route('/api/graph-settings', methods=['GET'])
@login_required
def get_graph_settings():
  settings = (UserGraphSetting.query
  .filter_by(user_id=current_user.id)
  .order_by(UserGraphSetting.order)
  .all()
  )
  data = [{'id': s.id, 'exercise_id': s.exercise_id} for s in settings]
  return jsonify(data)

# グラフの削除
@app.route('/api/graph-settings', methods=['DELETE'])
@login_required
def delete_graph_settings():
  try:
    setting_id = request.args.get('setting_id',type=int) 
    graph_setting = UserGraphSetting.query.get(setting_id)

    db.session.delete(graph_setting)
    db.session.commit()

    return jsonify({"message": "グラフ設定の一部を削除しました", "template_id": setting_id}), 200
  
  except Exception as e:
    print(f"エラー発生: {e}")  # デバッグ用
    return jsonify({"error": "データの削除に失敗しました", "message": str(e)}), 500

# 新規追加種目を保存
@app.route('/api/exercise', methods=['POST'])
@login_required
def add_excercise():
  #POST リクエストが失敗したときに、何が原因なのか分かりにくいのでtry~exceptでエラーメッセージを出す
  try:
    data = request.json

    # recordを作成
    new_record = Exercise(
      name=data['exercise_name'],
      user_id=current_user.id,
      memo=data['memo']
    )
    db.session.add(new_record)
    db.session.commit() 

    return jsonify({"message": "新規追加種目を保存しました", "id": new_record.id}), 201

  except Exception as e:
    print(f"エラー発生: {e}")  # デバッグ用
    return jsonify({"error": "データの保存に失敗しました", "message": str(e)}), 500

# 種目レコードをすべて取得（種目選択肢表示用）
# データを返すAPIの場合はページURLと区別するためにapi/任意のapi名とするのが慣習
# 実際はapi/をつけなくてもAPIとして動作はする
@app.route('/api/exercise', methods=['GET'])
@login_required
def get_exercise():

  exercises = Exercise.query.filter_by(user_id=current_user.id).all()
  
  data = [{"id":exercise.id, "exercise_name":exercise.name, "memo":exercise.memo} for exercise in exercises]
  print('data:{}'.format(data))
  return jsonify(data)
# JSON化した後は以下のような配列構造
# [
#   { "id": 1, "exercise_name": "ベンチプレス" },
#   { "id": 2, "exercise_name": "スクワット" },
#   { "id": 3, "exercise_name": "デッドリフト" }
# ]

# 種目を削除
@app.route('/api/exercise', methods=['DELETE'])
@login_required
def delete_exercise():
  try:
    exercise_id = request.args.get('exercise_id',type=int) 
    print('exercise_id:{}'.format(exercise_id))
    exercise = Exercise.query.get(exercise_id)

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": "種目を削除しました", "exercise_id": exercise_id}), 200
  
  except Exception as e:
    print(f"エラー発生: {e}")  # デバッグ用
    return jsonify({"error": "データの削除に失敗しました", "message": str(e)}), 500

# テンプレート詳細含めた全データ取得
@app.route('/api/template', methods=['GET'])
@login_required
def get_template():
  records = (
  Template.query
    .filter_by(user_id=current_user.id)#ログインユーザの記録だけ取得
    .join(Template.details)  # リレーションしているdetailsを取得
    .all()
  )
  
  # テンプレート情報を取得
  data = []
  for record in records:
    record_data = {
      'id':record.id,
      'template_name':record.name,
      'details': []
    }
    
    # テンプレートの詳細情報を取得
    for detail in record.details:
      exercise_name = Exercise.query.filter_by(id = detail.exercise_id).first().name
      detail_data = {
        'id':detail.id,
        'exercise_id':detail.exercise_id, 
        'exercise_name': exercise_name,
        'weight':detail.weight,
        'goal_reps': detail.goal_reps,
        'goal_sets': detail.goal_sets,
      }
          
      record_data['details'].append(detail_data)
    
    data.append(record_data)

  return jsonify(data)

# 新規作成されたテンプレートを保存
@app.route('/api/template', methods=['POST'])
def add_template():
  try:
    data = request.json

    # recordを作成
    new_record = Template(name=data['template_name'],user_id=current_user.id)
    db.session.add(new_record)
    db.session.commit()  # TRN記録の保存と同様にテンプレートデータのIDをまずは確定させる

    # detailsを作成
    # detailsの中はさらに種目ごとに辞書配列で入ってくることが想定されるためforループで取り出す
    for detail in data['details']:
      new_detail = TemplateDetail(
        template_id=new_record.id,  # ID 確定後に取得
        exercise_id=detail['exercise_id'],
        weight=detail['weight'],
        goal_reps=detail['goal_reps'],
        goal_sets=detail['goal_sets']
      )
      db.session.add(new_detail)
      db.session.commit()  # ID を確定させる
    
    return jsonify({"message": "テンプレートを保存しました", "template_id": new_record.id}), 201

  except Exception as e:
    print(f"エラー発生: {e}")  # デバッグ用
    return jsonify({"error": "データの保存に失敗しました", "message": str(e)}), 500
    
# テンプレートの更新を保存
#受け取ったテンプレートIDを元にそれに紐づく詳細を上書き
@app.route('/api/template', methods=['PUT'])
@login_required
def change_template():
  try:
    data = request.json
    print('data:{}'.format(data))

    template_id = request.args.get('template_id',type=int) 
    print(template_id)
    template = Template.query.get(template_id)
    template.name = data.get('template_name', template.name) #入力された値が無ければ元の値を格納する

    for detail in data['details']:
      for i,template_detail in enumerate(template.details):
        if detail.get('id') == template_detail.id: #フロントから送られてくるデータにテンプレート詳細idは含まてているか？
          template.details[i].exercise_id=detail.get('exercise_id', template.details[i].exercise_id)
          template.details[i].weight = detail.get('weight', template.details[i].weight)
          template.details[i].goal_reps = detail.get('goal_reps', template.details[i].goal_reps)
          template.details[i].goal_sets = detail.get('goal_sets', template.details[i].goal_sets)
          break
      # 既存のレコードの上書きでない場合はレコードを上書きではなく追加する
      else:
        new_detail = TemplateDetail(
        template_id=template_id,
        exercise_id=detail['exercise_id'],
        weight=detail['weight'],
        goal_reps=detail['goal_reps'],
        goal_sets=detail['goal_sets']
      )
        db.session.add(new_detail)

    db.session.commit()

    return jsonify({"message": "テンプレートを更新しました", "template_id": template_id}), 201
  
  except Exception as e:
    print(f"エラー発生: {e}")  # デバッグ用
    return jsonify({"error": "データの保存に失敗しました", "message": str(e)}), 500

# テンプレートを削除
@app.route('/api/template', methods=['DELETE'])
@login_required
def delete_template():
  try:
    template_id = request.args.get('template_id',type=int) 
    print('template_id:{}'.format(template_id))
    template = Template.query.get(template_id)

    db.session.delete(template)
    db.session.commit()

    return jsonify({"message": "テンプレートを削除しました", "template_id": template_id}), 200
  
  except Exception as e:
    print(f"エラー発生: {e}")  # デバッグ用
    return jsonify({"error": "データの削除に失敗しました", "message": str(e)}), 500
    
# 新規追加・更新時における詳細の削除
@app.route('/api/template/detail', methods=['DELETE'])
@login_required
def delete_template_detail():
  try:
    detail_id = request.args.get('detail_id',type=int) 
    # print('detail_id:{}'.format(detail_id))
    template_detail = TemplateDetail.query.get(detail_id)

    db.session.delete(template_detail)
    db.session.commit()

    return jsonify({"message": "テンプレート詳細一部を削除しました", "template_id": detail_id}), 200
  
  except Exception as e:
    print(f"エラー発生: {e}")  # デバッグ用
    return jsonify({"error": "データの削除に失敗しました", "message": str(e)}), 500

# 新規ユーザー登録 
@app.route('/api/register', methods=['POST'])
def register():
  data = request.json
  if User.query.filter_by(username=data['user_name']).first():
    return jsonify({"error": "ユーザー名は既に存在します"}), 400
  
  hashed_pw = generate_password_hash(data['password'])
  new_user = User(username=data['user_name'], password_hash=hashed_pw)
  db.session.add(new_user)
  db.session.commit()
  return jsonify({"message": "登録完了"}), 201

# ログイン
@app.route('/api/login', methods=['POST'])
def login():
  data = request.json
  print('data:{}'.format(data))
  user = User.query.filter_by(username=data['user_name']).first()

  # 入力したパスワードがハッシュ化してDBに保存したものと一致していればログインしidがセッションに保存される
  if user and check_password_hash(user.password_hash, data['password']):
    login_user(user)
    return jsonify({"message": "ログイン成功", "user_id": user.id})
  
  return jsonify({"error": "ログイン失敗"}), 401

# ログアウト
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "ログアウトしました"})

# ログイン中ユーザの取得
@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user():
  return jsonify({"user_id":current_user.id,"user_name": current_user.username})

#ユーザーのセッション管理
@login_manager.user_loader
def load_user(user_id):
  print('user_id:{}'.format(user_id))
  return User.query.get(int(user_id))



if __name__ == '__main__':
  # with app.app_context():
  #     db.drop_all()
  #     db.create_all()
  app.run(debug=True)