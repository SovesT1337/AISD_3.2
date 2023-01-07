import math
import fileinput


class BloomFilter:
    def __init__(self):
        self.__data = None
        self.__size = 0
        self.__hash_n = 0
        self.__primes = [2, 3]

    def update_primes(self, n):
        number = self.__primes[-1]
        while len(self.__primes) < n:
            number += 2
            for i in self.__primes:
                if number % i or i > math.ceil(number ** 0.5):
                    break
            self.__primes.append(number)

    def __hash_i(self, i, x) -> int:
        return (((i + 1) * x + self.__primes[i]) % 2147483647) % self.__size

    def initialize(self, n, p):
        if not self.__hash_n < 1:
            raise Exception('already exists')
        if n < 1:
            raise Exception('bad input n')
        if not 0 < p < 1:
            raise Exception('bad input p')
        self.__size = round(-n * math.log2(p) / math.log(2))
        self.__data = bytearray(math.ceil(self.__size / 8))
        self.__hash_n = round(-math.log2(p))
        if self.__hash_n < 1:
            raise Exception('no hash')
        self.update_primes(self.__hash_n)

    def add(self, x):
        if self.__hash_n < 1:
            raise Exception('not initialized')
        for i in range(self.__hash_n):
            hash = self.__hash_i(i, x)
            if hash >= self.__size:
                raise Exception('BitArray out of range')
            byte = hash // 8
            hash -= byte * 8
            self.__data[byte] |= (1 << hash)

    def search(self, x) -> bool:
        if self.__hash_n < 1:
            raise Exception('not initialized')
        for i in range(self.__hash_n):
            hash = self.__hash_i(i, x)
            if hash >= self.__size:
                raise Exception('BitArray out of range')
            byte = hash // 8
            hash -= byte * 8
            if (self.__data[byte] & (1 << hash)) >> hash != 1:
                return False
        return True

    def get_m(self):
        return self.__size

    def get_k(self):
        return self.__hash_n

    def to_print(self):
        s, rest = '', self.__size
        for byte in self.__data:
            s += bin(byte)[2:].zfill(8 if rest >= 8 else rest)[::-1]
            rest -= 8
        return s


if __name__ == '__main__':
    bf = BloomFilter()
    for line in fileinput.input():
        try:
            s = line.strip().split(' ')
            if s[0] == "set" and s[1] and s[2]:
                bf.initialize(int(s[1]), float(s[2]))
                print(bf.get_m(), bf.get_k())
                continue
            if s[0] == "add" and s[1]:
                bf.add(int(s[1]))
                continue
            if s[0] == "search" and s[1]:
                status = bf.search(int(s[1]))
                print('1' if status else '0')
                continue
            if s[0] == "print":
                str = bf.to_print()
                print('error' if not str else str)
                continue
            print('error')
        except Exception:
            print('error')
