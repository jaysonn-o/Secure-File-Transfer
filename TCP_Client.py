import socket
import ssl

def tcp_tls_client():
    server_address = input("Enter the server address: ")
    port = int(input("Enter the port number to connect to: "))
    sender_identity = input("Please, who are you? ")
    recipient_identity = input("Who are you looking for? ")

    context = ssl.create_default_context()
    context.check_hostname = False  # Skip hostname validation
    context.verify_mode = ssl.CERT_NONE  # Disable server certificate verification

    with socket.create_connection((server_address, port)) as client_socket:
        with context.wrap_socket(client_socket, server_hostname=server_address) as secure_socket:
            print(f"Connected to {server_address}:{port} with TLS encryption")

            # Send a message to the server
            message = f"{sender_identity} is looking for {recipient_identity}"
            secure_socket.send(message.encode())

            # Receive the server's response
            response = secure_socket.recv(1024).decode()
            print(f"Server says: {response}")

            if "Sending file..." in response:
                file_name = f"{recipient_identity}_received_file"
                with open(file_name, "wb") as file:
                    while chunk := secure_socket.recv(1024):
                        file.write(chunk)
                print(f"File saved as '{file_name}'")
            else:
                print("No file received.")

if name == "main":
    tcp_tls_client()
