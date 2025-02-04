from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
import redis

app = FastAPI()


MYSQL_CONFIG = {
    "host": "XXX.XXX.XXX.XXX",
    "user": "interview",
    "password": "password",
    "database": "interview"
}


REDIS_HOST = "XXX.XXX.XXX.XXX"
REDIS_PORT = 6379
REDIS_PASSWORD = "password"


def get_mysql_connection():
    """Mysql Connect"""
    try:
        return mysql.connector.connect(**MYSQL_CONFIG)
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail="MySQL WIRING ERROR：" + str(e))


def get_redis_connection():
    """ Redis Connect"""
    try:
        return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail="Redis WIRING ERROR：" + str(e))


@app.get("/users/{user_id}")
def get_user(user_id: int):
    try:

        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()


        if not user:
            return JSONResponse(
                status_code=400,
                content={"error": "USER ID DOES NOT EXIST", "user_id": user_id}
            )

        username = user["username"]
        email = user["email"]


        redis_conn = get_redis_connection()
        redis_value = redis_conn.get(username)

        if not redis_value:
            redis_value = "No value in Redis"


        return JSONResponse(
            status_code=200,
            content={
                "username": username,
                "email": email,
                "redis_value": redis_value
            }
        )

    except mysql.connector.Error as e:
        return JSONResponse(
            status_code=400,
            content={"error": "MySQL 查詢錯誤", "details": str(e)}
        )
    except redis.RedisError as e:
        return JSONResponse(
            status_code=400,
            content={"error": "Redis 連線錯誤", "details": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": "未知錯誤", "details": str(e)}
        )
