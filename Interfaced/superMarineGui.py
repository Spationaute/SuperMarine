import tornado.ioloop
import tornado.web

formTemplate = ""

class Form(tornado.web.RequestHandler):
    """
        Handle request for forms
    """
    def get(self):
        self.write(formTemplate)

class Generator(tornado.web.RequestHandler):
    """
        Handle generating request from forms.
    """
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")

    def get(self):
        arguments = self.get_arguments("")
        self.write_error("{}".format(arguments))

def application():
    app = [
        (r"/", Form),
        (r"/gen/",Generator),
        (r"/static/(.*)", tornado.web.StaticFileHandler,{"path":"assets"})
    ]
    return tornado.web.Application(app)

if __name__=="__main__":
    formFile = open("interface.html","r")
    formTemplate  = formFile.read()

    app = application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
