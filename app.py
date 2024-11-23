import sys
sys.path.append('/usr/local/lib/python3.9/dist-packages')
from flask import Flask
from todo.todo import todo_module

app = Flask(__name__)

app.register_blueprint(todo_module)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)