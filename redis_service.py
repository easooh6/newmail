import redis
from config import *
from fastapi.responses import JSONResponse

r = redis.Redis(host= REDIS_HOST, port= REDIS_PORT, db = REDIS_DB)


class Code():
    def save_code(self,email,code):
        r.setex(email,300,code)

    def get_code(self,email):
        return r.get(email)
    
    def delete_code(self,email):
        r.delete(email)

    def check_rate_limit(self,email):
        key = f"user:{email}"
        request = r.get(key)
        if not request:
            r.setex(key,300,1)
            return True
        elif int(request) < 3:
            r.setex(key,300,int(request)+1)
            return True
        elif int(request) >= 3:
            return False



