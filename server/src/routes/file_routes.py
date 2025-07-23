from flask import Blueprint, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from src.db.user import User
from src.utils.extensions import db
from src.modules.resume_optimizer import *

relate_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
file_bp = Blueprint('upload', __name__, url_prefix='/api')

UPLOAD_CERTIFICATE_FOLDER = os.path.join(relate_path, 'data/certificate')
os.makedirs(UPLOAD_CERTIFICATE_FOLDER, exist_ok=True)
UPLOAD_RESUME_FOLDER = os.path.join(relate_path, 'data/cvs')
os.makedirs(UPLOAD_RESUME_FOLDER, exist_ok=True)


@file_bp.route('/upload-certificate', methods=['POST'])
def upload_certificate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_CERTIFICATE_FOLDER, filename)
    file.save(save_path)

    return jsonify({'message': 'File uploaded successfully', 'filename': filename})

@file_bp.route('/upload-resume/<username>', methods=['POST'])
def upload_resume(username):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename[:-4] + "-active.pdf"

    user = User.query.filter_by(username=username).first()
    user.resume_name = filename
    db.session.commit()

    save_path = os.path.join(UPLOAD_RESUME_FOLDER, filename)
    file.save(save_path)

    return jsonify({'message': 'File uploaded successfully', 'filename': filename})

@file_bp.route('/resume-optimization', methods=['POST'])
def resume_optimization():
    data = request.json
    print(data)
    filename = data.get('filename')
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    file_path = os.path.join(UPLOAD_RESUME_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    advice_path = os.path.join(UPLOAD_RESUME_FOLDER, filename[:-11] + "-feedback.json")

    if os.path.exists(advice_path):
        with open(advice_path, 'r', encoding='utf-8') as f:
            advice = json.load(f)
        return jsonify({'advice': advice})

    cv_json = parse_resume(file_path)

    optimizer = ResumeOptimizer(
        user.job_position if user.job_position else "",
        user.job_requirement if user.job_requirement else "",
    )
    advice = optimizer.optimize_resume(cv_json, filename)

    result = json.loads(str(advice).replace('```json\n', '').replace('```', '').replace("\\n", "\n"))

    with open(advice_path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    return jsonify({'message': 'Resume optimized successfully', 'advice': result})

@file_bp.route('/get-resume/<username>', methods=['GET'])
def get_resume(username):
    user = User.query.filter_by(username=username).first()

    if not user or not user.resume_name:
        return jsonify({'error': 'User or resume not found'}), 404

    path = os.path.join(UPLOAD_RESUME_FOLDER, user.resume_name)
    print(path)
    if not os.path.exists(path):
        return jsonify({'error': 'Resume file not found'}), 404
    return send_file(path, as_attachment=True, download_name=user.resume_name[:-11]+".pdf", mimetype='application/pdf')
