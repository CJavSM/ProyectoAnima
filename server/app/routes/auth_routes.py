from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controllers.auth_controller import AuthController
from app.schemas.auth_schemas import UserRegister, UserLogin, TokenResponse, UserResponse, MessageResponse
from app.middlewares.auth_middleware import get_current_active_user
from app.models.user import User

router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación"]
)

@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea una nueva cuenta de usuario en el sistema"
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo usuario con los siguientes requisitos:
    
    - **email**: Email válido y único
    - **username**: Username único (3-50 caracteres, solo letras, números, guiones)
    - **password**: Mínimo 8 caracteres, debe incluir mayúsculas, minúsculas, números y caracteres especiales
    - **first_name**: Nombre (opcional)
    - **last_name**: Apellido (opcional)
    """
    return AuthController.register(user_data, db)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
    description="Autentica un usuario y devuelve un token JWT"
)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Inicia sesión con username o email:
    
    - **username_or_email**: Username o email del usuario
    - **password**: Contraseña del usuario
    
    Retorna un token JWT y la información del usuario
    """
    return AuthController.login(login_data, db)

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario actual",
    description="Obtiene la información del usuario autenticado"
)
def get_current_user(
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la información del usuario actual autenticado.
    
    Requiere token JWT válido en el header Authorization: Bearer <token>
    """
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        profile_picture=current_user.profile_picture,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )

@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Cerrar sesión",
    description="Cierra la sesión del usuario (cliente debe eliminar el token)"
)
def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    Cierra la sesión del usuario actual.
    
    Nota: Como usamos JWT stateless, el token seguirá siendo válido hasta que expire.
    El cliente debe eliminar el token de su almacenamiento local.
    """
    return MessageResponse(
        message="Sesión cerrada exitosamente",
        detail="Token debe ser eliminado del cliente"
    )