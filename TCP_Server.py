import socket
import ssl
import os

def tcp_tls_server():
    server_identity = input("Please, who are you? ")  # Server identity
    port = int(input("Enter the port number to listen on: "))
    file_to_send = input("Enter the file path to broadcast: ")

    if not os.path.exists(file_to_send):
        print("File not found!")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)

    # Configure TLS context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="Jason_cert.pem", keyfile="private.pem")  # Server certificate only
    context.check_hostname = False  # No hostname validation
    context.verify_mode = ssl.CERT_NONE  # No client certificate verification

    print(f"Server ({server_identity}) is listening on port {port}...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection established with {addr}")

            secure_socket = context.wrap_socket(client_socket, server_side=True)
            try:
                data = secure_socket.recv(1024).decode()
                sender, _, recipient = data.partition(" is looking for ")
                print(f"Message received: {sender} is looking for {recipient}")

                if recipient.strip() == server_identity:
                    secure_socket.send(f"Hello {sender}, this is {server_identity}. Sending file...".encode())
                    with open(file_to_send, "rb") as file:
                        while chunk := file.read(1024):
                            secure_socket.send(chunk)
                    print(f"File '{file_to_send}' sent to {sender}")
                else:
                    secure_socket.send("Identity mismatch!".encode())
            except Exception as e:
                print(f"Error during communication: {e}")
            finally:
                secure_socket.close()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_socket.close()
        print("Socket closed.")

if __name__ == "__main__":
    tcp_tls_server()
