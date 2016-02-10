import math
import time
from random import randrange

__author__ = 'peetp'


#Created on 15 OCT 2015
#@author: Petr Pospisil


class RSA():
    # My implementation of RSA cipher
    # Just for study purposes

    def __init__(self, INPUT, mode, magic_shift):
        self.alphabet_convert_table =  ['Q','G','E','R','T','S','U','.','O','L','K','J','H','F',' ',
                                        'D','P','W','X','C','!','I','Y','M','V','Z','/',';','B','[',
                                        ']','N','-','0','9','A','7','6','5','4','3','2','1',',','?','8']

        block_size = 4
        self.magic_shift = magic_shift

        if mode == '1':
            big_chars = str(INPUT).upper()
            numbers_array = self.character_decoder(big_chars)
            blocks_array = self.block_maker(numbers_array, block_size)
            print(blocks_array)

            prime_array = self.prime_gen()
            p, q, n = self.n_calculation(prime_array)
            fi = self.fi_calculation(p, q)
            e = self.find_e(fi)
            d = self.d_calculation(e, fi)
            self.show_keys(d, e, n)
            shrinked_blocks = self.shrink_it(blocks_array, block_size)
            print('Shrinked >>> ' + str(shrinked_blocks))
            print('Ciphered >>> ' + str(self.encrypt_it(shrinked_blocks, e, n)))

        else:
            d = input('d >>> ')
            n = input('n >>> ')
            number_blocks = self.slice_input(INPUT)
            decyphered = self.decrypt_it(number_blocks, int(d), int(n))
            print('Deciphered to assemble\n>>> ' + str(decyphered))
            print('Readable text\n>>> ' + ''.join(self.unshrink(decyphered, block_size)))

    def prime_gen(self):
        # Returns array of n huge primes
        # Used from Assign. #1, not bad, but for bigger blocks needed better one. Primes are approx. 100bits big.

        print('\nPrime number generator' +
              '\n######################' +
              '\n>>> Generating tons of prime numbers!')
        start = time.time()
        primes = []
        counter = 0
        while True:
            p = randrange(1000000000000001, 10000000000000001, 2)
            if all(p % n != 0 and p % 4 == 3 for n in range(3, int((p ** 0.5) + 1), 2)):
                primes.append(p)
                counter += 1

                if counter == 2:
                    print('>>> Created ' + str(len(primes)) + ' prime numbers')
                    break

        end = time.time()
        print('Elapsed time\n>>> ' + str(end - start))
        return primes

    def n_calculation(self, primes_array):
        # Return p,q,n numbers
        # Just some basics params of RSA ciphering.
        # n = p * q

        p = 0
        q = 0
        n = 0

        p = primes_array.pop(randrange(0, len(primes_array)))
        q = primes_array.pop(randrange(0, len(primes_array)))
        n = p * q

        print(
            '\nN number calculation' +
            '\n######################' +
            '\n>>> p = ' + str(p) + ', q = ' + str(q) +
            '\n>>> p * q = n' +
            '\n>>> n = ' + str(n) + ' => ' + str(int(n).bit_length()) + ' bits')

        return p, q, n

    def egcd(self, a, b):
        # For better perfomance used editted algorithm
        # from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
        # Extended Euclid Algorithm
        # used for finding E
        # return egcd

        x, y, u, v = 0, 1, 1, 0
        while a != 0:
            q, r = b // a, b % a
            m, n = x - u * q, y - v * q
            b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
        return gcd

    def find_e(self, fi):
        # Finding e for ciphering with egcd() function above
        # Pick E vaue from suggested values or pick whatever else by your choice.
        # returns e

        e_array = []
        ret_arr = []
        for x in range(3, 50):
            is_coprime = self.egcd(fi, x)
            if (is_coprime == 1):
                e_array.append(x)

        for x in range(0, 5):
            ret_arr.append(e_array.pop(randrange(0, len(e_array))))

        print('\nPick \'E\' - public key' +
              '\n######################' +
              '\nSome suggested E values\n>>> ' + str(ret_arr))

        e = input('Pick the your E >>> ')
        e = int(e)

        return e

    def fi_calculation(self, p, q):

        # easy calculation of phi,
        # fi = p_minus * q_minus
        # return phi

        p_minus = p - 1
        q_minus = q - 1

        fi = p_minus * q_minus

        print(
            '\nFi number calculation' +
            '\n######################' +
            '\n>>> (p - 1) = ' + str(p_minus) + ', (q - 1) = ' + str(q_minus) +
            '\n>>> (p - 1) * (q - 1) = fi' +
            '\n>>> fi = ' + str(fi))

        return fi

    def inverse(self, x, m):

        # returns inverse EGCD

        a, b, u = 0, m, 1
        while x > 0:
            q = b // x  
            x, a, b, u = b % x, u, x, a - q * u
        if b == 1:
            return a % m
        else:
            print("must be coprime")

    def d_calculation(self, e, fi):

        # calculation of D based on inverse function above
        # checking if its right.
        # D = e * mod fi = 1
        # returns D

        d = self.inverse(e, fi)
        check = e * d % fi

        print(
            '\nD number calculation' +
            '\n######################' +
            '\n>>> e = ' + str(e) + ' fi = ' + str(fi) +
            '\n>>> d = ' + str(d) +
            '\n>>> Let\' check it'
            '\n>>> d = e * d mod fi has to be 1.0 ...' +
            '\n>>> ' + str(e) + ' * ' + str(d) + ' mod ' + str(fi) + ' = ' + str(check) + ' => d is OK')

        return d

    def show_keys(self, d, e, n):

        # returns d, e, n in beautiful format

        print(
            '\nKeys show up' +
            '\n######################')
        print('>>> Private key: {d: ' + '{ ' + str(d) + ' n: ' + str(n) + ' }')
        print('>>> Public key:  {e: { ' + str(e) + ' n: ' + str(n) + ' }')

        return d, e, n

    def character_decoder(self, plaintext):
        # converts CHARs to INTEGER
        # shifts letters by certain numbers
        # returns array of shifted numbers

        numbers_array = []
        for character in plaintext:
            numbers_array.append(self.alphabet_convert_table.index(character))

        for i in range(0, len(numbers_array)):
            numbers_array[i] += self.magic_shift

        return numbers_array

    def block_maker(self, numbers_array, block_size):
        # from Assign #1
        # calculate how many blocks are needed
        # parse array of numbers to blocks
        # returns array of blocks

        nBlock = math.ceil(len(numbers_array) / block_size)

        print(
            '\nBlock Maker' +
            '\n######################' +
            '\nBinary plaintext : Blocksize ratio' +
            '\n>>> ' + str(len(numbers_array) / block_size) +
            '\nBlocks to create\n>>> ' + str(nBlock) + '\nBlocks')

        # parsing binary number to blocks of "block size" width
        blocks = [numbers_array[i:i + block_size] for i in range(0, len(numbers_array), block_size)]

        while (len(blocks[len(blocks) - 1]) != block_size):
            blocks[len(blocks) - 1].append(self.alphabet_convert_table.index('X') + self.magic_shift)

        return blocks

    def encrypt_it(self, blocks, e, n):
        # encrypting blocks
        # because of small e and small blocks, not hard to calculate.
        # for better perfomance:
        #	> instead of ** use function ipow()
        #	> or even better function modpow() - combination of pow and mod ...
        #	... (skipping saving-to-variables time and skipping 2 diffic. operations(pow + mod) instead of only one easy (mod and pow in one function))
        # I'm aware of mistakes in this function, keeping it like that for study purposes

        ciphered_blocks = []
        for number in blocks:
            pow_ed = int(number) ** e
            # pow_ed = self.ipow(number, e)

            foo = pow_ed % n
            ciphered_blocks.append(foo)
        # print(ciphered_blocks)
        return ciphered_blocks

    def pairing(self, a, b):
        # GOOD IDEA, BAD RESOULT :] Particularly proud of me, even it wasn't good idea at the end.
        # Implementation of Math Pairing function for merging numbers in blocks
        # Taking 2 INTEGERS and returns one merged INTEGER
        # Actually good idea, I was googling for some solution how to merge integers
        # quite long time. Then I implemented this sollution...
        # ...unfortunally, I didn't expect HUGE rise of merged integer. ...
        # ...So when I was trying to merge block of 8 numbers, resoult ...
        # ...was such huge number, I wasnt able to cipher it anymore with primes available from generator.
        # Maximum of merged numbers - 4-6 INTEGERS, then is numbers huge (+- 10exp150 ??)
        # Because of this function I'm not able to cipher blocks bigger then 4 INTEGERS
        # Solution... Just next time dont try to work with INTEGERS, and keep working with binary numbers.
        # Convert text to binary form instead of integers.

        return ((a + b) * (a + b + 1)) / 2 + b;

    def unpair(self, c):
        # recovering numbers from pairing function
	    # require INTEGER returns 2 INTEGERS, one original number, one merged for another unpairing.

        t = math.floor((-1.0 + math.sqrt(1.0 + 8.0 * c)) / 2.0)
        x = t * (t + 3) / 2 - c
        y = c - t * (t + 1) / 2
        return x, y

    def shrink_it(self, blocks, block_size):
        # just using pairing function

        shrinked_blocks = []

        for block in blocks:
            temp = block[0]
            for x in range(0, len(block) - 1):
                temp = self.pairing(temp, block[x + 1])

            shrinked_numbers = temp

            shrinked_blocks.append(int(shrinked_numbers))
        return shrinked_blocks

    def ipow(self, base, exp):
        # Cryptographic pow
        # I was looking for solution how to decrypt ciphered text quite long time. It was tooking my computer more
        # then 10 minutes from the begin and most of times
        # it ended with crash. Then I realized that only way how to decrypt message is to merge
        # pow and mod together - function modpow(). Keeping this function for future use.

        result = 1
        while (exp != 0):
            if ((exp & 1) != 0):
                result *= base
            exp >>= 1
            base *= base
        return result

    def modpow(self, base, exp, modulus):
        # combination od mod and pow
        # only way how to deal with huge numbers like RSA cipher.
        # inpirated by solution on StackOverflow, after one day of trying to use libraries like math.pow etc. ...
        # ...I gave up. Did not realize that 100000000000 pow 1000000 is basically load for months.

        base %= modulus
        result = 1
        while (exp > 0):
            if (exp & 1):
                result = (result * base) % modulus

            base = (base * base) % modulus
            exp >>= 1
        return result

    def decrypt_it(self, blocks, d, n):
        # just practical use of modpow and returning of deciphered but still merged number.

        decyphered_blocks = []
        for block in blocks:
            decyphered_blocks.append(self.modpow(int(block), d, n))
        return decyphered_blocks

    def unshrink(self, blocks, blocksize):
        # Require deciphered, merged number
        # From one INTEGER recovers rest of numebers - pairing/unpairing function more above.
        # returns array of numbers.

        to_alphabet = []

        for number in blocks:
            decoded = []

            dumb, b = self.unpair(number)
            decoded.append(b)
            for x in range(0, blocksize - 1):

                if (x == blocksize - 2):
                    decoded.append(dumb)
                else:
                    dumb, b = self.unpair(dumb)
                    decoded.append(b)

            for number in decoded[::-1]:
                to_alphabet.append(self.alphabet_convert_table[int(number - self.magic_shift)])

        return to_alphabet

    def slice_input(self, INPUT):
        # Just formating stuff for deciphering INPUT
	    # From input are deleted any letters which are not numbers, and ','
	    # returns clean array of ciphered blocks ready to decipher

        formated = ''.join(i for i in INPUT if i.isdigit() or (i == ','))
        result = formated.split(',')
        return result


INPUT = input('Input >>> ')
mode = input('Encrypt[1], Decrypt[0] >>> ')

test = RSA(INPUT, mode, 23)
