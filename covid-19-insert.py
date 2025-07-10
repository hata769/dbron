from MyDatabase import my_open , my_query , my_close
import pandas as pd
#パスワードのハッシュ化に用いる
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

#Data Source Nameのパラメータを辞書型変数で定義しオープン
dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'dbron' #オープンするデータベース名
}
dbcon,cur = my_open( **dsn )

# my_query(sqlstring, cur)
# recset = pd.DataFrame( cur.fetchall() )

#3つのファイル名をlist変数として保存
filename = ["./school.csv","./department.csv","./user.csv","./user_from.csv","./user_pass.csv"]
#デバック用
# filename = ["./user.csv"]

#現在の日時を取得
import datetime
dt_now = datetime.datetime.now()

#3つのファイルを処理するための繰り返し処理 fnにファイル名が入る
for fn in filename:

    #ファイルオープン 先頭行をheaderとして
    df = pd.read_csv( fn ,header=0)

    #recsetは，DataFrameのため，indexとrowdataをペアで取得する
    for ind,rowdata in df.iterrows():

        #レコードを挿入するSQL文をそれぞれ定義する
        if fn =="./school.csv" :
            sqlstring = f"""
                INSERT INTO school
                (school_name, post_num, prefecture, city, area, lastupdate)
                VALUES
                ('{rowdata.school_name}', '{rowdata.post_num}', '{rowdata.prefecture}', '{rowdata.city}', '{rowdata.area}', '{dt_now}');
            """
        elif fn == "./department.csv" :
            sqlstring = f"""
                INSERT INTO department
                (schoolID, department_name, phone, lastupdate)
                VALUES
                ({rowdata.schoolID}, '{rowdata.department_name}', '{rowdata.phone}', '{dt_now}');
            """
        elif fn == "./user.csv" :
            #userテーブルの場合
            sqlstring = f"""
                INSERT INTO user
                (schoolID,affiliation,user_code,l_name,f_name,l_name_kana,f_name_kana,gender,birthday,lastupdate)
                values
                ({rowdata.schoolID},'{rowdata.affiliation}','{rowdata.user_code}','{rowdata.l_name}','{rowdata.f_name}','{rowdata.l_name_kana}','{rowdata.f_name_kana}',{rowdata.gender},'{rowdata.birthday}','{dt_now}')
                ;
            """
        elif fn == "./user_from.csv" :
            #user_fromテーブルの場合
            sqlstring = f"""
                INSERT INTO user_from
                (userID,return_home,post_num,prefecture,city,area,phone,lastupdate)
                values
                ({rowdata.userID},{rowdata.return_home},'{rowdata.post_num}','{rowdata.prefecture}','{rowdata.city}','{rowdata.area}','{rowdata.phone}','{dt_now}')
                ;
            """
        else:
            #user_passテーブルの場合
            #パスワードをハッシュ化
            hashed_password = bcrypt.generate_password_hash(str(rowdata.password)).decode('utf-8')

            sqlstring = f"""
                INSERT INTO user_pass
                (userID,permission,user_name,password,lastupdate)
                values
                ({rowdata.userID},{rowdata.permission},'{rowdata.user_name}','{hashed_password}','{dt_now}')
                ;
            """
        #クエリー実行
        my_query(sqlstring, cur)

    #INSERT文を実行するループが終了し，結果をフィードバック
    print( f"{fn}を{len( df )}レコードを新規挿入しました")

    #テーブルに書き込み
    dbcon.commit()  

#カーソルとDBコンソールのクローズ
my_close(dbcon, cur)
