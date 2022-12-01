import numpy as np

hex_letters = ["0", "1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
binVal = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]
roundConstants = ["0000000000000000", "13198a2e03707344","a4093822299f31d0", "082efa98ec4e6c89", "452821e638d01377", "be5466cf34e90c6c", "7ef84f78fd955cb1", "85840851f1ac43aa", "c882d32f25323c54", "64a51195e0e3610d", "d3b5a399ca0c2399", "c0ac29b7c97c50dd"]
shiftNibbles = [0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11]

sbox = [11, 15, 3, 2, 10, 12, 9, 1, 6, 7, 8, 0, 14, 5, 13, 4]

def hexToInt(hexString):
    return hex_letters.index(hexString)

def intToHex(intVal):
    return (hex_letters[intVal])

def hexToBin(hexString):
    return binVal[hex_letters.index(hexString)]

def makeBinString(hexString):
    binString =""
    for i in range(16):
        binString+=hexToBin(hexString[i])
    return binString

def binListHexString(binList):
    ansList=[]
    for i in range(len(binList)):
        ansList.append(binToHex(binList[i]))
    ansString=""
    ansString=ansString.join(ansList)
    return ansString

def binToHex(binString):
    return hex_letters[binVal.index(binString)]

def substitution(inputHex):
    resString=""
    for i in range(16):
        resString+=intToHex(sbox[hexToInt(inputHex[i])])
    return resString

def substitutionInverse(inputHex):
    resString=""
    for j in range(16):
        for i in range(16):
            if hexToInt(inputHex[j])==sbox[i]:
                resString+=intToHex(i)
                break
    return resString

def keyWhitening(key):
    k0 = key[0:16]
    k1 = key[16:32]
    k0_bin =makeBinString(k0)
    k0_ = k0_bin[63]+k0_bin[0:63]
    k0_ = k0_[0:63]+ str(int(k0_[63])^int(k0_bin[0]))
    k0_list = [(k0_[i:i+4]) for i in range(0, len(k0_), 4)]
    k0_=binListHexString(k0_list)
    return k0+k0_+k1

def roundXor(inputHex, round):
    resString=""
    for i in range(16):
        resBit = hexToInt(inputHex[i])^hexToInt(roundConstants[round][i])
        resString+=intToHex(resBit)
    return resString

def keyXor(inputHex, keyHex):
    resString=""
    for i in range(16):
        resBit = hexToInt(inputHex[i])^hexToInt(keyHex[i])
        resString+=intToHex(resBit)
    return resString

def shiftRows(inputHex):
    resString=""
    for i in range(16):
        resString+=inputHex[shiftNibbles[i]]
    return resString

def shiftRowsInverse(inputHex):
    resString=""
    for i in range(16):
        resString+=inputHex[shiftNibbles.index(i)]
    return resString

def matrixLayer(inputHex):
    resList=[]
    m0 = np.matrix([[0,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])
    m1 = np.matrix([[1,0,0,0], [0,0,0,0], [0,0,1,0], [0,0,0,1]])
    m2 = np.matrix([[1,0,0,0], [0,1,0,0], [0,0,0,0], [0,0,0,1]])
    m3 = np.matrix([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,0]])
    zeroMatrix = np.matrix([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]])
    
    m0_ = np.vstack(((np.hstack((m0,m1,m2,m3))), np.hstack((m1,m2,m3,m0)), np.hstack((m2,m3,m0,m1)), np.hstack((m3,m0,m1,m2))))
    m1_ = np.vstack(((np.hstack((m1,m2,m3,m0))), np.hstack((m2,m3,m0,m1)), np.hstack((m3,m0,m1,m2)), np.hstack((m0,m1,m2,m3))))
    bigZeroMatrix = np.vstack(((np.hstack((zeroMatrix,zeroMatrix,zeroMatrix,zeroMatrix))), np.hstack((zeroMatrix,zeroMatrix,zeroMatrix,zeroMatrix)), np.hstack((zeroMatrix,zeroMatrix,zeroMatrix,zeroMatrix)), np.hstack((zeroMatrix,zeroMatrix,zeroMatrix,zeroMatrix))))

    mPrime = np.vstack(((np.hstack((m0_,bigZeroMatrix,bigZeroMatrix,bigZeroMatrix))), np.hstack((bigZeroMatrix,m1_,bigZeroMatrix,bigZeroMatrix)), np.hstack((bigZeroMatrix,bigZeroMatrix,m1_,bigZeroMatrix)), np.hstack((bigZeroMatrix,bigZeroMatrix,bigZeroMatrix,m0_))))

    inputBin = makeBinString(inputHex)

    for i in range(len(inputBin)):
        mulResult = 0
        for j in range(64):
            mulResult^=int(inputBin[j])*mPrime.item((j,i))
        resList.append(mulResult)

    resList=[(''.join(map(str,resList[i:i+4]))) for i in range(0,len(resList),4)]

    return (binListHexString(resList))

def commonEncDecFunction(plaintext, k0, k0Prime, k1):
    firstXor = keyXor(plaintext, k0)
    pCoreXor = keyXor(firstXor, k1)
    nextXor = roundXor(pCoreXor,0)

    for i in range(1,6):
        subStep = substitution(nextXor)
        difStep = matrixLayer(subStep)
        nextDifStep = shiftRows(difStep)
        roundCStep = roundXor(nextDifStep, i)
        nextXor = keyXor(roundCStep, k1)

    midSub = substitution(nextXor)
    matrixRes = matrixLayer(midSub)
    midSubInv = substitutionInverse(matrixRes)

    for j in range(6,11):
        nextOp = keyXor(midSubInv, k1)
        roundCStep = roundXor(nextOp, j)
        shiftInv = shiftRowsInverse(roundCStep)
        difStep = matrixLayer(shiftInv)
        midSubInv = substitutionInverse(difStep)

    lastRoundXor = roundXor(midSubInv, 11)
    lastKeyXor = keyXor(lastRoundXor, k1)

    afterCore = keyXor(lastKeyXor, k0Prime)

    return afterCore


def princeEncryption(plaintext, key):
    expandedKey = keyWhitening(key)
    k0 = expandedKey[0:16]
    k0Prime = expandedKey[16:32]
    k1=expandedKey[32:48]

    encryption = commonEncDecFunction(plaintext, k0, k0Prime, k1)
    return encryption

def princeDecryption(ciphertext, key):
    expandedKey = keyWhitening(key)
    k0= expandedKey[0:16]
    k0Prime = expandedKey[16:32]
    k1=expandedKey[32:48]

    new_k1=keyXor(k1, "c0ac29b7c97c50dd")

    decryption = commonEncDecFunction(ciphertext, k0Prime, k0, new_k1)
    return decryption

def ECBModeEnc(plaintext, key):
    input_list = [(plaintext[i:i+16]) for i in range(0, len(plaintext), 16)]
    finalEncryption=""
    for k in input_list:
        finalEncryption+=princeEncryption(k, key)
    return finalEncryption

def ECBModeDec(ciphertext, key):
    input_list = [(ciphertext[i:i+16]) for i in range(0, len(ciphertext), 16)]
    finalDecryption=""
    for k in input_list:
        finalDecryption+=princeDecryption(k, key)
    return finalDecryption

def CBCModeEnc(plaintext, key, iv):
    input_list = [(plaintext[i:i+16]) for i in range(0, len(plaintext), 16)]
    finalEncryptionList = [iv]
    for k in range(len(input_list)):
        finalEncryptionList.append(princeEncryption(keyXor(input_list[k], finalEncryptionList[k]), key))
    ansString=""
    ansString=ansString.join(finalEncryptionList)
    return ansString

def CBCModeDec(ciphertext, key):
    input_list = [(ciphertext[i:i+16]) for i in range(0, len(ciphertext), 16)]
    finalDecryption=""
    for i in range(1, len(input_list)):
        decryptPrince = princeDecryption(input_list[i], key)
        cbcXor = keyXor(decryptPrince, input_list[i-1])
        finalDecryption+=cbcXor
    return finalDecryption

# print(princeEncryption("0000000000000000", "00000000000000000000000000000000"))
# print(princeDecryption("818665aa0d02dfda", "00000000000000000000000000000000"))

encOrdec = input("Enter E for encryption or D for decryption: ")
inputText = input("Enter the plaintext/ciphertext.")
inputKey = input("Enter the 128 bit key: ")
mode = input("Enter the mode (ECB/CBC): ")

while (len(inputText)%16!=0):
    inputText+="0"

while (len(inputKey)<32):
    inputKey+="0"

if (mode=="CBC"):
    if (encOrdec=="E"):
        iv = input("Enter a 64 bit iv: ")
        while (len(iv)<16):
            iv+='0'
        ciphertext = CBCModeEnc(inputText, inputKey, iv)
        print(ciphertext)
    else:
        plaintext = CBCModeDec(inputText, inputKey)
        print(plaintext)
elif (mode=="ECB"):
    if (encOrdec=="E"):
        ciphertext = ECBModeEnc(inputText, inputKey)
        print(ciphertext)
    else:
        plaintext =ECBModeDec(inputText, inputKey)
        print(plaintext)
