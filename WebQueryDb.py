from flask import Flask, redirect, url_for, request, render_template,g
from RealtimeQuery import query_realtime, documentation, log, log_append
import sqlite3
import datetime
import os

app = Flask(__name__)

DATABASE = './database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def query_from_db(city):
	'''通过城市名称，从数据库查询天气'''
	r = query_db('select * from qw where city_name = ?',
	                [city], one=True)
	if r is None:
	    print('No such city')
	else:
	    print(r)
	return r

def insert_into_db(city, weather, temperature):
	'''将查询的结果插入到数据库中'''
	c = get_db().cursor()
	qttime = datetime.date.today()
	city_name = city
	c.execute("INSERT INTO qw VALUES (?,?,?,?)",(qttime,city_name,weather,temperature))
	get_db().commit()

@app.route('/query/<city>')
def query(city):
	'''查询实时天气。参数：城市；返回值：天气；在html网页显示，" "替换为<br>'''
	r = query_realtime(city)
	insert_into_db(city, r[city][0], r[city][1])
	s = query_from_db(city)
	return render_template('index.html', result = s)

@app.route('/', methods = ['POST', 'GET'])
def weather():
	'''从文本框输入城市名，作为参数提交到query(),取回天气值'''
	if request.method == 'POST':
		user_input = request.form['InputCity']	
		return redirect(url_for('query',city = user_input))
#		return render_template('index.html', result = dict)
	else:
		user_input = request.args.get('InputCity')
		return redirect(url_for('query',city = user_input))
 
@app.route('/update', methods = ['POST'])
def update():
	'''向数据库插入数据'''
	if request.method == 'POST':
		c = get_db().cursor()
		user_input = request.form['Input']
		d = user_input.split(" ")
		dic = ["晴","雪","雨","阴"]
		q = query_from_db(d[0])
		if q and (d[1] in dic):
			c.execute("UPDATE qw SET weather= ? WHERE city_name = ?" , (str(d[1]),str(d[0])))
			get_db().commit()
			s = q
		else:
			s = ["请输入正确的天气情况：如晴，雪，雨，阴"]
		return render_template('index.html', result = s)

@app.route('/history')
def history():
	'''点击“历史”按钮，返回查询记录，需要将\n替换为<br>才能在网页中正常换行'''
	h = documentation("log.txt").splitlines()
	return render_template('index.html', result = h)

@app.route('/help')
def help():
	'''点击“帮助”按钮，返回帮助文档'''
	h = documentation("README.md").splitlines()
	return render_template('index.html', result = h)

if __name__ == '__main__':
	log()
	port = int(os.environ.get("PORT", 5000))
	with app.app_context():
		app.run(host='0.0.0.0', port=port)