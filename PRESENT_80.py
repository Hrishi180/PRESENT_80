


# Declaring variable for storing the round keys

roundKeys = [0 for x in range(32)]

# Sbox declaration
SBox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

# Pbox declaration
PBox = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
        4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
        8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
        12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]


# Function to perform Add round key operation
def add_roundkey(state, roundkey):
    return state ^ roundkey


# Function to perform Sbox Substitution
def substitute(state):
    substitute_state = 0
    for i in range(16):
        substitute_state |= SBox[(state >> 4 * i) & 0xf] << (4 * i)
    return substitute_state

# Function to perform Pbox substitution
def permute(state):
    permute_state = 0
    for i in range(64):
        permute_state |= ((state >> i) & 0x1) << PBox[i]
    return permute_state


# Function to convert from decimal to hexadecimal format
def dectohex(dec):
    return format(dec, '016x')


# Function to perform key expansion

def keyexpansion(left, right):

    # input: 80-bit key splited into 64 bits and 16 bits

    # Looping to generate 31 keys 
    for i in range(32):
    
        roundKeys[i] = left
       #  print('Round key ' + str(i + 1) + ': ' + dectohex(roundKeys[i]))

        temp = right
        right = (left >> 3) & 0xffff
        left = ((left << 61) | (temp << 45) | (left >> 19)) 

        temp = left
        left = (SBox[(left >> 60) & 0xf] << 60)
        left |= (temp & 0x0fffffffffffffff)

        counter = (i + 1) & 0x1f
        left ^= counter >> 1
        right ^= (counter & 0x1) << 15


# Function to perform encryption algorithm

def encry_algo(message, key):
    leftkey, rightkey = int(key[:-4], 16), int(key[16:], 16)

    state = int(message, 16)
    keyexpansion(leftkey, rightkey)

# Loop the function 31 times 
    for i in range(31):
        state = add_roundkey(state, roundKeys[i])
        state = substitute(state)
        state = permute(state)
       # print(f'Round Output {i + 1}: {dectohex(state)}')

# Perform add round key
    cipher = add_roundkey(state, roundKeys[31])

# Print the final Ciphertext
    print(f'Ciphertext: {dectohex(cipher)}')


# The main function
if __name__ == "__main__":

# 80 bit key for test
    key = '04040404040404040404' 

# 64 bit block plain text for encryption
    message = '0404040404040404' 
# Calling the funtion to perfrom encryption
    print("Message: {}".format(message))
    print("Key: {}".format(key))
    encry_algo(message, key)

