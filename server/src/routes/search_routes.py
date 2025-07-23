from datetime import datetime
import os
from src.GraphBase.handle_graph import GraphHandler
from src.db.graph_history import GraphHistory
from src.db.user import User
from src.utils.kg import build_knowledge_graph, summary_word, build_knowledge_graph_from_keywords
from flask import Blueprint, request, jsonify
from src.modules.learn_search_new import learn_search
from src.db.graph import Graph
from src.db.learn import Learn
from src.utils.extensions import db
import json

relate_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

search_bp = Blueprint('search', __name__, url_prefix='/api/search')

@search_bp.route('/get-search', methods=['POST'])
def get_search():
    data = request.json
    keyword = data.get('keyword')

    if not keyword:
        return jsonify({'error': '关键词不能为空'}), 400

    learn = Learn.query.filter_by(key=keyword).first()
    if learn:
        result = learn.value
    else:
        result = learn_search(keyword)
        learn = Learn(key=keyword, value=result)
        db.session.add(learn)
        db.session.commit()

    return jsonify(json.loads(result))

graph_handle = GraphHandler()

@search_bp.route('/get-graph', methods=['POST'])
def get_graph():
    data = request.json
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    graph_history = GraphHistory.query.filter_by(user_id=user.id).all()

    if not graph_history:
        return jsonify({'error': '请先构建知识图谱'}), 400

    graph = Graph.query.filter_by(id=graph_history[-1].graph_id).first()

    graph_handle.create_graph(graph.value)
    graph_json = graph_handle.get_graph()

    return jsonify({'graph': graph_json, 'history': [{'keyword': gh.search_keyword, 'time': gh.time} for gh in graph_history]})

@search_bp.route('/update-graph', methods=['POST'])
def update_graph():
    data = request.json
    seed = data.get('keyword')
    username = data.get('username')

    user = User.query.filter_by(username=username).first()

    if not seed:
        return jsonify({'error': '关键词不能为空'}), 400

    graph_history = GraphHistory.query.filter_by(user_id=user.id, search_keyword=seed).first()
    if graph_history:
        graph = Graph.query.filter_by(id=graph_history.graph_id).first()
        graph_handle.create_graph(graph.value)
        graph_json = graph_handle.get_graph()

        graph_history = GraphHistory.query.filter_by(user_id=user.id).all()
        return jsonify({'graph': graph_json, 'history': [{'keyword': gh.search_keyword, 'time': gh.time} for gh in graph_history]})

    if Graph.query.filter(Graph.key.cast(db.String).like(f'%"{seed}"%')).first():
        graph = Graph.query.filter(Graph.key.cast(db.String).like(f'%"{seed}"%')).first()

        graph_handle.create_graph(graph.value)
        graph_json = graph_handle.get_graph()

        graph_history = GraphHistory(user_id=user.id, graph_id=graph.id, search_keyword=seed, time=datetime.now())
        db.session.add(graph_history)
        db.session.commit()

        graph_history = GraphHistory.query.filter_by(user_id=user.id).all()
        return jsonify({'graph': graph_json, 'history': [{'keyword': gh.search_keyword, 'time': gh.time} for gh in graph_history]})

    graphs, key = build_knowledge_graph(seed, max_depth=2, max_nodes=50)

    graph_handle.create_graph(graphs)
    graph_json = graph_handle.get_graph()

    graph = Graph(key=key, value=graphs)
    db.session.add(graph)
    db.session.commit()

    graph_history = GraphHistory(user_id=user.id, graph_id=graph.id, search_keyword=seed, time=datetime.now())
    db.session.add(graph_history)
    db.session.commit()

    graph_history = GraphHistory.query.filter_by(user_id=user.id).all()
    return jsonify({'graph': graph_json, 'history': [{'keyword': gh.search_keyword, 'time': gh.time} for gh in graph_history]})

@search_bp.route('/feedback-graph', methods=['POST'])
def feedback_graph():
    data = request.json
    feedback = data.get('feedback')
    username = data.get('username')
    user = User.query.filter_by(username=username).first()

    keywords = summary_word(feedback)
    graphs = build_knowledge_graph_from_keywords(keywords)

    graph_handle.create_graph(graphs)
    graph_json = graph_handle.get_graph()

    graph = Graph(key=keywords, value=graphs)
    db.session.add(graph)
    db.session.commit()

    graph_history = GraphHistory(user_id=user.id, graph_id=graph.id, search_keyword=keywords[0], time=datetime.now())
    db.session.add(graph_history)
    db.session.commit()

    graph_history = GraphHistory.query.filter_by(user_id=user.id).all()
    return jsonify({'graph': graph_json, 'history': [{'keyword': gh.search_keyword, 'time': gh.time} for gh in graph_history]})
