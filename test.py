import  struct
def int_to_2_byte(value):
    def transform_data(value):  # transforms real value from 2 bytes
        iValue1 = value[0]
        iValue2 = value[1]
        ans = (((iValue2 & 0x7f) << 7) | (iValue1 & 0x7f))  # mask
        return ans
    RawByteValue = value.to_bytes(2,byteorder='big',signed=True)

    ans = transform_data(RawByteValue)
    return ans
def binary(num):
    packed = struct.pack('!f', num)
    #print('Packed: %s' % repr(packed))
    integers = [c for c in packed]
    #print('Integers: %s' % integers)
    binaries = [bin(i) for i in integers]
    #print('Binaries: %s' % binaries)
    stripped_binaries = [s.replace('0b', '') for s in binaries]
    #print('Stripped: %s' % stripped_binaries)
    padded = [s.rjust(8, '0') for s in stripped_binaries]
    #print('Padded: %s' % padded)
    return ''.join(padded)




def float_to_5_byte(value):
    b_array = bytearray(struct.pack("f", value))
    print(b_array)
    ans_array = bytearray()
    int_value = int.from_bytes(b_array,'little',signed=False)
    print(int_value)
    for i in range(5):
        ans_array.append(((int_value >> (7*i)) & 0x7f) | 0x80)
    return ans_array

def decrypt(k):
    def bitsToFloat(b):
        s = struct.pack('>l', b)
        return struct.unpack('>f', s)[0]
    res = 0
    for i in range(5):
        temp = k & 127 # Берём 7 бит
        k >>= 8 # Отбрасываем очередноё байт
        temp <<= 7*i # Сдвигаем число на 7 позиций вправо
        res += temp
    return bitsToFloat(res)


def makeBytes(BitString):
    def str_to_list(BitString):
        ReversedBitString = BitString[::-1]
        List = []
        i = 0
        for k in range(5):
            List.append((ReversedBitString[i: i + 7])[::-1])
            i += 7
        List[-1] = '000'+List[-1]
        return List

    def add_1_to_every_7_bits(list):
        ModdedList = list
        for i in range(len(ModdedList)):
            ModdedList[i] = '1'+ModdedList[i]
        if len(ModdedList) < 5:
            for i in range(5-len(ModdedList)):
                ModdedList.append('10000000')
        return ModdedList

    def list_to_bytes(list):
        byte_array = bytearray()
        for i in range(5):
            byte_array.append(int(list[i],2))
        return byte_array

    List = str_to_list(BitString)
    print(List)
    ModdedList = add_1_to_every_7_bits(List)
    print(ModdedList)
    Bytes = list_to_bytes(ModdedList)
    print(Bytes)




#print(int_to_2_byte(12))
a = 12.5
a = float_to_5_byte(a)
print(a)

#b = decrypt(a)
#print(b)
#print(binary(a))

#makeBytes(binary(12.5))

#print(binary(1))

def float_to_5_byte(value):
    def binary(num):
        packed = struct.pack('!f', num)
        # print('Packed: %s' % repr(packed))
        integers = [c for c in packed]
        # print('Integers: %s' % integers)
        binaries = [bin(i) for i in integers]
        # print('Binaries: %s' % binaries)
        stripped_binaries = [s.replace('0b', '') for s in binaries]
        # print('Stripped: %s' % stripped_binaries)
        padded = [s.rjust(8, '0') for s in stripped_binaries]
        # print('Padded: %s' % padded)
        return ''.join(padded)

    Value = value

    def transform_data(value):

        def make_bytes(BitString):
            def str_to_list(BitString):
                ReversedBitString = BitString[::-1]
                List = []
                i = 0
                for k in range(5):
                    List.append((ReversedBitString[i: i + 7])[::-1])
                    i += 7
                List[-1] = '000' + List[-1]  # add zeros to form valid 7-bit byte
                return List

            def add_1_to_every_7_bits(list):
                ModdedList = list
                for i in range(len(ModdedList)):
                    ModdedList[i] = '1' + ModdedList[i]  # add 1 first bit to every byte
                if len(ModdedList) < 5:
                    for i in range(5 - len(ModdedList)):
                        ModdedList.append('10000000')
                return ModdedList

            def list_to_bytes(list):
                byte_array = bytearray()
                for i in range(5):
                    byte_array.append(int(list[i], 2))
                return byte_array

            List = str_to_list(BitString)
            # print(List)
            ModdedList = add_1_to_every_7_bits(List)
            # print(ModdedList)
            Bytes = list_to_bytes(ModdedList)
            # print(Bytes)
            return Bytes

        a = binary(value)
        a = make_bytes(a)
        return a

    return transform_data(Value)