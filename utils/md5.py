import hashlib
from wms.settings import SECRET_KEY

# md5加密，使用加盐策略，加的盐就是settings中的密钥
def encrypt(string):
    hash_object = hashlib.md5(SECRET_KEY.encode('utf-8'))
    hash_object.update(string.encode('utf-8'))
    return hash_object.hexdigest()
