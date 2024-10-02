from src.presentation.routes import AppRoutes
from src.presentation.server import Server

routes = AppRoutes.get_routes()
server = Server(routes=routes)
app = server.start()


