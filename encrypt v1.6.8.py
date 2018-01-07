#Encoder v1.6.8

#OPTIONAL password feature
    #supports up to 74 characters long
    #encrypted with custom cipher and rot-13
#new encoder
#further optimisations
#further bug checks and redevelopments
#larger alphabet and encoder

from random import *
from codecs import *

#lowercase,uppercase,numbers,full stop,comma,question mark,exclamation mark,apostrophe,hyphon,speech mark,star,space,hashtag,slash,brackets,@,&,colon,semicolon,equals,underscore,^
alphabet = ['A', 'z', '!', 'f', ";", ":", 'u', '"', '-', 'B', '@', 'Y', 'p', 'I', '7', '2', 'D', "'", 'U', 'F', '5', 'J', '9', '3', 'T', '0', 'X', 'G', '/', '_', 'y', 'H', '=', 'b', 'k', '^', 't', 'c', 'S', 'W', ' ', 'N', 'e', 'x', '&', '6', '?', 'C', 'w', 'R', 'h', 'Z', 'v', 'K', '1', '*', 'g', 'L', 'm', 'E', 'O', '4', 'd', 's', 'M', '8', ',', 'q', 'r', ')', 'n', 'i', '#', 'V', 'o', '.', '(', 'j', 'l', 'P', 'a', 'Q']
encoder = ("B?mRocwOb`Ch(N.M8tEnF>S-Hj6Y^fu]g~Q#0+<_UGkiyl2p7}z'vI[rqA!W1Z9aXVd)Px{ DeK3TJ5L4s")
encoder = list(map(str,encoder))

#unique checker (checks if every item is unique)

check = False

def unique():
    a = [];b = []
    for i in alphabet:
        a.append(i)
    for i in encoder:
        b.append(i)
    x = [a,b]
    for n in x:
        while 0 < len(n):
            tmp = n[0]
            del n[0]
            for i in n:
                if i == tmp:
                    print(i)

if check:
    check()

#Rescramble encoder/alphabet:

#shuffle(alphabet)
#shuffle(encoder)
#print(alphabet)
#print("".join(encoder))

def get_length():
    length = {}
    for i in range(len(alphabet)):
        length[i] = alphabet[i]
    return length
password_length = get_length()

class encrypt:
    def get_string(self,string):
        numbers = []
        for i in string:#turns string into numbers based on alphabet
            numbers.append(alphabet.index(i))
        return numbers
        
    def get_cipher(self,string):
        numbers = []
        for i in string:#creates pseudo-random cipher
            numbers.append(randint(0,len(alphabet)))
        return numbers
        
    def convert(self,string):
        string_num = self.get_string(string)
        cipher_num = self.get_cipher(string)
        output_num = []
        ciphertext = []
        cipher = []
        
        for i in range(len(string)):
            tmp_sum = string_num[i] + cipher_num[i]
            if tmp_sum > len(alphabet) - 1:
                tmp_sum -= len(alphabet)
                cipher_num[i] -= len(alphabet)
            output_num.append(tmp_sum)#gets ciphertext pos

        for i in range(len(cipher_num)):
            cipher.append(encoder[cipher_num[i]])
            ciphertext.append(encoder[output_num[i]])#creates ciphertext
        
        cipher += ciphertext#cipher is first half
        return cipher

    def get_password(self,password):
        output = []
        cipher_num = []
        password_num = []
        output_num = []
        
        output.append(password_length[len(password)])#1st character of any string is length of password

        for i in password:
            cipher_num.append(randint(0,len(alphabet)-1))
            password_num.append(alphabet.index(i))#gets pos

        for i in cipher_num:
            output.append(encoder[i])

        for i in range(len(cipher_num)):
            tmp_sum = cipher_num[i] + password_num[i]
            if tmp_sum > len(alphabet) - 1:
                cipher_num[i] -= len(alphabet)
                tmp_sum -= len(alphabet)
            output.append(encoder[tmp_sum])#encodes ciphertext

        return list(encode("".join(output),"rot-13"))#encodes with rot-13
        
    def encrypt(self,string,password=[]):
        password_output = self.get_password(password)
        
        pre = self.convert(string)
        layer1 = []
        layer2 = []
        layer3 = []

        for i in pre:#white noise
            layer1.append(i)
            layer1.append(encoder[randint(0,len(encoder)-1)])

        tmp1 = layer1[:int(len(layer1)/2)]#slices list for efficiency
        tmp2 = layer1[int(len(layer1)/2):]#faster than appending every 2nd item, then reversing list and appendint list
        tmp2.reverse()

        for i in range(len(tmp1)):#[fist,last,2nd,2nd last...] - zigzag pattern
            layer2.append(tmp1[i])
            layer2.append(tmp2[i])

        for i in layer2:#white noise
            layer3.append(encoder[randint(0,len(encoder)-1)])
            layer3.append(i)

        return ["|"] + password_output + layer3 + ["|"]

class decrypt:  
    def unscramble(self,string):
        layer3 = string
        layer2 = []
        layer1 = []
        layer1_tmp = []
        unscrambled = []

        for i in range(len(layer3)):#appends every 2n-1 term
            if ((i + 1) % 2):
                layer2.append(layer3[i+1])

        for i in range(len(layer2)):#removes zigzag scramble
            if (i % 2):
                layer1_tmp.append(layer2[i])
            else:
                layer1.append(layer2[i])
        layer1_tmp.reverse()
        layer1 += layer1_tmp

        for i in range(len(layer1)):#appends every 2n-2 term
            if not (i % 2):
                unscrambled.append(layer1[i])

        return unscrambled

    def decrypt(self,string):
        both = self.unscramble(string)
        cipher = both[:int(len(both)/2)]#first half of unscrambled text is cipher
        ciphertext = both[int(len(both)/2):]
        cipher_num = []
        ciphertext_num = []
        output_str = []

        output_num = []

        for i in range(len(cipher)):#converts text into encoder pos
            cipher_num.append(encoder.index(cipher[i]))
            ciphertext_num.append(encoder.index(ciphertext[i]))

        for i in range(len(cipher)):
            tmp_sum = ciphertext_num[i] - cipher_num[i]
            if tmp_sum < 0:
                tmp_sum += len(alphabet)#converts ciphertext into numerical plaintext
            output_str.append(alphabet[tmp_sum])

        return output_str

    def get_password(self,whole):
        cipher = whole[:int(len(whole)/2)]#1st half of password is cipher
        password = whole[int(len(whole)/2):]
        cipher_num = []
        password_num = []
        output = []

        for i in range(len(cipher)):
            cipher_num.append(encoder.index(cipher[i]))
            password_num.append(encoder.index(password[i]))#gets pos from ciphertext

        for i in range(len(cipher)):
            tmp_sum = password_num[i] - cipher_num[i]
            if tmp_sum < 0:
                tmp_sum += len(alphabet)
            output.append(alphabet[tmp_sum])#decrypts ciphertext to plaintext

        return output

    def verify(self,string,password_input=[],state=False):
        del string[0]
        del string[-1]
        if state == False:
            if decode(string[0],"rot-13") == password_length[0]:#If theres no password
                del string[0]
                return self.decrypt(string)
            else:#if there is a password but user entered no
                return "Error - Password required."

        else:
            for key in password_length:
                if password_length[key] == decode(string[0],"rot-13"):
                    length = key
            del string[0]
            password = list(decode("".join(string[:length*2]),"rot-13"))#decodes rot-13 encryption

            if self.get_password(password) == password_input:#compares given password with actual
                del string[:length*2]#deletes password from string
                return self.decrypt(string)

            else:#user entered incorrect password
                return "Error - Incorrect password."
        
run_e = encrypt()
run_d = decrypt()

while True:#main loop
    try:
        print("\n<<<<<<<<<<OOOO>>>>>>>>>>")
        print("")
        which = str(input("Encrypt or Decrypt? - E/D: "))
        print("\n<<<<<<<<<<OOOO>>>>>>>>>>")
        if which == "E" or which == "e":
            message_e = str(input("\nEnter your message: "))
            while True:
                yes = input("\nDo you want a password? - Y/N: ")
                if yes == "Y" or yes == "y":
                    password = input("Enter a password: ")
                    print("\nOutput string:","".join(run_e.encrypt(list(message_e),list(password))))
                    break
                elif yes == "N" or yes == "n":
                    print("Output string:","".join(run_e.encrypt(list(message_e))))
                    break
                else:
                    print("Error.")
        elif which == "D" or which == "d":
            message_d = str(input("\nEnter encrypted message: "))
            while True:
                yes = input("\nIs this message password protected? - Y/N: ")
                if yes == "Y" or yes == "y":
                    password = input("Enter password: ")
                    print("\nOutput string:","".join(run_d.verify(list(message_d),list(password),True)))
                    break
                elif yes == "N" or yes == "n":
                    print("\nOutput string:","".join(run_d.verify(list(message_d))))
                    break
                else:
                    print("Error.")
        elif which == "q" or which == "Q":
            break
        else:
            print("\n",which,"is not a valid option.")
    except:
        if ValueError:
            print("\nSyntax Error.")
            print("Please check the alphabet/encoder for available characters.")
        elif MemoryError:
            print("\nError - Message is too large.")
            print("Please split up your message.")
        else:
            print("\nCode Error.")
