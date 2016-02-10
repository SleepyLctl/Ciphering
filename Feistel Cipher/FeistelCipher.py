__author__ = 'peetp'

import math
import random

class Feistel(object):
    def __init__(self, mode, inputtext, nrounds):

        self.n_prime_numbers_CONST = 400
        self.block_size_CONST = 256
        self.keySize_CONST = 128
        self.nRounds_CONST = nrounds
        self.inputText_CONST = inputtext

        self.primelist = ()
        self.random_bit_key = []
        self.nonEditText = ''
        self.Lx = ''
        self.Rx = ''
        self.encoded_message = []
        self.subkeys = []
        self.key = ''
        self.binaryList = []
        self.init_permutation_table_CONST = \
            [16, 94, 70, 121, 122, 98, 39,
             86, 40, 41, 76, 20, 123, 118, 116,
             79, 38, 84, 75, 67, 90, 104, 91, 27,
             65, 78, 82, 102, 21, 64, 83,
             45, 114, 97, 74, 120, 5, 69, 117,
             32, 52, 30, 43, 63, 48, 17, 37,
             26, 14, 119, 2, 103, 33, 59,
             100, 109, 51, 85, 127, 125, 113, 28, 6,
             110, 81, 42, 101, 50, 15, 7, 34, 95, 0, 19, 35, 80, 29,
             105, 126, 71, 9, 56, 66,
             107, 31, 36, 92, 3, 72, 4, 60, 23, 12, 13, 24,
             87, 89, 47, 112, 11, 77, 8, 108,
             88, 49, 54, 61, 68, 53, 96, 10, 1, 93,
             58, 124, 62, 22, 57,
             44, 111, 25, 46, 55, 99, 115, 73, 106, 18]

        self.substution = []
        if (mode == 'D'):
            decoded_output = []
            self.key = input('Insert binary key >>>')
            decoded_output = self.switching(self.key, self.nRounds_CONST, self.block_size_CONST, self.inputText_CONST)
            print('Decoded message\n>>> '+ self.to_ascii(''.join(decoded_output)))
            input('Enter to exit')


        elif (mode == 'E'):
            binary_plaintext = self.stringtify(self.inputText_CONST)
            self.primelist = self.prime_gen()
            self.key = self.blum_blum_shub_gen()
            self.switching(self.key, self.nRounds_CONST, self.block_size_CONST, binary_plaintext)

    def to_ascii(self, binary_plaintext):
        #
        #Convert BINARY text to ASCII
        #
        return ''.join(chr(int(binary_plaintext[i:i+8], 2)) for i in range(0, len(binary_plaintext), 8))


    def formatText(self, nonedittext):
        #
        #Just some formating, removing some chars
        #
        self.nonEditText = nonedittext.translate(
            {ord(' '): '', ord(','): '', ord('.'): '', ord('?'): '', ord('!'): '', ord('\n'): ''})

        print('\
        \nText to process:\n>>> ' + self.inputText_CONST + '\
        \nNumber of Chars:\n>>> ' + str(len(self.inputText_CONST)) + '\
        \n\n>>> Removing whitespaces')

    def asciiToBin(self, character):
        #
        #Convert ASCII to BINARY
        #
        binarychar = bin(ord(character))
        binarychar = binarychar.replace('0b', '')
        binarychar = binarychar.rjust(8, '0')
        return binarychar

    def stringtify(self, string):
        #
        #Making some strings for next precedures
        #
        binaryString = ''

        for c in string:
            binaryString += self.asciiToBin(c)

        print('Binary: ' + binaryString)
        print('Text:   ' + self.nonEditText)
        return binaryString

    def block_maker(self, binaryPlaintext, blockSize):
        #
        #Creating blocks from single array of bits.
        #
        # ceil the number up
        nBlock = math.ceil(len(binaryPlaintext) / blockSize)
        print("\nBinary plaintext : Blocksize ratio\n>>> " + str(
            len(binaryPlaintext) / blockSize) + '\nBlocks to create\n>>> ' + str(nBlock) + '\n')

        # parsing binary number to blocks of "block size" width
        self.binaryList = [binaryPlaintext[i:i + blockSize] for i in range(0, len(binaryPlaintext), blockSize)]

        for i in self.binaryList:
            smallerblock = 0
            if len(str(i)) < blockSize:
                smallerblock = blockSize - len(i)
                i = str(i.rjust(blockSize, "0"))

            print('BlockSize >>> ' + str(len(i)) + ' Justified by >>> ' + str(smallerblock))

        return self.binaryList

    def makeRxLx(self, binaryBlock):
        #
        #Dividing previously created block on halves -> lx, rx
        #
        lx = (
            str(binaryBlock[0:int(self.block_size_CONST / 2)]).rjust(int(self.block_size_CONST / 2), '0'))
        rx = (
            str(binaryBlock[int(self.block_size_CONST / 2):self.block_size_CONST]).rjust(int(self.block_size_CONST / 2),
                                                                                         '0'))

        return (lx, rx)

    def prime_gen(self):
        #
        # Create array of n huge primes
        #
        print('\nPrime number generator' +
              '\n######################' +
              '\n>>> Generating tons of prime numbers!')
        primes = []
        n_prime_numbers = 0
        while True:
            p = random.randrange(100001, 10000000, 2)
            if all(p % n != 0 and p % 4 == 3 for n in range(3, int((p ** 0.5) + 1), 2)):
                primes.append(p)
                n_prime_numbers += 1

                if n_prime_numbers == self.n_prime_numbers_CONST:
                    print('>>> Created ' + str(len(primes)) + ' prime numbers')
                    break
        return primes

    def blum_blum_shub_gen(self):
        #
        #Generate M which depends on previously calculated primes
        #Used for creation of main key, which is used as round key as well
        #
        print('\n>>> Blum Blum Shub pseudo-random generator' +
              '\n##########################################' +
              '\n>>> X(i) = X(i-i)pow(2) mod N')
        p = self.primelist.pop(random.randrange(0, len(self.primelist)))
        q = self.primelist.pop(random.randrange(0, len(self.primelist)))
        n = p * q

        print('>>> Generating M number\n>>> p = ' + str(p) + ' q = ' + str(q) + '\n>>> N = p * q = ' + str(n))

        #
        # Getting X
        #
        xi_minus_one = self.primelist.pop(random.randrange(0, len(self.primelist)))

        #
        # First X(i)
        #
        for i in range(0, self.keySize_CONST):
            p = self.primelist.pop(random.randrange(0, len(self.primelist)))
            q = self.primelist.pop(random.randrange(0, len(self.primelist)))
            n = p * q
            xi = (xi_minus_one ** 2) % n
            binnumber = str(bin(xi))
            self.random_bit_key.append(binnumber[len(binnumber) - 1])
            xi_minus_one = xi

        print('##########################################' +
              '\n\nNew ' + str(self.keySize_CONST) + '-bit key generated\n>>>\t' + ''.join(self.random_bit_key))
        return self.random_bit_key


    def init_permutation(self, block128):
        #
        #Permutation depending on static permutatiton table
        #
        permuted_block = []

        for x in range(0, len(block128)):
            permuted_block.append(block128[self.init_permutation_table_CONST[x]])

        return ''.join(permuted_block)

    def xor_it(self, binary_a, binary_b):
        #
        #Simple XOR with converting to array before.
        #
        a_arr = []
        b_arr = []
        for i in range(0, len(binary_a)):
            a_arr.append(binary_a[i])
            b_arr.append(binary_b[i])

        xor = [ord(a) ^ ord(b) for a, b in zip(a_arr, b_arr)]
        return str(xor)

    def make_it_clean(self, string):
        #
        #Just formating
        #
        string = str(string)
        return string.translate({ord(' '): '', ord(','): '', ord('['): '', ord(']'): '', ord('\''): '', ord('"'): ''})

    def magic_function(self, Rx, Key):
        #
        #Function of Feistel cipher. There is permutation and XORing with key
        #
        # permutation
        permutation = self.init_permutation(Rx)

        # XORing with KEY
        key_xored = self.make_it_clean(''.join(self.xor_it(permutation, Key)))
        return key_xored

    def switching(self, Key, nRounds_CONST, block_size_CONST, binary_plaintext):
        #
        #Main part of Feistel cipher. Switching of Lx, Rx + XORing
        #
        self.block_maker(binary_plaintext, block_size_CONST)
        print("\nSwitching...")

        for block in range(0, len(self.binaryList)):
            lx, rx = self.makeRxLx(self.binaryList[block])

            key = ''.join(Key)

            for x in range(0, nRounds_CONST):
                foo = rx
                functioned_rx = self.magic_function(rx, key)
                rx = self.make_it_clean(''.join(self.xor_it(lx, functioned_rx)))
                lx = foo

            foo = rx
            rx = lx
            lx = foo

            self.encoded_message.append(str(lx) + str(rx))

        print('>>> Switched ' + str(self.nRounds_CONST) + ' times')
        print('\nCiphering 128-bit key \n>>> ' + ''.join(key))

        print('Message\n>>> ' + ''.join(self.encoded_message))
        input('Enter to continue')
        return self.encoded_message



########################################################################################################################
choice = input('[E]ncode or [D]ecode >>> ')
inputText = input('Input >>> ')
leMachine = Feistel(choice, inputText, 16)
