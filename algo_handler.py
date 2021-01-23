"""
The Monopoly Bank
"""
import random
import pyqrcode
from algosdk import account, encoding, mnemonic
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn
from algosdk.v2client import algod

#  Set Configuration Values
ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
ALGOD_TOKEN = 'lAeLUMFRFz6ikbxRJ8AaC6ljWrVgIybe3klwEiNZ'
HEADERS = {"x-api-key":ALGOD_TOKEN}
ALGODCLIENT = algod.AlgodClient(algod_token=ALGOD_TOKEN, algod_address=ALGOD_ADDRESS, headers=HEADERS)
SENDER_ADDRESS = "3HPTKX4O4ME4RFX7CSRFEZUOWJBXTHQ5CG6ODV4GKA6B5OUBWCKH6LXDUA"
SENDER_MNEMONIC = 'atom asthma zero sleep shy leg outdoor banner smart second caution large unknown also permit veteran beach answer faculty warrior call guard below about echo'
SENDER_PRIVATE_KEY = mnemonic.to_private_key(SENDER_MNEMONIC)
ASSET_ID = 13080064


def algo_transaction(sender, private_key, receiver, amount):
    """Function for Algos transfer"""
    params = ALGODCLIENT.suggested_params()
    txn = PaymentTxn(sender, params, receiver, amount, None)
    signed_tx = txn.sign(private_key)
    ALGODCLIENT.send_transaction(signed_tx)
    return True

def asset_transfer(sender, private_key, receiver, amount, index):
    """Function for asset transfer"""
    params = ALGODCLIENT.suggested_params()
    txn = AssetTransferTxn(sender, params, receiver, amount, index)
    signed_tx = txn.sign(private_key)
    ALGODCLIENT.send_transaction(signed_tx)
    return True


def check_optin(address):
    """ Check account information for opt-in Monopoly """
    account_info = ALGODCLIENT.account_info(address)
    try:
        account_info['assets'][str(ASSET_ID)]['amount']
    except KeyError:
        return False
    return True


def fund_transaction(address, role):
    """ Fund account with Monopoly Money """
    amount = 0
    message_text = ''
    error_text = ''
    if encoding.is_valid_address(address):
        if check_optin(address):
            if role == 'player':
                amount = 1500
                message_text = 'Your account has been funded with 1,500 Monopoly Money'

            elif role == 'banker':
                amount = 20000
                message_text = 'Your account has been funded with 20,000 Monopoly Money'

            asset_transfer(SENDER_ADDRESS, SENDER_PRIVATE_KEY, address, amount, ASSET_ID)
        else:
            error_text = "Your account not opt-in to Monopoly Money asset"
    else:
        error_text = "Enter correct Algorand address"
    return message_text, error_text


def create_account(role):
    """ Create new account """
    RECEIVER_PRIVATE_KEY, RECEIVER_ADDRESS = account.generate_account()
    amount = 0
    algo_amount = 301000
    message = ''
    if role == 'player':
        amount = 1500
        message = 'Your account has been created with 1,500 Monopoly Money. Scan QR code.'

    elif role == 'banker':
        amount = 20000
        message = 'Your account has been created with 20,000 Monopoly Money. Scan QR code. '

    # Send 0.301 Algo to new account (for opt-in and transaction fees)
    algo_transaction(SENDER_ADDRESS, SENDER_PRIVATE_KEY, RECEIVER_ADDRESS, algo_amount)

    # Opt-in Monopoly Money Asset
    asset_transfer(RECEIVER_ADDRESS, RECEIVER_PRIVATE_KEY, RECEIVER_ADDRESS, 0, ASSET_ID)

    # Send Monopoly Money ASA
    asset_transfer(SENDER_ADDRESS, SENDER_PRIVATE_KEY, RECEIVER_ADDRESS, amount, ASSET_ID)

    # Create PNG file with QR-code which store the passphrase
    passphrase = '{{"version":"1.0", "mnemonic":"{}"}}'.format(mnemonic.from_private_key(RECEIVER_PRIVATE_KEY))
    qr_code = pyqrcode.create(passphrase)
    rnd = random.random()
    qr_file = 'static/{}{}.png'.format(RECEIVER_ADDRESS, str(rnd))
    qr_code.png(qr_file, scale=6)
    return qr_file, message
