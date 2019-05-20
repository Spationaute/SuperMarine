import tornado.ioloop
import tornado.web

class SuperMarine(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")


def application():
    app = [
        (r"/", SuperMarine)
    ]
    return tornado.web.Application(app)

if __name__=="__main__":
    app = app();
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
