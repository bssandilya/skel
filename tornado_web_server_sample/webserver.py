from tornado import httpserver, web, ioloop
import tornado.options
import time
import uuid

class ErrorHandler(web.RequestHandler):

    def write_error(self, status_code, **kwargs):
        self.render("404.html")


class SomeHandler(web.RequestHandler):

    def get(self):
        self.render("someother.html")


class IndexHandler(web.RequestHandler):

    def write_error(self, status_code, **kwargs):
        self.write("Gosh darnit! You caused a %d error" % status_code)

    def post(self):
        # username = self.get_argument('username')
        # print username, self.request.remote_ip
        # save username along with cookie self.get_secure_cookie("ADCAM")
        self.render('someother.html')

    def get(self):
        cookieName = "ADCAMP"
        # save user info from self.request.remote_ip
        # print self.request.remote_ip
        if not self.get_secure_cookie(cookieName):
            self.set_secure_cookie(cookieName, str(uuid.uuid4()))
            self.render("index.html")
        else:
            self.render("index.html")

class Application(web.Application):

    def __init__(self):
        handlers = [(r'/', IndexHandler),
                    (r'/something', SomeHandler),
                    (r'/(.*)', ErrorHandler)]

        settings = {'static_path': 'static',
                    'template_path': 'templates',
                    "cookie_secret":
                    "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                    'debug': True}
        web.Application.__init__(self, handlers, **settings)


def main():
    app = Application()
    tornado.options.parse_command_line()
    webserver = httpserver.HTTPServer(app).listen(8888)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
