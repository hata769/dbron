# covid19.py 
# FlaskモジュールでDBの操作
import re
from ssl import MemoryBIO
from MyDatabase import my_open , my_query , my_close
import pandas as pd

from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta, date
import mysql.connector

# 関数のインポート
from today_input import df_user_health_activity_today #今日の活動件数を検索する関数（引数：userID）

app = Flask(__name__, static_folder="static")
# セッション情報の暗号化や署名に使う
app.secret_key = 'covid-19-test'# 後々環境変数から読み込むかも
app.permanent_session_lifetime = timedelta(minutes=30)
bcrypt = Bcrypt(app)

# MySQL 接続情報
dsn = {
    'host': '172.30.0.10',
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'database': 'dbron'
}

# ログインページ
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # ユーザー名とパスワードの受け取り
        username = request.form['username']
        password = request.form['password']

        # ユーザー名の照合
        try:
            conn = mysql.connector.connect(**dsn)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_pass WHERE user_name = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            return f"DB接続エラー: {e}"

        if user:
            # パスワードチェック
            if bcrypt.check_password_hash(user['password'], password):
                session.permanent = True
                session['username'] = username
                session['permission'] = user['permission']
                session['userID'] = user['userID']  # ← 追加
                return redirect(url_for('top'))
            else:
                error = "ユーザー名またはパスワードが正しくありません"
        else:
            error = "ユーザー名またはパスワードが正しくありません"

    return render_template("covid-19-login.html", error=error)

# ログアウト
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# トップページ
@app.route("/")
def top():
    # ログインしていなければログインページへ
    if "username" not in session:
        return redirect(url_for('login'))

    # DB接続
    conn = mysql.connector.connect(**dsn)
    cur = conn.cursor()

    today = date.today().strftime("%Y-%m-%d")

    # ユーザーIDを取得
    user_id = session["userID"]

    # 本日の記録件数を取得
    df = df_user_health_activity_today(user_id)

    # 変数を定義し、それぞれの活動件数を格納
    if not df.empty:
        health_count = int(df.iloc[0]["check_health_count"])
        activity_count = int(df.iloc[0]["activity_count"])
    else:
        health_count = 0
        activity_count = 0

    #トップページへ移行
    return render_template("covid-19-top.html",
        username=session["username"],
        permission=session["permission"],
        title="Covid-19管理システムトップ",
        health_count=health_count,
        activity_count=activity_count
    )

# 体調記録
@app.route("/check_health1")
def check_health1():
    # ログインしていなければログインページへ
    if "username" not in session:
        return redirect(url_for("login"))
    
    # 体調観察記入フォームに移行
    return render_template("covid-19-check_health1.html",
        title = "体調観察記録"
    )

# 体調記録を受け取り、check_healthテーブルに保存
@app.route("/check_health2", methods=["POST"])
def check_health2():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        # DB接続
        conn = mysql.connector.connect(**dsn)
        cur = conn.cursor()

        # userID を取得（ログインユーザーから）
        cur.execute("SELECT userID FROM user_pass WHERE user_name = %s", (session["username"],))
        result = cur.fetchone()
        if not result:
            return "ユーザーが見つかりません"
        user_id = result[0]

        # フォームから個別に取得
        input_date = request.form["input_date"]
        am_pm = int(request.form["am_pm"])
        body_temp = float(request.form["body_temp"])
        pain = "pain" in request.form
        washedout_feeling = "washedout_feeling" in request.form
        headache = "headache" in request.form
        sore_throat = "sore_throat" in request.form
        breathless = "breathless" in request.form
        cough = "cough" in request.form
        vomiting = "vomiting" in request.form
        diarrhea = "diarrhea" in request.form
        taste_disorder = "taste_disorder" in request.form
        olfactory_disorder = "olfactory_disorder" in request.form
        dt_now = datetime.now()

        # SQL文（f-stringで構築）
        sqlstring = f"""
            INSERT INTO check_health (
                userID, input_date, am_pm, body_temp,
                pain, washedout_feeling, headache, sore_throat,
                breathless, cough, vomiting, diarrhea,
                taste_disorder, olfactory_disorder, lastupdate
            ) VALUES (
                {user_id}, '{input_date}', {am_pm}, {body_temp},
                {int(pain)}, {int(washedout_feeling)}, {int(headache)}, {int(sore_throat)},
                {int(breathless)}, {int(cough)}, {int(vomiting)}, {int(diarrhea)},
                {int(taste_disorder)}, {int(olfactory_disorder)}, '{dt_now}'
            );
        """

        # 実行
        cur.execute(sqlstring)
        conn.commit()
        cur.close()
        conn.close()

        return render_template("covid-19-check_health2.html", title="体調記録完了")

    except Exception as e:
        return f"エラーが発生しました: {e}"

# 行動記録
@app.route("/activity1")
def activity1():
    # ログインしていなければログインページへ
    if "username" not in session:
        return redirect(url_for("login"))
    
    # 行動記録記入フォームに移行
    return render_template("covid-19-activity1.html",
        title = "行動記録"
    )

# 行動記録受け取り・DB保存
@app.route("/activity2", methods=["POST"])
def activity2():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        conn = mysql.connector.connect(**dsn)
        cur = conn.cursor()

        # ログインユーザーの userID 取得
        cur.execute("SELECT userID FROM user_pass WHERE user_name = %s", (session["username"],))
        result = cur.fetchone()
        if not result:
            return "ユーザーが見つかりません"
        user_id = result[0]

        # フォームデータ取得
        went_date = request.form["went_date"]
        went_time = request.form["went_time"]
        return_time = request.form["return_time"]
        location = request.form["location"]
        move_method = request.form["move_method"]
        departure = request.form["departure"]
        arrival = request.form["arrival"]
        comp_NY = "comp_NY" in request.form
        comp_num = request.form.get("comp_num", "")
        sp_mention = request.form.get("sp_mention", "")
        dt_now = datetime.now()

        # SQL登録（f-string）
        sqlstring = f"""
            INSERT INTO activity (
                userID, went_date, went_time, return_time, location,
                move_method, departure, arrival, comp_NY, comp_num, sp_mention, lastupdate
            ) VALUES (
                {user_id}, '{went_date}', '{went_time}', '{return_time}', '{location}',
                '{move_method}', '{departure}', '{arrival}', {int(comp_NY)}, '{comp_num}', '{sp_mention}', '{dt_now}'
            );
        """
        cur.execute(sqlstring)
        conn.commit()
        cur.close()
        conn.close()

        return render_template("covid-19-activity2.html", title="行動記録完了")

    except Exception as e:
        return f"エラーが発生しました: {e}"

# 履歴
@app.route("/history1")
def history1():
    # ログインしていなければログインページへ
    if "username" not in session:
        return redirect(url_for("login"))
    
    # 履歴表示に移行
    return render_template("covid-19-history_select.html",
        title = "履歴選択"
    )

# 履歴の選択
@app.route("/history_select", methods=["GET", "POST"])
def history_select():
    # ログインしていなければログインページへ
    if "username" not in session:
        return redirect(url_for("login"))

    choice = request.form.get("history_type")
    if choice == "health":
        return redirect(url_for("health_history"))
    elif choice == "activity":
        return redirect(url_for("activity_history"))
    else:
        return "無効な選択です"

# 健康観察記録の参照
@app.route("/history/health")
def health_history():
    # ログインしていなければログインページへ
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        conn = mysql.connector.connect(**dsn)
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT userID FROM user_pass WHERE user_name = %s", (session["username"],))
        user_id = cur.fetchone()["userID"]

        cur.execute("""
            SELECT input_date, am_pm, body_temp, pain, washedout_feeling, headache, sore_throat,
                   breathless, cough, vomiting, diarrhea, taste_disorder, olfactory_disorder
            FROM check_health
            WHERE userID = %s AND delflag = FALSE
            ORDER BY input_date DESC
        """, (user_id,))
        records = cur.fetchall()

        cur.close()
        conn.close()

        return render_template("covid-19-health_history.html", title="体調記録履歴", records=records)

    except Exception as e:
        return f"エラーが発生しました: {e}"

# 行動記録の参照
@app.route("/history/activity")
def activity_history():
    # ログインしていなければログインページへ
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        conn = mysql.connector.connect(**dsn)
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT userID FROM user_pass WHERE user_name = %s", (session["username"],))
        user_id = cur.fetchone()["userID"]

        # SQL文
        cur.execute("""
            SELECT went_date, went_time, return_time, location, move_method, departure,
                   arrival, comp_NY, comp_num, sp_mention
            FROM activity
            WHERE userID = %s AND delflag = FALSE
            ORDER BY went_date DESC, went_time DESC
        """, (user_id,))
        records = cur.fetchall()

        cur.close()
        conn.close()

        return render_template("covid-19-activity_history.html", title="行動記録履歴", records=records)

    except Exception as e:
        return f"エラーが発生しました: {e}"

# 感染報告
@app.route("/report")
def report():
    # ログインしていなければログインページへ
    if "username" not in session:
        return redirect(url_for("login"))
    
    # 感染報告に移行
    return render_template("covid-19-history_select.html",
        title = "履歴選択"
    )

# 管理者用のセッション

# データベース検索
@app.route("/admin/search")
def admin_search():
    if "username" not in session or session.get("permission") != 1:
        return redirect(url_for("login"))
    # 管理者専用の検索ページを表示
    return render_template("admin_search.html", title="データベース検索")

# データベース編集
@app.route("/admin/edit")
def admin_edit():
    if "username" not in session or session.get("permission") != 1:
        return redirect(url_for("login"))
    # 管理者専用の編集ページを表示
    return render_template("admin_edit.html", title="データベース編集")

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)