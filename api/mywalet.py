from bipwallet import wallet
import requests
# generate 12 word mnemonic seed
# seed = wallet.generate_mnemonic()

# print(seed)


from bipwallet.utils import *

def gen_address(index):
    # Наша seed фраза
    seed = 'will coach exercise defense pistol drive round bronze toddler exit clean anxiety'

    # Мастер ключ из seed фразы
    master_key = HDPrivateKey.master_key_from_mnemonic(seed)

    # Public key из мастер ключа по пути 'm/44/0/0/0'
    root_keys = HDKey.from_path(master_key, "m/44'/0'/0'/0")[-1].public_key.to_b58check()

    # Extended public key
    xpublic_key = str(root_keys)

    # Адрес дочернего кошелька в зависимости от значения index
    address = Wallet.deserialize(xpublic_key, network='BTC').get_child(index, is_prime=False).to_address()

    rootkeys_wif = HDKey.from_path(master_key, f"m/44'/0'/0'/0/{index}")[-1]

    # Extended private key
    xprivatekey = str(rootkeys_wif.to_b58check())

    # Wallet import format
    wif = Wallet.deserialize(xprivatekey, network='BTC').export_to_wif()

    return address #, str(wif)

#####wallet = gen_address(999999999)


def get_balans(walleton):
    ret ={}
    url = f'https://blockchain.info/rawaddr/{walleton}'
    x = requests.get(url)
    print(x,"LLLLLLLLLLLLLLLLLLLLLLLLL")
    wallet = x.json()

    ret['balanse']= str(wallet['final_balance'])
    ret['tranz']=str(wallet['txs'])

    if wallet['total_received']==0:
      ret['total'] = 0
    return ret


