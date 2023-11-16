import hashlib
from ff3 import FF3Cipher
import geohash2

def hash_tweak(ccn):
    ccn_str = str(ccn)
    ccn_bytes = ccn_str.encode('utf-8')
    tweak = hashlib.sha256(ccn_bytes[:6] + ccn_bytes[-4:]).digest()[:8]
    tweak_hex = tweak.hex()
    return tweak_hex


def encrypt_cc_num(ccn):
    key = "2DE79D232DF5585D68CE47882AE256D6"
    tweak=hash_tweak(ccn)
    c = FF3Cipher(key, tweak)
    plaintext_str = str(ccn) # Convert to string
    ciphertext = c.encrypt(plaintext_str)
    return ciphertext

def encrypt_merchant(plaintext):
    key = "2DE79D232DF5585D68CE47882AE256D6"
    tweak = "A8E7920AFA330A73"
    c = FF3Cipher(key, tweak, radix=62)
    #plaintext_str = str(plaintext)
    final_text = ""
    for char in plaintext:
        if char.isalnum():
            final_text += char
    ciphertext = c.encrypt(final_text)
    return ciphertext

# Function to encode latitude and longitude into geohash
def encode_geohash(latitude, longitude, precision = 9):
    return geohash2.encode(latitude, longitude, precision)