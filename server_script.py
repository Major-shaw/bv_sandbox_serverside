from db_script import db_main, delete_db
from container_script import create_container, delete_container
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from base64 import b64encode
import logging

hostName = "206.189.138.203"
serverPort = 47157
validIPs = ["175.100.148.0", "171.76.82.251"]
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

#key = b64encode(b"atulyasingh:password").decode('UTF-8')

class MyServer(BaseHTTPRequestHandler):

    def authenticate(self):
        if self.client_address[0] in validIPs:
            return True
        return False

    def do_POST(self):
        print('Recieved post request')
        if not self.authenticate():
            self.send_error(500, "authentication error")
            logging.error("code: 500 authentication error")
            self.end_headers()
            return

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        logger.info("POST request,\n Client ip: %s\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.client_address[0]),str(self.path), str(self.headers), data)
        db_name = data["name"]
        db_username = data["db_username"]
        db_password = data["db_password"]
        admin = data["admin_username"]
        admin_password = data["admin_password"]
        wp_version = data["wp_version"]
        php_version = data["php_version"]

        if db_main(db_name, db_username, db_password, admin, admin_password) == 200 and create_container(db_name, db_username, db_password, wp_version, php_version) == 200:
            self.send_response(200)
            logging.info("code 200 Site created")
        else:
            self.send_error(500, "Internal Server Error! Try again later")
            logging.error("code: 500 Internal server error")
        self.end_headers()

    def do_DELETE(self):
        if not self.authenticate():
            self.send_error(500, "Authentication error")
            logging.error("code: 500 Authenctication error")
            self.end_headers()
            return
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        logger.info("DELETE request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), data)
        db_name = data["name"]
        db_username = data["db_username"]
        if delete_db(db_name, db_username) == 200 and delete_container(db_name) == 200:
            self.send_response(200)
            logging.info("code: 200 Deleted Successfully")
        else:
            self.send_response(1000, "Unable to delete site")
            logging.error("code: 1000 Unable to delete site")

        self.end_headers()


if __name__ == "__main__":
    log_file = 'server_log.log'
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger('server_log')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    logger.info("Starting server...\n")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
    logger.info("Stopping server... \n")


