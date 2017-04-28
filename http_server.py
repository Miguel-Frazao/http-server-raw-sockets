import threading, socket, queue

class Server:
    def __init__(self):
        self.conns = set() # all connections
        self.print_queue = queue.Queue()
        t = threading.Thread(target=self.print_manager)
        t.daemon = True
        t.start()
        del t

    def print_manager(self):
        while True:
            msg = self.print_queue.get()
            print(msg)
            self.print_queue.task_done()

    def run(self, addr, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((addr, port))
            sock.listen(5)
            self.print_queue.put('Server started at {}:{}\n'.format(addr, port))
            while True:
                client, addr = sock.accept()
                self.conns.add(client)
                self.print_queue.put("New Connection: {}\nConnections {}: {}\n\n".format(addr, len(self.conns), self.conns))
                t = threading.Thread(target=self.response, args=(client,))
                t.start()

    def response(self, client):
        raw = client.recv(1024)
        client.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n<h1>HEYA {}</h1>i\'m thread: {}'.format(client.getpeername(), threading.current_thread().getName()).encode('utf-8'))
        client.close()

server = Server()
server.run('', 9005) # adjust host/port
