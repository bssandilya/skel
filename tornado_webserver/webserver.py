from tornado import httpserver, web, ioloop
import tornado.options
import simplejson

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
        # data = simplejson.loads(self.request.body)
        self.render('someother.html')

    def get(self):
        # param1 = self.get_argument('param1')
        self.render("index.html")

class Application(web.Application):

    def __init__(self):
        handlers = [(r'/', IndexHandler),
                    (r'/something', SomeHandler),
                    (r'/(.*)', ErrorHandler)]

        settings = {'static_path': 'static',
                    'template_path': 'templates',
                    'debug': True}
        web.Application.__init__(self, handlers, **settings)

def main():
    app = Application()
    tornado.options.parse_command_line()
    webserver = httpserver.HTTPServer(app).listen(8888)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
