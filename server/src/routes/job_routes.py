from flask import Blueprint, request, jsonify
from src.db.job_info import JobInfo
from sqlalchemy import or_

job_bp = Blueprint('job', __name__, url_prefix='/api/job')


@job_bp.route('/get-job', methods=['POST'])
def get_job():
    data = request.json
    print(data)

    location = data.get('location')
    title = data.get('title')
    search = data.get('search')
    # New: Get page number and items per page
    page = data.get('page', 1)  # Default to page 1 if not provided
    per_page = data.get('per_page', 20) # Default to 20 items per page

    # Start with the base query
    query = JobInfo.query

    # 1. Apply global search 'search' condition (if present)
    if search and search.strip():
        search_term = search.strip()
        query = query.filter(
            or_(
                JobInfo.title.ilike(f'%{search_term}%'),
                JobInfo.company.ilike(f'%{search_term}%')
            )
        )

    # 2. Independently apply 'location' condition (if present and not 'all')
    if location and location != 'all':
        query = query.filter_by(location=location)

    # 3. Independently apply 'title' condition (if present and not 'all')
    if title and title != 'all':
        query = query.filter(JobInfo.title.ilike(f'%{title}%'))

    # New: Apply pagination
    # Use Flask-SQLAlchemy's paginate method for easier pagination
    paginated_jobs = query.paginate(page=page, per_page=per_page, error_out=False)
    job_infos = paginated_jobs.items

    formatted_job_list = []
    for job in job_infos:
        formatted_job_list.append({
            'location': job.location,
            'industry': job.industry,
            'companySize': job.scale,
            'companyName': job.company,
            'title': job.title,
            'salary': job.salary,
            'experience': job.experience,
            'address': job.address,
            'education': job.education,
            'description': job.description,
            'skills': job.tags.split(',') if job.tags else [],
            'updateTime': job.postTime.replace('更新于 ', '') if job.postTime else ''
        })

    print("job_infos", job_infos)
    return jsonify({
        'data': formatted_job_list,
        'totalItems': paginated_jobs.total, # Total number of items
        'totalPages': paginated_jobs.pages, # Total number of pages
        'currentPage': paginated_jobs.page, # Current page number
        'status': 200,
        'statusText': 'OK'
    })
