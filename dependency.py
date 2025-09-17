from fastapi import HTTPException, status
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, http
from uuid import UUID

from client import GoogleClient
from exception import TokenExpiredException, InvalidTokenException
from repository import TaskRepository, TaskCache, UserRepository
from cache import get_redis_connection
from service import TaskService, UserService, AuthService
from settings import Settings


def get_tasks_repository() -> TaskRepository:
    """
    Retrieves an instance of the task repository.
    Returns:
        TaskRepository: An instance of the task repository.
    """
    return TaskRepository()


def get_cache_tasks_repository() -> TaskCache:
    """
    Retrieves an instance of the task cache using a Redis connection.
    Returns:
        TaskCache: An instance of the task cache.
    """
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_task_service(
    task_repository: TaskRepository = Depends(get_tasks_repository),
    task_cache: TaskCache = Depends(get_cache_tasks_repository),
) -> TaskService:
    """
    Retrieves an instance of the task service.
    Args:
        task_repository (TaskRepository, optional): The task repository. Defaults to the result of
            the get_tasks_repository function.
        task_cache (TaskCache, optional): The task cache. Defaults to the result of
            the get_cache_tasks_repository function.
    Returns:
        TaskService: An instance of the task service.
    """
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache,
    )


def get_user_repository() -> UserRepository:
    """
    Retrieves an instance of the user repository.
    Returns:
        UserRepository: An instance of the user repository.
    """
    return UserRepository()


def get_google_client() -> GoogleClient:
    """
    Retrieves an instance of the Google client configured with application settings.

    Returns:
        GoogleClient: An instance of Google client for OAuth authentication and
        user information retrieval from Google APIs.
    """
    return GoogleClient(settings=Settings())


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
) -> AuthService:
    """
    Retrieves an instance of the authentication service.
    Args:
        user_repository (User Repository, optional): The user repository. Defaults to the result of
            the get_user_repository function.
        google_client (GoogleClient, optional):
    Returns:
        AuthService: An instance of the authentication service.

    """
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
    )


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    """
    Retrieves an instance of the user service.
    Args:
        user_repository (User Repository, optional): The user repository. Defaults to the result of
            the get_user_repository function.
        auth_service (AuthService, optional): The authentication service. Defaults to the result of
            the get_auth_service function.
    Returns:
        UserService: An instance of the user service.
    """
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = HTTPBearer(auto_error=False)


def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> UUID:
    """
    Extracts the user ID from the access token.
    Args:
        auth_service (AuthService, optional): The authentication service. Defaults to the result of
            the get_auth_service function.
        token (http.HTTPAuthorizationCredentials, optional): The access token obtained from the
            authorization header.
    Raises:
        HTTPException: If the token is missing or invalid, an exception is raised with a 401 status code.
    Returns:
        UUID: The user ID extracted from the access token.
    """
    if not token or not token.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token."
        )
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except (TokenExpiredException, InvalidTokenException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
        )
    return user_id
