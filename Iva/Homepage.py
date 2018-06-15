from flask import g, Flask, session, redirect, request, render_template
import sqlite3
import hashlib
import json

DATABASE = './db.sqlite'
app = Flask(__name__)
app.secret_key = 'any random string'


def get_db():
	"""Connect to the application's configured database. The connection
	is unique for each request and will be reused if this is called
	again.
	"""
	if 'db' not in g:
		g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
		g.db.row_factory = sqlite3.Row
	return g.db


def is_logged():
	return session.get


def is_admin():
	return session.get('is_logged_admin') == True


def re_init_nav(is_logged_in, is_logged_admin):
	global nav
	nav = """
<nav class="navbar navbar-inverse">
	<div class="container-fluid">
		<div class="navbar-header">
			<a class="navbar-brand" href="#">HealthyLifestyle</a>
		</div>
		<ul class="nav navbar-nav">
			<li class=""><a href="/">Начало</a></li>
					"""
	if is_logged_admin:
		nav += """
			<li class=""><a href="/articleNew">Добави новина</a></li>
		"""
	nav += """
			<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#"> Здраве <span class="caret"></span></a>
				<ul class="dropdown-menu">
					<li><a href="sports">Спорт</a></li>
					<li><a href="food">Здравословно хранене</a></li>
				</ul>
			</li>
			<li><a href="us">За нас</a></li>
		</ul>
	"""

	nav += """
		<ul class="nav navbar-nav navbar-right">
		"""

	if is_logged_in:
		nav += """
			 <li><a href="logout"><span class="glyphicon glyphicon-log-out"></span> Logout </a></li>
		"""
	else:
		nav += """
			<li><a href="signUp"><span class="glyphicon glyphicon-user"></span> Sign Up </a></li>
			<li><a href="login"><span class="glyphicon glyphicon-log-in"></span> Login </a></li>
		"""

	nav += """
		</ul>
	</div>
</nav>
"""


head = """
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
"""
nav = ""
re_init_nav(False, False)


# def debug():
# 	data = request.data or request.form
# 	print('*' * 40)
# 	print('request')
# 	print(data)
# 	print('session')
# 	print(session)
# 	print('*' * 40)
#
#
# @app.route("/debug", methods=['GET'])
# def debug_page():
# 	debug()
# 	re_init_nav(is_logged())
#
# 	db = get_db()
# 	cursor = db.cursor()
# 	post = cursor.execute("SELECT COUNT(*) FROM post",).fetchone()
# 	user = cursor.execute("SELECT COUNT(*) FROM user",).fetchone()
# 	cursor.connection.close()
# 	return """
# <a href="/">/</a>
# <br/>
# <a href="/articlesList">articlesList</a>
# <br/>
# <a href="/login">login</a>
# <br/>
# <a href="/signUp">signUp</a>
# <br/>
# <a href="/logout">logout</a>
# <br/>
# USER ROWS: """ + str(user[0]) + """
# <br/>
# ARTICLES: """ + str(post[0]) + """
# <br/>
# USER ID: """ + str(session["id"])


# @app.route("/", methods=['GET'])
# def homepage():
# 	return """
# <html>
# 	<head>
# 		<title>Health</title>
# 		""" + head + """
# 	</head>
# 	<body>
# 		""" + nav + """
# 		<h3 class="container">Начало</h3>
# 		<div class="text-center">
# 			<img src="https://static1.squarespace.com/static/551f9a6ee4b09eb81bf1d06b/t/565b72aee4b04e8771106cf0/1448833718904/">
# 		</div>
#
# 		<div class="container">
# 			<h4><small>RECENT POSTS</small></h4>
# 			<hr>
# 			<h2><a href="article1">Здравословен начин на живот с промяна на хранителните навици</a></h2>
# 			<p>
# 				Може би решението е било дълго обмисляно и променяно многократно,
# 				а може и тази статия да ви накара да погледнете с нови очи на здравето си.
# 				Смисълът на всичко, което правим, е да ви накараме да се чувствате по-добре и да бъдете здрави.
# 				Единственото, което се иска от вас, е воля за здравословен начин на живот.
# 				Ако искате да вдъхновите и другите членове на семейството за здравословен начин на живот,
# 				споделете им за препоръките, които ви допадат. Те ще ви последват когато забележат вашата решителност.
# 				И понеже добрата кондиция не се оформя само в кухнята, прекарвайте повече време сред природата.
# 				Увеличаването на физическата активност е отлично решение и ще донесе само позитиви за вашия здравословен начин
# 				на живот.
# 			</p>
# 			<br /><br />
#
# 			<h4><small>RECENT POSTS</small></h4>
# 			<hr />
# 			<h2><a href="article2">10 тайни за хидратация на тялото</a></h2>
# 			<hr>
# 			<p>
# 				Кожата е най-големият орган от човешкото тяло, съдържащ над 70 % вода. Тази вода й
# 				е необходима не само, за да функционира пълноценно като защитен механизъм на организма,
# 				но и за да изглежда добре.
# 				Под въздействие на множество фактори обаче тялото ежедневно губи определени количества
# 				от естествените си водни запаси. И ако не бъдат възстановени, тези загуби се отразяват не
# 				само на здравето, но и на състоянието на кожата.
# 				Следващите 10 тайни за хидратация на тялото ще ви помогнат да поддържате хидробаланса на организма
# 				в норма – както вътрешно, така й външно.
# 			</p>
# 			<hr>
# 		</div>
# 	</body>
# </html>
# """


@app.route("/articleInsert", methods=['POST'])
def article_insert():
	if not is_logged():
		return "not_logged"
	if not is_admin():
		return "not_admin"

	title = request.form['title']
	if title is None:
		return "empty_title"

	text = request.form['text']
	if text is None:
		return "empty_text"

	db = get_db()
	cursor = db.cursor()
	cursor.execute(
		'INSERT INTO post (author_id, title, body) VALUES(?, ?, ?)',
		(session["id"], title, text,)
	)
	db.commit()
	new_article_id = cursor.lastrowid
	cursor.connection.close()
	return "OK:" + str(new_article_id)


@app.route("/articleNew", methods=['GET'])
def article_create():
	if not is_logged():
		return redirect("/", code=401)
	if not is_admin():
		return redirect("/", code=403)
	return """
<html>
	<head>
		<title>Добави Статия</title>
		""" + head + """
		<script type="text/javascript">
			$(document).ready(function() {
				$("#newArticle").submit(function(e) {
					e.preventDefault();
					
					$.ajax({
						url: "/articleInsert",
						type: "POST",
						data: $("#newArticle").serialize(),
						success: function(result) {
							if(result.substr(0, 3) == "OK:")
								window.location.href = "/article/" + result.substr(3);
							else {
								console.log(result);
								alert(result);
							}
						},
						error: function(result) {
							console.log(result);
							alert(result);
						}
					});
				});
			});
		</script>
	</head>
	<body>
		""" + nav + """
		<div class="container">
			<h3>Добави статия</h3>
			<form id="newArticle">
				<div class="form-group">
					<label for="Title">Заглавие</label>
					<input type="text" class="form-control" id="Title" name="title" placeholder="Заглавие" required>
				</div>
				<div class="form-group">
					<label for="text">Текст</label>
					<textarea class="form-control" id="text" name="text" rows="3" required></textarea>
				</div>
				<button type="submit" class="btn btn-primary">Добави</button>
			</form>
		</div>
	</body>
</html>
"""


@app.route("/article/<article_id>", methods=['GET'])
def article(article_id):
	if article_id == 0:
		return redirect("/", code=404)

	db = get_db()
	cursor = db.cursor()
	article = cursor.execute("""
					SELECT p.title, p.body, strftime('%d-%m-%Y %H:%M:%S', created) AS date, u.username 
					FROM post AS p, user AS u WHERE p.id=? AND p.author_id = u.id
					""", (article_id,)).fetchone()
	cursor.connection.close()

	return """
<html>
	<head>
		<title>Добави Статия</title>
		""" + head + """
		<script type="text/javascript">
			$(document).ready(function() {
				$("#newArticle").submit(function(e) {
					e.preventDefault();
					
					$.ajax({
						url: "/articleInsert",
						type: "POST",
						data: $("#newArticle").serialize(),
						success: function(result) {
							if(result.substr(0, 3) == "OK:")
								window.location.href = "/article/" + result.substr(3);
							else {
								console.log(result);
								alert(result);
							}
						},
						error: function(result) {
							console.log(result);
							alert(result);
						}
					});
				});
			});
		</script>
	</head>
	<body>
		""" + nav + """
		<div class="container">
			<h3>""" + article["title"] + """</h3>
			<p>""" + article["body"] + """</p>
			<div>
				<span>Създадена от """ + article["username"] + """ </span>
				<span>Създадена на """ + article["date"] + """ </span>
			</div>
		</div>
	</body>
</html>
"""


@app.route("/articlesInRange", methods=['GET'])
def articles_in_range():
	start = 0
	if request.args.get("start") is not None:
		start = int(request.args.get("start"))

	limit = 50
	if request.args.get("limit") is not None:
		limit = int(request.args.get("limit"))

	db = get_db()
	cursor = db.cursor()
	rows = cursor.execute("""
						SELECT p.id, p.title, p.body, strftime('%d-%m-%Y %H:%M:%S', p.created) AS date, u.username 
						FROM post AS p, user AS u WHERE p.author_id = u.id ORDER BY p.id DESC LIMIT ? OFFSET ?
					""", (limit, start,)).fetchall()
	cursor.connection.close()

	return "OK:" + json.dumps([dict(ix) for ix in rows])


@app.route("/", methods=['GET'])
def home():
	return """
<html>
	<head>
		<title>Health</title>
		""" + head + """
		<script src="https://unpkg.com/infinite-scroll@3/dist/infinite-scroll.pkgd.min.js"></script>
		<script type="text/javascript">
			$(document).ready(function() {
				let start = 0;
				const limit = 50;
				var container = $('#container').infiniteScroll({
					path: function() {
						return '/articlesInRange?start=' + start + "&limit=" + limit;
					},
					responseType: 'text',
					status: '.scroller-status',
					history: false,
					scrollThreshold: true,
					debug: true
				});
				container.on('load.infiniteScroll', function(event, data) {
					if(data.substr(0, 3) == "OK:") {
						data = JSON.parse(data.substr(3));
						if(data.length == 0) {
							// no more results
							container.attr("infinite-scroll-disabled", true);
							return;
						}
						start += data.length;
						let result = "";
						data.forEach(function(element) {
							result += '<div class="panel panel-default">';
							result += '<div class="panel-heading">';
							result += '<h3 class="panel-title">' + element.title + '</h3>';
							result += '</div>';
							result += '<div class="panel-body">' + element.body.substr(0, 500) + '...';
							result += '<div><a class="btn btn-info" href="/article/' + element.id + '">Прочети повече</a></div>';
							result += '</div></div>';
						});
						container.infiniteScroll('appendItems', $(result));
					}
				});
				container.infiniteScroll('loadNextPage');
				window.container = container;
			});
		</script>
	</head>
	<body>
		""" + nav + """
		<div class="text-center">
			<img src="https://static1.squarespace.com/static/551f9a6ee4b09eb81bf1d06b/t/565b72aee4b04e8771106cf0/1448833718904/">
		</div>
		<div id="container" class="container">
			<hr/>
			<div class="scroller-status">
				<div class="infinite-scroll-request loader-ellips">
					...
				</div>
				<p class="infinite-scroll-last">End of content</p>
				<p class="infinite-scroll-error">No more pages to load</p>
			</div>
		</div>
	</body>
</html>
"""


@app.route("/checkSignUp", methods=['POST'])
def check_sign_up():
	if is_logged():
		return "logged"

	username = request.form['username']
	if username is None:
		return "empty_username"

	password = request.form['password']
	if password is None:
		return "empty_password"

	re_password = request.form['re-password']
	if re_password is None:
		return "empty_re-password"

	fname = request.form['fname']
	if fname is None:
		return "empty_fname"

	lname = request.form['lname']
	if lname is None:
		return "empty_lname"

	if password != re_password:
		return "password"
	db = get_db()
	cursor = db.cursor()
	check_username = cursor.execute("SELECT COUNT(*) FROM user WHERE username = ?", (username,)).fetchone()
	if check_username[0] != 0:
		return "username"
	cursor.execute(
		'INSERT INTO user (f_name, l_name, username, password) VALUES(?, ?, ?, ?)',
		(fname, lname, username, hashlib.sha512(password.encode('utf-8')).hexdigest(),)
	)
	db.commit()
	session["id"] = cursor.lastrowid
	session["username"] = username
	session["fname"] = fname
	session["lname"] = lname
	session["logged_in"] = True
	session["is_logged_admin"] = False
	re_init_nav(True, False)
	cursor.connection.close()

	return render_template('auth/register.html')


@app.route("/signUp", methods=['GET'])
def sign_up():
	if is_logged():
		return redirect("/", code=410)
	return """
<html>
	<head>
		<title>Регистрация</title>
		""" + head + """
		<script type="text/javascript">
			$(document).ready(function() {
				$("#signUpPanel").submit(function(e) {
					e.preventDefault();

					$.ajax({
						url: "/checkSignUp",
						type: "POST",
						data: $("#signUpPanel").serialize(),
						success: function(data) {
							if(data == "OK") {
								window.location.href = "/";
							} else {
								console.log(data);
								alert("Error");
							}
						}
					});
				});
			});
		</script>
		<style rel="stylesheet">
			#signUpPanel {
				width: 300px;
				position: absolute;
				top: 50%;
				left: 50%;
				transform: translate(-50%, -50%);
				background: #fff;
				border-radius: 2px;
				box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
				border: 1px solid #ccc;
			}

			#signUpPanel > div {
				padding: 10px 20px;
			}

			#signUpPanel input {
				width: 100%;
			}

			#signUpPanel > div:last-child {
				text-align: right;
			}
		</style>
	</head>
	<body>
		<form id="signUpPanel">
			<div>
				<h3>Sign Up</h3>
			</div>
			<div class="form-group">
				<label for="username">Потребителско име</label>
				<input type="text" name="username" class="form-control" id="username" placeholder="username" required>
			</div>
			<div class="form-group">
				<label for="password">Парола</label>
				<input type="password" name="password" class="form-control" id="password"
					placeholder="password" required>
			</div>
			<div class="form-group">
				<label for="re-password">Повтори паролата</label>
				<input type="password" name="re-password" class="form-control" id="re-password"
					placeholder="re-password" required>
			</div>
			<div class="form-group">
				<label for="fname">Име</label>
				<input type="text" name="fname" class="form-control" id="fname" placeholder="First name" required>
			</div>
			<div class="form-group">
				<label for="lname">Фамилия</label>
				<input type="text" name="lname" class="form-control" id="lname" placeholder="Last name" required>
			</div>
			<div>
				<button type="submit" class="btn btn-primary mb-2">Регистрирай ме</button>
			</div>
		</form>
	</body>
</html>
"""


@app.route("/checkLogin", methods=['POST'])
def check_login():
	username = request.form['username']
	password = request.form['password']
	db = get_db()
	user = db.execute(
		'SELECT * FROM user WHERE username = ? AND	password = ?',
		(username, hashlib.sha512(password.encode('utf-8')).hexdigest(),)
	).fetchone()

	db.close()

	if user is not None and len(user) != 0:
		session["id"] = user[0]
		session["username"] = username
		session["fname"] = user[1]
		session["lname"] = user[2]
		session["logged_in"] = True
		session["is_logged_admin"] = (user[5] == 1)
		re_init_nav(True, session["is_logged_admin"])
		return "OK"

	return "Wrong credentials"


@app.route("/login", methods=['GET'])
def login():
	return """
<html>
	<head>
		<title>Вход</title>
		""" + head + """
		<script type="text/javascript">
			$(document).ready(function() {
				$("#loginPanel").submit(function(e) {
					e.preventDefault();

					$.ajax({
						url: "/checkLogin",
						type: "POST",
						data: $("#loginPanel").serialize(),
						success: function(data) {
							if(data == "OK") {
								window.location.href = "/";
							} else {
								alert("Wrong credentials");
							}
						}
					});
				});
			});
		</script>
		<style rel="stylesheet">
			#loginPanel {
				width: 300px;
				position: absolute;
				top: 50%;
				left: 50%;
				transform: translate(-50%, -50%);
				background: #fff;
				border-radius: 2px;
				box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
				border: 1px solid #ccc;
			}

			#loginPanel > div {
				padding: 10px 20px;
			}

			#loginPanel input {
				width: 100%;
			}

			#loginPanel > div:last-child {
				text-align: right;
			}
		</style>
	</head>
	<body>
		<form id="loginPanel">
			<div>
				<h3>Login</h3>
			</div>
			<div>
				<input name="username" type="text" placeholder="Username" required />
			</div>
			<div>
				<input name="password" type="password" placeholder="password" required />
			</div>
			<div>
				<button type="submit">Вход</button>
			</div>
		</form>
	</body>
</html>
"""


@app.route("/logout", methods=['GET'])
def logout():
	session["logged_in"] = False
	re_init_nav(False)
	return redirect("/", 200)


@app.route("/us", methods=['GET'])
def us():
	return """
<html>
	<head>
		<title>За нас</title>
		""" + head + """
	</head>
	<body>
		""" + nav + """

		<div class="container">
			<h2>За нас</h2>
			Ние сме организация, която желае да предостави полезна информация за здравословния начин на живот на всички 
			читатели. Нашата цел е да предложим на хората различни статии, чрез който те да могат да получат подробна 
			информация по различни теми, който ги вълнуват свързани със здравословния начин на живот. Ние сме екип от 
			професионалисти, в своята област, който желаят да предоставят информация, която да е полезна и достъпна за 
			всеки един потребител на сайта. Всеки от нас е с подходящо образование в областта, за която отговаря 
			например имаме диетолози отговарящи за статиите за здравословното хранене, фитнес инструктори за статиите 
			за спорт и т.н.. Нашето желание е информацията, която споделяме да достигне до по-голяма алдитория от хора, 
			за да можем да предадем максимално много от нашите знания на хора, който имат интерес към тях. Надяваме се 
			да успеем да помогнем на хората да започнат да водят по-здравословен начин на живот, като заменят 
			нездравословното хранене със здравословно, да успеем да ги мотивираме да спортуват повече и да оставят 
			застоялия начин на живот, който е ежедневие за повечето хора.
		</div>
	</body>
</html>
"""


@app.route("/sports")
def sports():
	return """
<html>
	<head>
		<title>За нас</title>
		""" + head + """
	</head>
	<body>
		""" + nav + """

		<div class="container">
		</div>
	</body>
</html>
"""


if __name__ == "__main__":
	app.secret_key = 'V$H96A4K^8KsJxpB6LWZ?^kxRssMNyj#q?SfLxeB-wGRr?$WnfJv542zy!HG&kg6'
	# app.debug = True
	app.run()
	re_init_nav(is_logged(), is_admin())