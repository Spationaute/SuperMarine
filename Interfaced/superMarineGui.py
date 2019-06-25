import tornado.ioloop
import tornado.web
import Toolkit as tk
import superMarine as sm

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
        opt = dict()
        opt["r"] = 10
        opt["theta"] = 10
        opt["z"] = 10
        opt["nsec"] = 4
        opt["sqratio"] = 0.62
        opt["lvlrot"] = "[0, 0, 0, 0]"
        opt["hlay"] = "[1, 1, 1, 1]"
        opt["shaft"] = "[0, 0, 0, 0]"
        opt["rquad"] = "[0.1,0.2,0.3]"
        opt["impellercut"] = "[0]"
        self.write(tk.genSupM(opt))

def application():
    app = [
        (r"/", Form),
        (r"/gen",Generator),
        (r"/static/(.*)", tornado.web.StaticFileHandler,{"path":"assets"})
    ]
    return tornado.web.Application(app)

if __name__=="__main__":
    formFile = open("interface.html","r")
    formTemplate  = formFile.read()
    app = application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
