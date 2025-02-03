from fastapi import FastAPI, HTTPException
import mysql.connector
import redis

app = FastAPI()

# 連接 MySQL
mysql_conn = mysql.connector.connect(
    host="54.150.84.198",  # DB 伺服器 IP
    user="interview",       # MySQL 帳號
    password="nfaafrCya2zTwnHn",  # MySQL 密碼
    database="interview_db"  #幫我確認一下他實際ＭＹＳＱＬ名稱是啥
)
mysql_cursor = mysql_conn.cursor(dictionary=True)

# 連接 Redis
redis_client = redis.Redis(
    host="54.150.84.198",  # Redis 伺服器 IP
    port=6379,
    password="fYNmRdZVkuX6",  # Redis 密碼
    decode_responses=True
)

@app.get("/users/{id}")
def get_user(id: int):
    try:
        # 查詢 MySQL
        mysql_cursor.execute("SELECT username, email FROM users WHERE id = %s", (id,))
        user = mysql_cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 查詢 Redis
        redis_value = redis_client.get(user["username"])
        if redis_value is None:
            redis_value = "Not found in Redis"

        return {
            "username": user["username"],
            "email": user["email"],
            "redis_value": redis_value
        }
    
    except Exception as e:
        return {"error": str(e)}

