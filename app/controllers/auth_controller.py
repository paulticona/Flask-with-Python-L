
from app.models.users_model import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthController:
    def __init__(self):
        self.model = UserModel
        self.schemas = ''
    def signIn(self, data): 
        try:
            # ? logeode usuarios
            # Buscar el usuario username
            if record:= self.model.where(
                    username=data.get('username'),
                    status=True    
            ).first():
                if record.checkPassword(data.get('password')):
                    access_token = create_access_token(
                        identity=record.id
                    )
                    refresh_token = create_refresh_token(
                        identity=record.id
                    )
                    return {
                        'access_token': access_token,
                        'refresh_token': refresh_token   
                    }, 200
                else:
                    raise Exception('password Invalid')

            raise Exception("No se encontro el usuario")
        except Exception as e:
            return {
                'message': 'Orcurrio un error',
                'error': str(e)
            }, 500
    def refreshToken(self, identity):
        try:
            access_token = create_access_token(
                identity=identity
            )
            return {
                'access_token': access_token
            }, 200 
        except Exception as e:
           return {
                'message': 'Orcurrio un error',
                'error': str(e)
            }, 500