import datetime
from flask import Blueprint, request, jsonify
from src.db.user import User
from src.utils.extensions import db
from src.db.check_in import CheckIn

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}),400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': '该邮箱已注册'}),400
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': '注册成功'})

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': '用户名不存在'}),400
    if user.password != password:
        return jsonify({'error': '密码错误'}),400
    else:
        return jsonify({'message': '登录成功'})

@user_bp.route('/revise-requirement', methods=['POST'])
def revise_requirement():
    data = request.json
    username = data.get('username')
    education = data.get('education')
    major = data.get('major')
    experience = data.get('experience')
    skills = data.get('skills')
    certs = data.get('certs')
    fresh = data.get('fresh')

    user = User.query.filter_by(username=username).first()
    user.education = education
    user.major = major
    user.experience = experience
    user.skills = skills
    user.certs = certs
    user.fresh = fresh
    db.session.commit()
    return jsonify({'message': '岗位要求已保存！'})

@user_bp.route('get-requirement/<username>', methods=['GET'])
def get_requirement(username):
    user = User.query.filter_by(username=username).first()
    return jsonify({
        'education': user.education,
        'major': user.major,
        'experience': user.experience,
        'skills': user.skills,
        'certs': user.certs,
        'fresh': user.fresh
    })

@user_bp.route('/revise-skills', methods=['POST'])
def revise_skills():
    data = request.json
    username = data.get('username')
    type = data.get('type')
    name = data.get('name')
    level = data.get('level')
    scene = data.get('scene')
    filename = data.get('filename')

    user = User.query.filter_by(username=username).first()
    user.skills_type = type
    user.skills_name = name
    user.skills_level = level
    user.skills_scene = scene
    user.skills_filename = filename
    db.session.commit()
    return jsonify({'message': '技能已保存！'})

@user_bp.route('/get-skills/<username>', methods=['GET'])
def get_skills(username):
    user = User.query.filter_by(username=username).first()
    return jsonify({
        'type': user.skills_type,
        'name': user.skills_name,
        'level': user.skills_level,
        'scene': user.skills_scene,
    })

@user_bp.route('/edit-user-info', methods=['POST'])
def edit_user_info():
    data = request.json
    name = data.get('username')
    realname = data.get('realname')
    username = data.get('nickname')
    gender = data.get('gender')
    bio = data.get('bio')
    location = data.get('location')
    graduation_year = data.get('graduationYear')
    education = data.get('education')
    university = data.get('university')
    major = data.get('major')

    user = User.query.filter_by(username=name).first()
    if username != name:
        if User.query.filter_by(username=username).first():
            return jsonify({"error": '用户名已存在'}),400
    user.realname = realname
    user.username = username
    user.gender = gender
    user.bio = bio
    user.location = location
    user.graduation_year = graduation_year
    user.education = education
    user.university = university
    user.major = major
    db.session.commit()

    return jsonify({"message": "success"})

@user_bp.route('/get-user-info/<username>', methods=['GET'])
def get_user_info(username):
    user = User.query.filter_by(username=username).first()

    return jsonify({
        'realname': user.realname,
        'nickname': user.username,
        'gender': user.gender,
        'bio': user.bio,
        'location': user.location,
        'graduationYear': user.graduation_year,
        'education': user.education,
        'university': user.university,
        'major': user.major,
    })


@user_bp.route('/edit-job-info', methods=['POST'])
def edit_job_info():
    data = request.json
    username = data.get('username')
    job_position = data.get('position')
    job_requirement = data.get('jobRequirements')
    job_status = data.get('status')
    job_salary = data.get('salaryRange')
    job_city = data.get('workLocation')

    user = User.query.filter_by(username=username).first()
    user.job_position = job_position
    user.job_requirement = job_requirement
    user.job_status = job_status
    user.job_salary = job_salary
    user.job_city = job_city
    db.session.commit()

    return jsonify({"message": "success"})

@user_bp.route('/get-job-info/<username>', methods=['GET'])
def get_job_info(username):
    user = User.query.filter_by(username=username).first()

    return jsonify({
        'position': user.job_position,
        'jobRequirements': user.job_requirement,
        'status': user.job_status,
        'salaryRange': user.job_salary,
        'workLocation': user.job_city,
    })

@user_bp.route('/edit-interview-info', methods=['POST'])
def edit_interview_info():
    data = request.json
    username = data.get('username')
    realname = data.get('name')
    major = data.get('major')
    job_position = data.get('expectedPosition')
    job_requirement = data.get('jobRequirements')

    user = User.query.filter_by(username=username).first()
    user.realname = realname
    user.major = major
    user.job_position = job_position
    user.job_requirement = job_requirement
    db.session.commit()

    return jsonify({"message": "success"})

@user_bp.route('/get-interview-info/<username>', methods=['GET'])
def get_interview_info(username):
    user = User.query.filter_by(username=username).first()

    return jsonify({
        'name': user.realname,
        'major': user.major,
        'expectedPosition': user.job_position,
        'jobRequirements': user.job_requirement,
    })

@user_bp.route('/get-check-in', methods=['POST'])
def get_check_in():
    data = request.json
    username = data.get('username')

    check_in = CheckIn.query.filter_by(user=username).first()
    if not check_in:
        check_in = CheckIn(user=username, continue_count=0, total_count=0)
        db.session.add(check_in)
        db.session.commit()
        return jsonify({'continue_count': 0, 'total_count': 0, 'is_checked_in': False})

    is_checked_in = check_in.date == datetime.date.today()
    return jsonify({
        'continue_count': check_in.continue_count,
        'total_count': check_in.total_count,
        'is_checked_in': is_checked_in
    })

@user_bp.route('/update-check-in', methods=['POST'])
def update_check_in():
    data = request.json
    username = data.get('username')

    check_in = CheckIn.query.filter_by(user=username).first()
    if not check_in:
        check_in = CheckIn(user=username, continue_count=0, total_count=0)
        db.session.add(check_in)

    today = datetime.date.today()
    if check_in.date == today:
        return jsonify({'message': '今天已经打卡过了！'}), 400

    if check_in.date == today - datetime.timedelta(days=1):
        check_in.continue_count += 1
    else:
        check_in.continue_count = 1

    check_in.total_count += 1
    check_in.date = today
    db.session.commit()

    return jsonify({'message': '打卡成功！', 'continue_count': check_in.continue_count, 'total_count': check_in.total_count})