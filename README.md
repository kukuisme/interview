1.登入伺服器：<我習慣直接在key的資料夾使用終端機 這樣就不用給鑰匙的path>
```
ssh -i 他給的那個.pem admin@ec2-54-178-66-208.ap-northeast-1.compute.amazonaws.com
```

2.安裝必要的 Python 依賴：<幫我確認一下伺服器有沒有這些插件>
```

sudo apt-get update && sudo apt-get install uvicorn cron pip -y
pip install fastapi mysql-connector-python redis
```

3.假設你已經編輯好ans.py
手動啟用：
```
cd /home/admin/
uvicorn ans:app --host 0.0.0.0 --port 8888 --reload
```

4.測試 API
在自己終端機：
```
curl http://your_server_ip:8888/users/1
```

5.如果資料庫中有 id=1 的用戶，看到下列就截圖收工：
{
    "username": "user1",
    "email": "user1@example.com",
    "redis_value": "redis_value1"
}


