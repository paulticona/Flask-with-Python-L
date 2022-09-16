from app import api, mail
from flask_restx import Resource
from app.schemas.auth_schema import AuthRequestSchema
from app.controllers.auth_controller import AuthController
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Message

auth_ns = api.namespace(
    name='Autenticacion',
    description='Rutas del modulo de autenticación',
    path='/auth'
)

request_schema = AuthRequestSchema(auth_ns)


@auth_ns.route('/signin')
class Signin(Resource):

    @api.expect(request_schema.signIn(), validate=True)
    def post(self):

        #  * el token creado es para validar el usurario y contraseña
        '''Crear token de autenticación'''
        controller = AuthController()
        return controller.signIn(request.json)


@auth_ns.route('/reset_password')
class ResetPassword(Resource):
    @auth_ns.expect(request_schema.resetPassword(), validate=True)
    def post(self):
        '''Resetear la contraseña de un usuario.'''
        controller = AuthController()
        return controller.resetPassword(request.json)

@auth_ns.route('/token/refresh')
class TokenRefresh(Resource):
    @auth_ns.expect(request_schema.refreshToken())
    @jwt_required(refresh=True)
    def post(self):
        '''Obtener un nuevo access token desde el refresh_token'''
        edentity = get_jwt_identity()
        controller = AuthController()
        return controller.refreshToken(edentity)


api.add_namespace(auth_ns)
