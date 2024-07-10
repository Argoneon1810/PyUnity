from socket import socket, AF_INET, SOCK_STREAM
import json
import threading
from c_style_boolean import true, false


class server():
    def __init__(self):
        self.read_options()

    def read_options(self):
        with open("promise.json") as ifile:
            self.options = json.load(ifile)

    def run(self):
        def worker(ip, port):
            s = socket(AF_INET, SOCK_STREAM)
            s.bind((ip, port))
            s.listen()
            conn, addr = s.accept()
            while conn:
                data = conn.recv(1024)
                if not data:
                    break
                resp = data.decode(encoding="utf8")
                print(resp)
                if resp == self.options['begin']:
                    conn.send(self.options['begin'].encode(encoding="utf8"))
                elif resp == self.options['end']:
                    s.close()
                    break
                else:
                    # process data here
                    conn.sendall(data)
        print("Establishing TCP Server")
        print(f"With IP: {self.options['ip']}:{self.options['port']}")
        self.server_thread = threading.Thread( \
            target=worker, \
            args=[self.options["ip"], int(self.options["port"])] \
        )
        print("Setting server as background task")
        self.server_thread.isDaemon = true
        print("Setting Finished")
        print("Running Server")
        self.server_thread.run()



def main():
    s = server()
    s.run()


if __name__ == "__main__":
    main()
