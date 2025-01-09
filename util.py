import os
import base58
import ecdsa
import hashlib
from eth_account import Account
from solders.keypair import Keypair 
from mnemonic import Mnemonic
from bip_utils import Bip39MnemonicGenerator,Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

# 启用未审计的助记词功能
Account.enable_unaudited_hdwallet_features()


#随机生成一个 BTC 私钥和地址
def generate_bitcoin_address():
    # 1. 生成随机私钥
    private_key = os.urandom(32)

    # 2. 计算公钥
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key = b'\x04' + vk.to_string()

    # 3. 计算地址 比特币地址编码方式有两种:Base58Check、Bech32,
    # 即同一个私钥可根据不同的编码得到不同的地址，但是在只知道地址的前提下，不同编码下的地址无法相互转换
    # 不过，这些地址只对应一个私钥，因此是一个账户
    sha256_hash = hashlib.sha256(public_key).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    version = b'\x00'
    checksum = hashlib.sha256(hashlib.sha256(version + ripemd160_hash).digest()).digest()[:4]
    bitcoin_address = base58.b58encode(version + ripemd160_hash + checksum).decode('utf-8')

    print(f"Bitcoin Private Key: {private_key.hex()}")
    print(f"Bitcoin Address: {bitcoin_address}")
    return private_key.hex(), bitcoin_address

#随机生成助记词 默认12位 可修改
def generate_mnemonic(num=12):
    return Bip39MnemonicGenerator().FromWordsNumber(num).ToStr()

#传入助记词得到 ETH 的地址
def generate_eth_address(mnemonic_phrase):
    # 验证助记词的有效性
    mnemo = Mnemonic("english")
    if not mnemo.check(mnemonic_phrase):
        raise ValueError("Invalid mnemonic phrase")

    # 通过助记词生成种子
    seed = Bip39SeedGenerator(mnemonic_phrase).Generate()

    # 使用 Bip44 生成以太坊账户
    bip44_eth_ctx = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    bip44_acc = bip44_eth_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)

    # 获取私钥
    private_key = bip44_acc.PrivateKey().Raw().ToHex()

    # 创建账户对象
    account = Account.from_key(private_key)
    # 输出以太坊地址和私钥
    print(f"ETH Private Key: {private_key}")
    print(f"ETH Address: {account._address}")
    
    
    return private_key,account.address

#传入助记词得到 SOL 的地址
def generate_solana_address(mnemonic_phrase):
    # 验证助记词的有效性
    mnemo = Mnemonic("english")
    if not mnemo.check(mnemonic_phrase):
        raise ValueError("Invalid mnemonic phrase")
    
    # 通过助记词生成种子
    try:
        seed = Bip39SeedGenerator(mnemonic_phrase).Generate()
    except ValueError:
        raise ValueError("Invalid mnemonic phrase")

    # 使用 Bip44 生成 Solana 账户
    bip44_mst_ctx = Bip44.FromSeed(seed, Bip44Coins.SOLANA)
    bip44_acc = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT) 

    # 获取私钥和地址
    private_key = bip44_acc.PrivateKey().Raw()
    keypair = Keypair.from_seed(private_key.ToBytes())
    address = keypair.pubkey().__str__()

    print(f"SOL Private Key: {private_key.ToHex()}")
    print(f"SOL Address: {address}")
    return private_key.ToHex(),address



if __name__=="__main__":

    #随机生成助记词
    mnemonic_words = generate_mnemonic()
    print("Your 12 word mnemonic seed is:")
    print(mnemonic_words)
    #得到 BitCoin、ETH、SOL的私钥和地址
    generate_bitcoin_address()
    generate_eth_address(mnemonic_words)
    generate_solana_address(mnemonic_words)















