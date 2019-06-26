import tornado.ioloop
import tornado.web
import json
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

    def prepare(self):
        self.args = {"status":"empty"}
        if self.request.body:
            self.args = json.loads(self.request.body)
            self.args["status"] = "ready"

    def post(self):
        print("Request in: \n{}".format(self.args))
        if self.args["status"] == "empty":
            self.write(self.args)
        elif self.args["type"] == "blockMesh":
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
            self.args["data"] = tk.genSupM(opt)
            print("Answer:\n{}".format(self.args))
            self.write(self.args)
        elif self.args["type"] == "python":
            self.args["data"] = "None"
            print("Answer:\n{}".format(self.args))
            self.write(self.args)


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
