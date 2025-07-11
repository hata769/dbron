# 今日の活動件数を検索する関数（ビュー：user_health_activity_today）
import pandas as pd
from MyDatabase import my_open, my_query, my_close

def df_user_health_activity_today(user_id):
    import pandas as pd
    from MyDatabase import my_open, my_query, my_close

    dsn = {
        'host': '172.30.0.10',
        'port': '3306',
        'user': 'root',
        'password': '1234',
        'database': 'dbron'
    }

    dbcon, cur = my_open(**dsn)

    # userIDを絞り込んで取得
    sqlstring = f"""
        SELECT * FROM user_health_activity_today
        WHERE userID = {user_id};
    """
    my_query(sqlstring, cur)
    df = pd.DataFrame(cur.fetchall(), columns=['userID', 'check_health_count', 'activity_count'])

    my_close(dbcon, cur)
    return df