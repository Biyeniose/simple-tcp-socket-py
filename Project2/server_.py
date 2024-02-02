import socket
import threading

def encrypt(text, key): 
    result = [] # empty list
    text = text.upper() 
    key = key.upper() # uppercase

    j = 0 # track current position in the key
    for i in range(len(text)): # iterates over each character in the text
        text_char = text[i] # get current character from text

        if text_char < 'A' or text_char > 'Z': # if not uppercase
            result.append(text_char)
            continue # skips over the rest of the loop for this iteration

        key_char = key[j] # gets current character from the key

       # ord(c) converts chars to ASCII values
        # chr() converts shifted value back to character
        # -2*ord(A) = aligns A to 0 (in 0-25 range of alphabet) and enseres result wraps around alphabet (A=0,B=1,C=2)
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

def handle_many_clients(client_socket, client_address):
    closed = False
    while True:
        # recv(1024) receives data from client socket
        req = client_socket.recv(1024)
        req = req.decode("utf-8") # convert bytes to string
        decryp_req = decrypt(req,"TMU")
        
        if decryp_req.lower() == "bye":
            client_socket.send("connection closed".encode("utf-8"))
            closed = True
            client_socket.close()
            print(f"Client connection > ({client_address[0]}:{client_address[1]}) closed")
            break

        # if not
        if closed == False:
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
            # convert string to bytes
            response = ans_encryp.encode("utf-8")
            client_socket.send(response)


def server_code():
    closed = False
    key = "TMU"
    port = 5000  # server port number
    server_ip_addr = "127.0.0.1" 
    
    # creates socket object
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip_addr, port))
        server.listen()
        print(f"Server listening on {server_ip_addr}: {port}")

        while True: # infinite loop accepts many clients then uses thread to handle
            client_socket, client_addr = server.accept()
            print(f"Connection Accepted from {client_addr[0]}:{client_addr[1]}")

            # create new thread to handle new clients
            # Each client connection is handled in a separate thread
            thread = threading.Thread(target=handle_many_clients, args=(client_socket, client_addr,))
            thread.start()

        # server.close()      
    except Exception as e:
        print(f"error met: {e}")
    finally:
        server.close()

if __name__ == '__main__':
    server_code()

