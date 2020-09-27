"""
server.py creates an instance of a server. It calls upon several request handlers, all of which process things slightly differently.
"""
import os
from http.server import BaseHTTPRequestHandler
from routes.main import routes
from pathlib import Path
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from human_backend import pending_comp, finished_comp, page_load_ack, FinishedEntry, AckEntry
# This file implements the server class for our webserver

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    #processes a get request -this is where most of the action lies
    def do_GET(self):
        request_tokens = self.path.split('?')
        self.path = request_tokens[0]

        #here we are checking the file type of the requested object. This is how we know how to handle the request
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        #if it's an html then we probably got a comparison submission
        if (request_extension == "") or (request_extension == ".html"):
            #if we did in fact get a comparison
            if len(request_tokens) > 1:
                values, submit = request_tokens[1].split("&")
                values = values.split('=')[1].split('%26')
                print('values <{}>'.format(values))
                print('submit <{}>'.format(submit))

                #process the data according to user submission. We put the answer on the FinishedEntry queue (this is used in human_backend to keep track of comparisons for the human phase)
                if submit == "submit=A":
                    try:
                        closer = values[1]
                        further = values[2]
                        finished_comp.put(FinishedEntry(main_pic_name = values[0], closer_pic_name = closer, further_pic_name = further))
                    except:
                        # On bad html requests, just ignore it and move on
                        pass
                elif submit == "submit=B":
                    try:
                        closer = values[2]
                        further = values[1]
                        finished_comp.put(FinishedEntry(main_pic_name = values[0], closer_pic_name = closer, further_pic_name = further))
                    except:
                        # On bad html requests, just ignore it and move on
                        pass
            #routes is a folder that houses our html page. We made it a folder for later project expansion.
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()
        elif request_extension is ".py":
            #if someone is trying to hack us
            handler = BadRequestHandler()
        else:
            #StaticHandler is sorta our catch all for images
            handler = StaticHandler()
            handler.find(self.path)

        self.respond({
            'handler': handler
        })

    def do_POST(self):
        return

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())

            #keller.jpg is a hardcoded image that we call. This is done because we dynamically change the pictures we are serving according to the queue -
            # essentially we are intercepting keller.jpg and changing it accordingly.
            if (self.path == "/keller.jpg"):
                #grab new files
                #files: comparison, A, B
                entry = pending_comp.get()

                # Ack
                page_load_ack.put(AckEntry(entry.main_pic.uid))

                #this is the string that we pass that contains each of the queue objects. The html file parses this and posts the correct photo.
                headerstring = "$" + entry.main_pic.name + "&" + entry.comp_a.name + "&" + entry.comp_b.name + "&" + entry.code +"$"
                print("header: <{}>".format(headerstring))
                self.send_header("File-Names", headerstring)
        else:
            content = "404 Not Found"

        self.end_headers()

        if isinstance(content, (bytes, bytearray)):
            return content

        return bytes(content, "UTF-8")

    def respond(self, opts):
        try:
            response = self.handle_http(opts['handler'])
            self.wfile.write(response)
        except BrokenPipeError:
            pass
