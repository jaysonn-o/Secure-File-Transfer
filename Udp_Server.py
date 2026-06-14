import socket

def udp_server():
    # Ask the user for a server identity and port number
    server_identity = input("Please, who are you? ")
    port = int(input("Enter the port number to listen on: "))

    # Create a socket for listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set socket option to reuse the address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind(("0.0.0.0", port))  # Listen on the specified port
        print(f"Server ({server_identity}) is listening on port {port}...")

        while True:
            # Wait for a broadcast message
            data, addr = server_socket.recvfrom(1024)
            message = data.decode()

            # Parse the sender and recipient from the message
            try:
                sender, _, recipient = message.partition(" is looking for ")
                print(f"Message received: {sender} is looking for {recipient}")

                # Check if the broadcast matches the server identity
                if recipient.strip() == server_identity:
                    # Respond to the sender
                    response = f"Hello {sender}, this is {server_identity}. Nice to meet you!"
                    server_socket.sendto(response.encode(), addr)
                    print(f"Response sent to {sender}")
            except ValueError:
                print("Invalid message format received.")
    except KeyboardInterrupt:
        print("\nServer script terminated by user.")
    finally:
        # Ensure the socket is closed
        server_socket.close()
        print("Socket closed. Exiting gracefully.")

if __name__ == "__main__":
    udp_server()
