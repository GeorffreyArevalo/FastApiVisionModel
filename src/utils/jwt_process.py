from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Header, HTTPException, status
from jwt.exceptions import InvalidTokenError


class JwtUtil:
    EXPIRE_HOURS=4
    SECRET_KEY='b13bd256e19bfee825cfbe70fe09106904337d43194b797b2a5ad6f864d55b2f'
    ALGORITHM='HS256'
    
    @staticmethod
    def generate_access_token( data: dict ):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta( hours=JwtUtil.EXPIRE_HOURS )
        to_encode.update( {"exp": expire} )
        jwt_user = jwt.encode(to_encode, JwtUtil.SECRET_KEY, algorithm=JwtUtil.ALGORITHM)
        return jwt_user
    
    @staticmethod
    async def get_user_authenticated(bearer_token: str = Header( alias='Authorization', default=None ) ):
        
        if bearer_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Acceso denegado - No Token')
        
        if not bearer_token.startswith('Bearer '):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Acceso denegado - No Starts With Bearer')
        
        try:
            token = bearer_token.split(' ')[1]
            payload = jwt.decode( token, JwtUtil.SECRET_KEY, algorithms=[JwtUtil.ALGORITHM] )
            username: str = payload.get("username")
            
        except InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Acceso denegado - Invalid Token') from e
            
        return username
            
        
    
    
    


