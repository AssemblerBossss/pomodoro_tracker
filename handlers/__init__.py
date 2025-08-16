from handlers.tasks import router as task_router
from handlers.ping import router as ping_router
from handlers.user import router as user_router

routers = [task_router, ping_router, user_router]
