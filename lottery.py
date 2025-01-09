import util
import requests
from web3 import Web3
import configparser
import ast

config = configparser.ConfigParser()
config.read('config.ini')
YOUR_INFURA_PROJECT_ID = config.get('API', 'YOUR_INFURA_PROJECT_ID')
COIN_TYPE= ast.literal_eval(config.get('CoinType','type'))
TIME=config.getint('Lottery','time')

#检查地址中是否有资产
def check_balance(address, coin):
    if coin == "BTC":
        try:
            response = requests.get(f"https://blockchain.info/rawaddr/{address}")
            if response.status_code == 200:
                data = response.json()
                balance = data.get("final_balance", 0) / 1e8
                print(f"Address: {address}, Balance: {balance} BTC")
                return balance
            else:
                print(f"Failed to fetch data for address {address}, Status Code: {response.status_code}")
                return 0
        except Exception as e:
            print(f"Error checking balance: {e}")
            return 0
    elif coin == "ETH":
        w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{YOUR_INFURA_PROJECT_ID}"))
        balance = w3.eth.get_balance(address) / 10 ** 18
        print(f"Address: {address}, Balance: {balance} ETH")
        return balance
    elif coin == "SOL":
        # 使用 Solana API 获取余额
        # 由于需要配置 Solana 节点,这里省略具体实现
        print(f"Address: {address}, Balance: {balance} SOL")
        return 100
    else:
        raise ValueError("Unsupported coin")
    

#通过助记词分别得到["BTC", "ETH", "SOL"]地址和私钥
def get_address_from_mnemonic(mnemonic_phrase,coin):
    if coin == "BTC":
        return util.generate_bitcoin_address()#比特币决定不通过助记词生成,而是随机生成
    elif coin == "ETH":
        return util.generate_eth_address(mnemonic_phrase)
    elif coin == "SOL":
        return util.generate_solana_address(mnemonic_phrase)
    else:
        raise ValueError("Unsupported coin")



def main():
    #随机生成助记词
    mnemonic_words = util.generate_mnemonic()
    print("Your 12 word mnemonic seed is:")
    print(mnemonic_words)
    # 依次检查["BTC", "ETH", "SOL"]地址中是否有资产
    print(COIN_TYPE,type(COIN_TYPE))
    for coin in COIN_TYPE:
        private_key,address = get_address_from_mnemonic(mnemonic_words,coin)
        balance=check_balance(address,coin)
        if balance > 0:
            print(f"🎉 Address {address} has {balance} {coin}!")
            print()
            print()
            print("mnemonic:",mnemonic_words)
            print("private_key:",private_key)
            print("address:",address)
            raise Exception("you motherfucker got money!!!!!!!!!!!!")
        else:
            print(f"No luck this time. Address {address} is empty.")
    
    print("----------------------------------------")


if __name__=="__main__":
    for i in range(1,TIME):
        main()
    
