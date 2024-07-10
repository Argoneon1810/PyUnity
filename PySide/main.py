from socket import socket, AF_INET, SOCK_STREAM
import json
import threading
from c_style_boolean import true, false


class some_dummy_class_for_example:
    def __init__():
        pass


class server():
    def __init__(self):
        self.read_options()

    def read_options(self):
        with open("promise.json") as ifile:
            self.options = json.load(ifile)

    def run(self):
        def converter(data: bytes):                 # do whatever conversion needed in here
            return data.decode(encoding=self.options['encoding'])
        def read(s: socket):
            data = s.recv(4)                                                # read 32 bit int
            if not data:                                                    # something went wrong
                raise ValueError()                                              # raise error
            size = int.from_bytes(data, self.options["number_endian"])      # convert bytes to int
            s.send(size.to_bytes(4, self.options["number_endian"]))         # send size for double check
            data = s.recv(size)                                             # re-read from remote using size above
            return converter(data)                                          # call your converter that fits your datatype
        def send(s: socket, data):
            b : bytes
            if type(data) is str:                                           # encode str into bytes
                b = data.encode(encoding=self.options['encoding'])
            else:                                                           # dump whateverdata into json str and encode it into bytes
                b = json.dumps(data).encode(encoding=self.options['encoding'])
            s.send(len(b).to_bytes(4, self.options['number_endian']))       # send the size of the bytes for preparation
            d = s.recv(4)                                                   # get response (length in 32 bit int)
            if int.from_bytes(d, self.options["number_endian"]) == len(b):  # if response matches the size of the bytes
                s.send(b)                                                       # send the actual bytes
            else:                                                           # something went wrong
                raise ValueError()                                              # raise error
        def worker(ip, port):
            s = socket(AF_INET, SOCK_STREAM)
            s.bind((ip, port))
            s.listen()
            conn, addr = s.accept()
            while conn:
                try:
                    data = read(conn)
                    print(data)
                    if data == self.options['begin']:
                        send(conn, self.options['begin'])
                    elif data == self.options['end']:
                        break
                    else:
                        # process data here
                        send(conn, data)
                except ValueError as e:
                    print("something went wrong")
                    break
            s.close()
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
