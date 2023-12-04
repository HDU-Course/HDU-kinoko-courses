def ex_gcd(a, b):
    """
    扩展欧几里得算法，计算私钥的指数d
    返回两个整数s和t，满足s * a + t * b = gcd(a, b)
    """
    if b == 0:
        return 1, 0
    # 计算商和余数
    q, r = divmod(a, b)
    # 递归调用，返回值s和t满足s * b + t * r = gcd(b, r)
    s, t = ex_gcd(b, r)
    # a 和 b 的最大公约数的线性表示。
    return t, s - q * t

def fast_expmod(a, e, n):
    """
    快速模幂运算，用于加密和解密过程中的数值计算
    计算 a^e mod n 的结果
    """
    d = 1
    while e != 0:
        if e & 1:
            d = (d * a) % n
        e >>= 1
        a = (a * a) % n
    return d

def make_key(p, q, e):
    """
    生成RSA的公钥和私钥
    输入：两个大素数p和q，以及公钥指数e
    输出：公钥[n, e]和私钥[n, d]
    """
    n = p * q
    fin = (p - 1) * (q - 1)
    d = ex_gcd(e, fin)[0]
    d = d % fin if d < 0 else d
    return [[n, e], [n, d]]

def encryption(key, data):
    """
    RSA加密算法，用公钥加密明文
    输入：公钥[key]和明文[data]
    输出：密文列表
    """
    n, e = key
    ciphertext = [fast_expmod(ord(item), e, n) for item in data]
    return ciphertext

def decrypt(key, ciphertext):
    """
    RSA解密算法，用私钥解密密文
    输入：私钥[key]和密文列表[ciphertext]
    输出：原始的明文字符串
    """
    n, d = key
    plaintext = ''.join(chr(fast_expmod(item, d, n)) for item in ciphertext)
    return plaintext

def make_p_q_e():
    """
    生成大素数p、q和公钥指数e
    输出：大素数p、q和公钥指数e
    """
    p = 33478071698956898786044169848212690817704794983713768568912431388982883793878002287614711652531743087737814467999489
    q = 36746043666799590428244633799627952632279158164343087642676032283815739666511279233373417143396810270092798736308917
    e = 65537
    return p, q, e