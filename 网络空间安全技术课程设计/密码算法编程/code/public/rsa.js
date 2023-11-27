// RSA 加密函数（异步版本）
async function rsaEncrypt(message, publicKey) {
  // 获取函数开始时间
  const startTime = Date.now();

  // 将公钥拆分为模数和指数
  const modulus = publicKey.modulus;
  const exponent = publicKey.exponent;

  // 将消息转换为 UTF-8 编码的字节序列
  const utf8Bytes = [];
  for (let i = 0; i < message.length; i++) {
    const charCode = message.charCodeAt(i);
    if (charCode < 128) {
      utf8Bytes.push(charCode);
    } else if (charCode < 2048) {
      utf8Bytes.push((charCode >> 6) | 192);
      utf8Bytes.push((charCode & 63) | 128);
    } else {
      utf8Bytes.push((charCode >> 12) | 224);
      utf8Bytes.push(((charCode >> 6) & 63) | 128);
      utf8Bytes.push((charCode & 63) | 128);
    }

    // 检查函数运行时间是否超过10秒
    const currentTime = Date.now();
    const elapsedTime = currentTime - startTime;
    if (elapsedTime > 10000) {
      return '加密操作超时';
    }
  }

  // 加密每个字节
  const encryptedBytes = utf8Bytes.map((byte) => {
    // 使用模指数运算进行加密
    let encryptedByte = BigInt(byte) ** BigInt(exponent) % BigInt(modulus);
    return encryptedByte.toString();
  });

  // 返回加密后的字符串数据
  return encryptedBytes.join(' ');
}


// RSA 解密函数（异步版本）
async function rsaDecrypt(encryptedMessage, privateKey) {
  // 获取函数开始时间
  const startTime = Date.now();

  // 将私钥拆分为模数和指数
  const modulus = privateKey.modulus;
  const exponent = privateKey.exponent;

  // 将加密后的数据拆分为每个字节的字符串数组
  const encryptedBytes = encryptedMessage.split(' ');

  // 解密每个字节
  const decryptedBytes = encryptedBytes.map((byte) => {
    // 使用模指数运算进行解密
    let decryptedByte = BigInt(byte) ** BigInt(exponent) % BigInt(modulus);
    return Number(decryptedByte);
  });

  // 将解密后的字节转换为 UTF-8 编码的字符串
  let decryptedMessage = '';
  let i = 0;
  while (i < decryptedBytes.length) {
    const byte = decryptedBytes[i];
    if (byte < 128) {
      decryptedMessage += String.fromCharCode(byte);
      i++;
    } else if (byte >= 192 && byte < 224) {
      const charCode = ((byte & 31) << 6) | (decryptedBytes[i + 1] & 63);
      decryptedMessage += String.fromCharCode(charCode);
      i += 2;
    } else if (byte >= 224 && byte < 240) {
      const charCode =
        ((byte & 15) << 12) |
        ((decryptedBytes[i + 1] & 63) << 6) |
        (decryptedBytes[i + 2] & 63);
      decryptedMessage += String.fromCharCode(charCode);
      i += 3;
    }

    // 检查函数运行时间是否超过10秒
    const currentTime = Date.now();
    const elapsedTime = currentTime - startTime;
    if (elapsedTime > 10000) {
      return '解密操作超时';
    }
  }

  // 返回解密后的字符串数据
  return decryptedMessage;
}
