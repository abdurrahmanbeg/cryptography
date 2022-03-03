
def encrypt (plaintext, key, m):
    #key = [9, 7, 11, 13, 4, 7, 5, 6, 2, 21, 14, 9, 3, 23, 21, 8]
    preprocess (plaintext, key, m)
    return cipherText(m)

def preprocess (plaintext, key, m):
    global pt_matrix, key_matrix
    print('Plain text: ' + plaintext)
    #plaintext = plaintext.replace('\n', '')
    #plaintext = plaintext.replace(' ', '')
    #plaintext = plaintext.upper()
    print('Plain text: ' + plaintext)
    print('Block size (m): ' + str(m))
    print('Length of PT: ' + str(len(plaintext)))
    plaintext = padding(plaintext, m)
    print('Plain text: ' + plaintext)
    plaintext = convertToInt(plaintext)
    print('PT in int: ' + str(plaintext))
    pt_matrix = convertToMatrix(plaintext,m)
    print(str(pt_matrix))
    #print("".join(convertToString(key)))
    #key = convertToInt(key)
    #key_matrix = convertToMatrix(key, m)
    #print(str(key_matrix))
    key_matrix = key
def cipherText (m):
    global ct_matrix
    ct_matrix = []
    print("P = " + str(pt_matrix))
    print("K = " + str(key_matrix))
    for i in range (0, numOfRows):
        #print("i=" + str(i))
        new = []
        for j in range (0, m):
            #print("j=" + str(j))
            sum = 0
            for k in range (0, m):
                #print("k=" + str(k))
                sum = sum + pt_matrix[i][k] * key_matrix [k][j]
            #print(str(sum % 26))
            new.append(sum % 26)
        ct_matrix.append(new)
    print("CT: " + str(ct_matrix))
    ct_string = convertToString(convertTo1DArray(m))
    print("CT: " + str(ct_string))
    return ct_string

def convertToInt (text):
    length = len(text)
    text_Int = []
    for i in range(0, len(text)):
        text_Int.append((ord(text[i]) - 65 ) % 26) #-65 on each char to get the int (via net) mod 26
    return text_Int

def convertToString(text):
    length = len(text)
    text_Int = []
    for i in range(0, len(text)):
        text_Int.append(chr(text[i] + 65)) #+65 on each char to get the int (via net) mod 26
    return text_Int

def convertTo1DArray(m): #For converting the CT matrix back to 1D alphabets
    matrix = []
    for i in range (0, numOfRows):
        for j in range (0, m):
            matrix.append(ct_matrix[i][j])
    return matrix

def padding (text, m):
    length = len(text)
    if  length % m  == 0:
        print("Even")
        return text
    else:
        print("Padding is needed (letter 'z')")
        text = text + str("Z")
        return text

def convertToMatrix (text, m):
    global numOfRows
    print('Converting to matrix ...')
    numOfRows = int( len(text) / m)
    element = 0
    matrix = []
    #print('Num of Rows = ' + str(numOfRows))
    for i in range (0, numOfRows):
        new = []
        for j in range (0, m):
            new.append(text[element])
            element = element + 1
        matrix.append(new)
    return matrix

#if __name__ == '__main__':
    #key = [9, 7, 11, 13, 4, 7, 5, 6, 2, 21, 14, 9, 3, 23, 21, 8]
    #encrypt("Code is ready", key, 4)
