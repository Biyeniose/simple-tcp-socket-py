import socket

def encrypt(text, key): # same as java class
    result = [] # empty list
    text = text.upper() 
    key = key.upper() # uppercase

    j = 0 # track current position in the key
    for i in range(len(text)): # iterates over each character in the text
        text_char = text[i] # get current character from text

        if text_char < 'A' or text_char > 'Z': # if not uppercase
            result.append(text_char) # ignores numbers and ponctuations
            continue # skips over the rest of the loop for this iteration

        key_char = key[j] # gets current character from the key

        # ord(c) converts chars to ASCII values
        # chr() converts shifted value back to character
        # -2*ord(A) = aligns A to 0 (in 0-25 range) and enseres result wraps around alphabet (A=0,B=1,C=2)
        # %26 = ensures result stays within 0 to 25 (alphabet numbers)
        # + ord(A) = we have a number between 0 and 25, but you need to convert back to char
        # so it shifts your 0-25 range back up into the ASCII range.
        # 0 is now 65 which is A, 1 -> 66 -> B
        
        # goal is to shift the text char by a certain lenght determind by the key char
        encrypted_c = chr((ord(text_char) + ord(key_char) - 2 * ord('A')) % 26 + ord('A'))
        result.append(encrypted_c)

        j = (j + 1) % len(key) # updates j to point to next char in key
                               # loops back if end of key is reached
    return ''.join(result) # joins a list into a string (no spaces between them)


def decrypt(text, key):
    result = []
    text = text.upper()
    key = key.upper()

    j = 0
    for i in range(len(text)):
        text_char = text[i]
        if text_char < 'A' or text_char > 'Z':
            result.append(text_char)
            continue

        key_char = key[j]
        # ord() gives numerical values to the chars
        # subtract instead of adding, (+ 26) is to stay within the 0 to 25 range A-Z
        # % 26 = modulus
        decrypted_c = chr((ord(text_char) - ord(key_char) + 26) % 26 + ord('A'))
        result.append(decrypted_c)

        j = (j + 1) % len(key)

    return ''.join(result)


def find_hint(hints, question):
    for index, hint in enumerate(hints):
        if hint in question:
            return index
    return -1 

def server_code():
    # create socket object with socket.socket
    # socket.AF_INET specifies the address family, AF_INET = IPv4
    # socket.SOCK_STREAM specificies socket type = TCP socket 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port_num = 2001
    # loopback address that only accepts connections from same machine as server
    server_ip = "127.0.0.1"
    closed = False
    key = "TMU"

    answers = [
        "I was made by talented engineers at Apple",
        "Siri is of Scandenavian descent, it means Victory and beautiful",
        "I dont have a gender because I am a language model",
        "The capital of Canada is Ottawa",
        "You never know ¯\_(ツ)_/¯",
        "I can speak any language you want me to",
        "Lagos is located in the South of Nigeria",
        "Argentina won the World Cup",
        "I was made in 2011 making me 12 years old",
        "My favorite color is silver",
        "Spain is in Europe"
    ]

    hints = [
        "made",
        "mean",
        "gender",
        "capital",
        "aliens",
        "languages",
        "lagos",
        "world cup",
        "old",
        "color",
        "spain"
    ]
    

    # binds socket to IP addr 127.0.0.1 and port 2000
    # now server can listen for connections from this IP and port
    server.bind((server_ip, port_num))
    # listen for incoming connections
    server.listen(0)
    print(f"Server listening on {server_ip}:{port_num}")

    # accepts connections. waits till client connects
    # when a client connects it returns a new socket object(connection) 
    # and a tuple with its address
    client_socket, client_ip = server.accept()
    # 1st element = ip addr of client, 2nd = port number
    print(f"Connection Accepted from {client_ip[0]}:{client_ip[1]}")

    # receive data from the client
    while True:
        # recv(1024) receives data from client socket
        req = client_socket.recv(1024).decode("utf-8")
        #req = req.decode("utf-8") # convert bytes to string
        decryp_req = decrypt(req,"TMU")
        
        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        if decryp_req.lower() == "bye":
            # send response to the client to indicated ended connection
            client_socket.send("connection closed".encode("utf-8"))
            closed = True
            break

        # if not
        if closed == False:
            # print(f"Client: {req}")
            print(f"Client Cipher: {req}")
            print(f"Client Plaintext: {decryp_req.lower()}")
            print("---------------------------------------------------------------")
            found_index = find_hint(hints, decryp_req.lower())

            if(found_index == -1):
                answer = "Sorry I cant answer that"
            else:
                answer = answers[found_index]

            # encode first  
            ans_encryp = encrypt(answer, "TMU")  
            # response = answer.encode("utf-8") # convert string to bytes
            response = ans_encryp.encode("utf-8")

            # convert and send accept response to the client
            client_socket.send(response)

    # close connection socket with the client
    client_socket.close()
    print("Client Connection closed")
    # close server socket
    server.close()


if __name__ == '__main__':
    server_code()
