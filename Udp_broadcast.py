import socket

def udp_broadcast():
    try:
        # Ask the user for a port number to send/receive messages
        port = int(input("Enter the port number to use for broadcast: "))

        # Create a socket for sending and listening
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client_socket.bind(("0.0.0.0", port))  # Bind to the specified port

        # Get user input for broadcast message
        sender = input("Please, who are you? ")
        recipient = input("Who are you looking for? ")

        # Create the broadcast message
        message = f"{sender} is looking for {recipient}".encode()

        # Send the broadcast
        client_socket.sendto(message, ("<broadcast>", port))
        print(f"Broadcast sent on port {port}.")

        # Listen for responses
        print(f"Listening for responses on port {port}...")
        while True:
            data, addr = client_socket.recvfrom(1024)
            print(data.decode())
    except KeyboardInterrupt:
        print("\nBroadcast script terminated by user.")
    finally:
        client_socket.close()
        print("Socket closed. Exiting gracefully.")

if name == "main":
    udp_broadcast()
