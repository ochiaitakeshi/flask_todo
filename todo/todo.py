import sys
sys.path.append('/usr/local/lib/python3.9/dist-packages')
from flask import Blueprint, request, render_template
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:///db/todo.db', echo=True)

Base = declarative_base()

class ToDo(Base):

    id = Column(Integer, autoincrement=True)
    task = Column(String(length=65535), primary_key=True)
    status = Column(String(length=255))

    __tablename__ = 'todo'

# Create(DBが未生成ならば生成)
Base.metadata.create_all(bind=engine)

todo_module = Blueprint("todo", __name__)

@todo_module.route('/', methods=['GET', 'POST'])
def todo():
    if request.method == 'GET':
        #todo_info = {}
        #return render_template('./template.html', user=todo_info) # userを変数としてテンプレートに渡す
        results = {}
        session = sessionmaker(bind=engine)()
        for result in session.query(ToDo):
            results[result.task] = result.status
        return render_template('template.html', user=results) # userを変数としてテンプレートに渡す
    elif request.method == 'POST':
        if 'todo_insert' in request.form:
            print('todo_insert')
            insert_task = ToDo()
            session = sessionmaker(bind=engine)()
            # データが存在していたら何もしない
            if session.query(ToDo).filter(ToDo.task == request.form['todo_insert']).count() == 0:
                insert_task.task = request.form['todo_insert']
                insert_task.status = '未実施'  # 新規作成なので未実施固定
                # idは、現在存在する最も大きい値+1
                #count = session.query(ToDo).order_by(ToDo.id.desc()).count()
                #if count == 0:
                #    insert_task.id = 1
                #else:
                #    insert_task.id = count + 1
                session.add(instance=insert_task)
                session.commit()
            ## todo_infoには、空情報を送る
            #todo_info = {}
            #return render_template('template.html', user=todo_info) # userを変数としてテンプレートに渡す
            results = {}
            for result in session.query(ToDo):
                results[result.task] = result.status
            return render_template('template.html', user=results) # userを変数としてテンプレートに渡す
        elif 'change_status_task' in request.form:
            print(request.form['change_status_task'])
            print(request.form['change_status_status'])
            session = sessionmaker(bind=engine)()
            results = {}
            results_all = {}
            # 対象データが存在しなかったら何もしない
            if session.query(ToDo).filter(ToDo.task == request.form['change_status_task']).count() == 1:
                # ステータスが空なら何もしない
                if request.form['change_status_status'] != '':
                    task = session.query(ToDo).filter(ToDo.task == request.form['change_status_task']).one()
                    task.status = request.form['change_status_status']
                    session.commit()
            for result in session.query(ToDo):
                results_all[result.task] = result.status
            results = results_all.copy()
            return render_template('template.html', user=results, all=results_all) # userを変数としてテンプレートに渡す
        elif 'disp_todo_status' in request.form:
            print('disp_todo_status')
            results = {}
            results_all = {}
            session = sessionmaker(bind=engine)()
            if request.form['disp_todo_status'] == 'prev':
                filter = '未実施'
            elif request.form['disp_todo_status'] == 'do':
                filter = '実施中'
            elif request.form['disp_todo_status'] == 'done':
                filter = '完了'
            else:
                filter = ''
            for result in session.query(ToDo):
                results_all[result.task] = result.status
            if filter != '':
                for result in session.query(ToDo).filter(ToDo.status == filter):
                    results[result.task] = result.status
            else:
                results = results_all.copy()
            return render_template('template.html', user=results, all=results_all) # userを変数としてテンプレートに渡す