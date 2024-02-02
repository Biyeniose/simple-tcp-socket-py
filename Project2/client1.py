import socket

def encrypt(text, key): # same as java class
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


def client_code():
    # create socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1" 
    server_port = 5000
    key = "TMU"
    # establish connection with server
    client.connect((server_ip, server_port))

    while True:
        # input message and send it to the server
        msg = input("Enter message: ")
        # client socket object sends message after encoding to bytes
        # only up to 1024 bytes
        cipher_msg = encrypt(msg,"TMU")
        client.send(cipher_msg.encode("utf-8")[:1024])
        # client.send(msg.encode("utf-8")[:1024])

        # cliebt socket object receive message from the server
        resp = client.recv(1024)
        resp = resp.decode("utf-8")

        decipher_resp = decrypt(resp, "TMU")

        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if resp.lower() == "connection closed":
            break

        print(f"Server Cipher: {resp}")
        print(f"Server Plaintext: {decipher_resp.lower()}")
        print("---------------------------------------------------------------")

    # close client socket (connection to the server)
    client.close()
    print("Server Connection closed")


if __name__ == '__main__':
    client_code()

