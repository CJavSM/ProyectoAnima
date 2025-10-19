from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth_schemas import UserRegister, UserLogin, TokenResponse, UserResponse, MessageResponse
from app.services.auth_service import AuthService

class AuthController:
    
    @staticmethod
    def register(user_data: UserRegister, db: Session) -> MessageResponse:
        """Controlador para registrar un nuevo usuario"""
        try:
            user = AuthService.register_user(user_data, db)
            return MessageResponse(
                message="Usuario registrado exitosamente",
                detail=f"Bienvenido {user.username}!"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al registrar usuario: {str(e)}"
            )
    
    @staticmethod
    def login(login_data: UserLogin, db: Session) -> TokenResponse:
        """Controlador para autenticar un usuario"""
        try:
            # Autenticar usuario
            user = AuthService.authenticate_user(
                login_data.username_or_email,
                login_data.password,
                db
            )
            
            # Crear token
            access_token = AuthService.create_user_token(user)
            
            # Preparar respuesta
            user_response = UserResponse(
                id=str(user.id),
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                profile_picture=user.profile_picture,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at
            )
            
            return TokenResponse(
                access_token=access_token,
                user=user_response
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al iniciar sesión: {str(e)}"
            )
    
    @staticmethod
    def get_current_user_info(user_id: str, db: Session) -> UserResponse:
        """Obtiene la información del usuario actual"""
        try:
            user = AuthService.get_user_by_id(user_id, db)
            return UserResponse(
                id=str(user.id),
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                profile_picture=user.profile_picture,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener información del usuario: {str(e)}"
            )