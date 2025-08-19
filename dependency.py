from fastapi import HTTPException, status
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, http
from uuid import UUID
from sqlalchemy.orm import Session
from exception import TokenExpiredException, InvalidTokenException
from repository import TaskRepository, TaskCache, UserRepository
from cache import get_redis_connection
from service import TaskService, UserService, AuthService
from settings import Settings


def get_tasks_repository() -> TaskRepository:
    return TaskRepository()


def get_cache_tasks_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_task_service(
    task_repository: TaskRepository = Depends(get_tasks_repository),
    task_cache: TaskCache = Depends(get_cache_tasks_repository),
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache,
    )


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings())


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = HTTPBearer(auto_error=False)


def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> UUID:
    try:
        if token is None:
            raise InvalidTokenException
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
        )
    except InvalidTokenException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
        )
    return user_id
