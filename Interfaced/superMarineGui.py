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
            self.args = json.loads(self.request.body.decode("UTF-8"))
            self.args["status"] = "ready"

    def post(self):
        print("Request in: \n")
        prettyJSON(self.args)
        if self.args["status"] == "empty":
            self.write(self.args)
        elif self.args["type"] == "blockMesh":
            opt = dict()
            opt["DIVI"] = [self.args["division"][0],
                           self.args["division"][1],
                           self.args["division"][2]]
            opt["NSEC"] = self.args["nsec"]
            opt["SQRRATIO"] = self.args["coeur"]
            opt["RQUAD"] = [self.args["centre"]]+self.args["sections"]
            opt["IMPELLERCUT"] = self.args["cuts"]

            bottom = self.args["bottom"]
            lvlrot = [bottom[0]]
            shaft = [1 if bottom[1] == "on" else 0]
            hlay = [bottom[2]]
            for level in self.args["vertical"]:
                lvlrot.append(level[0])
                shaft.append(1 if level[1] == "on" else 0)
                hlay.append(level[2])

            opt["LVLROT"] = lvlrot
            opt["HLAY"] = hlay
            opt["SHAFT"] = shaft

            self.args["data"] = sm.superMarine(opt)
            print("Answer:\n")
            prettyJSON(self.args)
            self.write(self.args)
        elif self.args["type"] == "python":
            opt = dict()
            opt["r"] = self.args["division"][0]
            opt["theta"] = self.args["division"][1]
            opt["z"] = self.args["division"][2]
            opt["nsec"] = self.args["nsec"]
            opt["sqratio"] = self.args["coeur"]
            opt["rquad"] = [self.args["centre"]]+self.args["sections"]
            opt["impellercut"] = self.args["cuts"]

            bottom = self.args["bottom"]
            lvlrot = [bottom[0]]
            shaft = [1 if bottom[1] == "on" else 0]
            hlay = [bottom[2]]
            for level in self.args["vertical"]:
                lvlrot.append(level[0])
                shaft.append(1 if level[1] == "on" else 0)
                hlay.append(level[2])

            opt["lvlrot"] = lvlrot
            opt["hlay"] = hlay
            opt["shaft"] = shaft

            self.args["data"] = tk.genSupM(opt)
            print("Answer:\n")
            prettyJSON(self.args)
            self.write(self.args)


def prettyJSON(toFormat):
    for key,item in toFormat.items():
        toprint = "{}".format(item)
        toprint = toprint.replace("\n", "\\n")
        if len(toprint) > 23:
            toprint = toprint[:23]+"..."
        print("{:12}: {:24}".format(key, toprint))

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
