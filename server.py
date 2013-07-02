#!./venv/bin/python
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import sys
sys.path.append("./scripts")
from hashacat import app

http_server = HTTPServer(WSGIContainer(app), xheaders=True)
http_server.listen(5000)
IOLoop.instance().start()
