import socket

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()

    # Reserve a port for your service.
    port = 49673

    # Bind to the port
    server_socket.bind((host, port))

    # Wait for client connection.
    server_socket.listen(1)
    print('Server listening on {}:{}'.format(host, port))

    while True:
        # Establish connection with client.
        client_socket, addr = server_socket.accept()
        print('Got connection from', addr)

        # Send a message to the client.
        message = 'Hello, client!'
        client_socket.send(message.encode('ascii'))

        # Receive data from the client.
        data = client_socket.recv(1024)
        print('Received data:', data.decode('ascii'))

        # Send a response to the client.
        response = 'Thank you for connecting!'
        client_socket.send(response.encode('ascii'))

        # Close the connection.
        client_socket.close()

if __name__ == '__main__':
    start_server()
