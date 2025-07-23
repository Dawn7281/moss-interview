# run.py
import sys
import os

# 将当前目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入并运行应用
from src.app import app

if __name__ == '__main__':
    host = os.getenv('RUN_HOST')
    port = os.getenv('RUN_PORT')

    app.run(host=host, port=port, debug=True, use_reloader=False)