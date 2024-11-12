import random
def xor_encrypt_decrypt(data, key):
    return ''.join(chr(ord(c) ^ key) for c in data)
def simple_permutation(data, perm):
    return ''.join(data[i] for i in perm)
def insert_chars(data, chars):
    mixed = list(data)
    for char in chars:
        position = random.randint(0, len(mixed))
        mixed.insert(position, char)
    return ''.join(mixed)
def swap_positions(data, swap_indices):
    data_list = list(data)
    for idx1, idx2 in swap_indices:
        data_list[idx1], data_list[idx2] = data_list[idx2], data_list[idx1]
    return ''.join(data_list)
def encrypt(plain_text, key, insert_chars_list):
    xor_encrypted = xor_encrypt_decrypt(plain_text, key)
    mixed_text = insert_chars(xor_encrypted, insert_chars_list)
    swap_indices = [(0, 1), (2, 3)]
    swapped_text = swap_positions(mixed_text, swap_indices)
    permutation = list(range(len(swapped_text)))
    random.shuffle(permutation)
    permuted_text = simple_permutation(swapped_text, permutation)
    permuted_text = permuted_text.replace('"', '?')
    return permuted_text, swap_indices, permutation
def encrypt_aws(plain_text, key, insert_chars_list="xyyuyyyui"):
    xor_encrypted = xor_encrypt_decrypt(plain_text, key)
    mixed_text = insert_chars(xor_encrypted, insert_chars_list)
    swap_indices = [(0, 1), (2, 3)]
    swapped_text = swap_positions(mixed_text, swap_indices)
    permutation = [18, 21, 1, 25, 27, 8, 19, 12, 16, 22, 10, 7, 3, 11, 4, 24, 15, 20, 23, 13, 2, 26, 17, 14, 28, 0, 6, 5, 9]
    permuted_text = simple_permutation(swapped_text, permutation)
    permuted_text = permuted_text.replace('"', '?')
    return permuted_text, swap_indices, permutation
def encrypt_ec2(plain_text, key, insert_chars_list="xyyuyyyui"):
    xor_encrypted = xor_encrypt_decrypt(plain_text, key)
    mixed_text = insert_chars(xor_encrypted, insert_chars_list)
    swap_indices = [(0, 1), (2, 3)]
    swapped_text = swap_positions(mixed_text, swap_indices)
    permutation = [7, 28, 1, 26, 0, 9, 23, 6, 10, 25, 24, 20, 3, 21, 18, 5, 27, 15, 8, 4, 2, 11, 12, 22, 19, 17, 16, 14, 13]
    permuted_text = simple_permutation(swapped_text, permutation)
    permuted_text = permuted_text.replace('"', '?')
    return permuted_text, swap_indices, permutation
def decrypt(encrypted_text, key, swap_indices, permutation, insert_chars_list):
    reverse_permutation = sorted(range(len(permutation)), key=lambda x: permutation[x])
    permuted_text = simple_permutation(encrypted_text, reverse_permutation)
    swapped_text = swap_positions(permuted_text, swap_indices)
    for char in insert_chars_list:
        swapped_text = swapped_text.replace(char, '', 1)
    decrypted = xor_encrypt_decrypt(swapped_text, key)
    return decrypted
def decrypt_new(encrypted_text, key, swap_indices, permutation, insert_chars_list):
    encrypted_text = encrypted_text.replace('?', '"')
    reverse_permutation = sorted(range(len(permutation)), key=lambda x: permutation[x])
    permuted_text = simple_permutation(encrypted_text, reverse_permutation)
    swapped_text = swap_positions(permuted_text, swap_indices)
    for char in insert_chars_list:
        swapped_text = swapped_text.replace(char, '', 1)
    decrypted = xor_encrypt_decrypt(swapped_text, key)
    return decrypted
if __name__ == "__main__":
    original_message = "*"
    key = 123
    insert_chars_list = "xyyuyyyui"
    print("Original Message:", original_message)
    encrypted_message, swap_indices, permutation = encrypt(original_message, key, insert_chars_list)
    print("Encrypted Message:", encrypted_message)
    print(swap_indices,permutation)
    decrypted_message = decrypt_new("?y:LN1*,y#-02y:iyHx)u9?#y0?#u", key, [(0, 1), (2, 3)], [18, 21, 1, 25, 27, 8, 19, 12, 16, 22, 10, 7, 3, 11, 4, 24, 15, 20, 23, 13, 2, 26, 17, 14, 28, 0, 6, 5, 9], insert_chars_list)
    print("Decrypted Message:", decrypted_message)