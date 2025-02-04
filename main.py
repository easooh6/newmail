from typing import Union
from config import *
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, ValidationError, PositiveInt, validator
from redis_service import Code
from email_service import Emessage
import random
from fastapi.responses import JSONResponse


app = FastAPI()

class User(BaseModel):
    email : EmailStr

class Verification(BaseModel):
    email: EmailStr
    code : PositiveInt



@app.post('/send-code')
def send_code(request: User):
    email = request.email
    code = random.randint(1000,9999)
    code_hanler = Code()
    limit = code_hanler.check_rate_limit(email)
    if limit == True:
        pass
    elif limit == False:
        return JSONResponse({"message":"Too much attempts"}, status_code=429)
    code_hanler.save_code(email,code)
    transfer = Emessage()
    transfer.send_message(EMAIL_HOST_USER, email, str(code))
    return JSONResponse(content={"message":"The code was sent"},status_code = 200)


@app.post('/verify-code')
def verify_code(verify: Verification):
    try:
        email = verify.email
        code = Code()
        current_code = code.get_code(email)
        current_code = int(current_code)
        if current_code == verify.code:
            return JSONResponse(content={"message":"you are verified"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Bad request"},status_code=400)
    except Exception:
        return JSONResponse(content={"message": "Bad request"},status_code=400)
        
