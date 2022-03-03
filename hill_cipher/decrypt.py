import numpy as np
from math import gcd
import sympy as matrix

def decrypt (ciphertext, key, m):
    #key = [9, 7, 11, 13, 4, 7, 5, 6, 2, 21, 14, 9, 3, 23, 21, 8]
    #ey = convertToInt(key)
    ciphertext = convertToInt(ciphertext)
    ciphertext = convertToMatrix(ciphertext,m)
    print(str(ciphertext))
    #key_matrix = convertToMatrix(key, m)
    #key_matrix = key
    #print(str(key_matrix))
    key_matrix = invertKey(key)
    print("Inverse: " + str(key_matrix))
    key_inverse = convert(key_matrix)
    print("Inverse: " + str(key_inverse))
    return plaintext(key_inverse, ciphertext, m)


def plaintext(key_matrix, ct_matrix, m):
    global pt_matrix
    pt_matrix = []
    print("C = " + str(ct_matrix))
    print("K_inv = " + str(key_matrix))
    for i in range (0, numOfRows):
        #print("i=" + str(i))
        new = []
        for j in range (0, m):
            #print("j=" + str(j))
            sum = 0
            for k in range (0, m):
                #print("k=" + str(k))
                sum = sum + ct_matrix[i][k] * key_matrix [k][j]
            #print(str(sum % 26))
            new.append(sum % 26)
        pt_matrix.append(new)
    print("PT: " + str(pt_matrix))
    pt_matrix = convertTo1DArray(pt_matrix,m)
    print("PT:" + str(pt_matrix))
    pt_matrix = convertToString(pt_matrix)
    print("PT:" + str(pt_matrix) + "\nLen: " + str(len(pt_matrix)))
    #pt_matrix = convertToString(pt_matrix, numOfRows, m)
    #print("PT:" + str(pt_matrix))
    print("PT: " + "".join(pt_matrix))
    return pt_matrix

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

# def convertToString(text, numOfRows,m):
#     text_Int = []
#     for i in range (0, numOfRows):
#         #print("i=" + str(i))
#         new = []
#         for j in range (0, m):
#             new.append((chr(text[i][j]) + 65))
#         text_Int.append(new)
#     return text_Int

def convertToMatrix (text, m):
    global numOfRows
    print('CT in int: ' + str(text))
    print('Converting to matrix ...')
    numOfRows = int( len(text) / m)
    element = 0
    matrix = []
    for i in range (0, numOfRows):
        new = []
        for j in range (0, m):
            new.append(text[element])
            element = element + 1
        matrix.append(new)
    return matrix

def convertTo1DArray(text,m): #For converting the CT matrix back to 1D alphabets
    matrix = []
    for i in range (0, numOfRows):
        for j in range (0, m):
            matrix.append(text[i][j])
    return matrix

def determinant (key):
    a = np.array(key)
    return int (np.linalg.det(a) % 26)

def convert (text):
    a = np.array(text)#.astype(np.float64))
    return a

def checkInvert (key):
    a = determinant(key)
    print("a = " + str(a))
    if gcd(a,26) == 1:
        return True
    else:
        return False

def invertKey (key):
    a = determinant(key)
    key = matrix.Matrix(key).inv_mod(26)
    return key



#if __name__ == '__main__':
    #key = [9, 7, 11, 13, 4, 7, 5, 6, 2, 21, 14, 9, 3, 23, 21, 8]
    #decrypt("OHKNIHGHFISS", key, 4)
