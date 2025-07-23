from flask import Blueprint, request, jsonify
from src.db.experience import Experience
from src.db.user import User
from src.utils.extensions import db

experience_bp = Blueprint('experience', __name__, url_prefix='/api/experience')

@experience_bp.route('/add', methods=['POST'])
def add_experience():
    data = request.json
    username = data.get('username')
    title = data.get('title')
    content = data.get('content')
    full_content = data.get('fullContent')
    content_type = data.get('contentType')
    level = data.get('level')
    time = data.get('time')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': '请先登录'}), 400
    school = user.university
    experience = Experience(
        user=username,
        title=title,
        content=content,
        full_content=full_content,
        content_type=content_type,
        level=level,
        time=time,
        school=school
    )
    db.session.add(experience)
    db.session.commit()

    return jsonify({'message': '提交成功'})

@experience_bp.route('/list', methods=['GET'])
def list_experiences():
    experiences = Experience.query.all()
    return jsonify([{
        'username': e.user,
        'title': e.title,
        'content': e.content,
        'fullContent': e.full_content,
        'contentType': e.content_type,
        'level': e.level,
        'school': e.school if e.school else '未知学校',
        'time': e.time
    } for e in experiences])

@experience_bp.route('/get', methods=['POST'])
def get_experience():
    data = request.json
    username = data.get('username')

    experiences = Experience.query.filter_by(user=username).all()
    if not experiences:
        return jsonify({'error': '用户未发布内容'}), 400

    return jsonify([{
        'id': e.id,
        'username': e.user,
        'title': e.title,
        'content': e.content,
        'fullContent': e.full_content,
        'contentType': e.content_type,
        'level': e.level,
        'school': e.school if e.school else '未知学校',
        'time': e.time
    } for e in experiences])