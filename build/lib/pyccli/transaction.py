from process import output
from helper import whichnet, check_if_file_exists, check_if_valid_json


def build(protocol_params_file, tx_out_file, change_address, final_tip, utxo_in_out, utxo_collateral, mainnet_flag=True):
    """
    Build a transaction and save the fileName into the tmp folder.
    """
    func = [
        'cardano-cli',
        'transaction',
        'build',
        '--alonzo-era',
        '--cardano-mode',
        '--protocol-params-file',
        protocol_params_file,
        '--change-address',
        change_address,
        '--invalid-hereafter',
        str(final_tip),
        '--out-file',
        tx_out_file
    ]
    func += utxo_collateral
    func += utxo_in_out
    func += whichnet(mainnet_flag)
    return output(func)


def sign(tx_body_file, tx_signed_file, signers, mainnet_flag=True):
    """
    Sign a transaction with the payment keys.
    """
    func = [
        'cardano-cli',
        'transaction',
        'sign',
        '--tx-body-file',
        tx_body_file,
        '--tx-file',
        tx_signed_file
    ]
    func += signers
    func += whichnet(mainnet_flag)
    return output(func)


def submit(file_path, file_name, mainnet_flag=True):
    """
    Submit the transaction to the blockchain.
    """
    func = [
        'cardano-cli',
        'transaction',
        'submit',
        '--cardano-mode',
        '--tx-file',
        file_path+file_name
    ]
    func += whichnet(mainnet_flag)
    return output(func)


def policy_id(file_path, file_name):
    """
    Calculate the policy id from a script file.
    """
    func = [
        'cardano-cli',
        'transaction',
        'policyid',
        '--script-file',
        file_path+file_name
    ]
    return output(func)


def calculate_min_value(file_path, file_name, multi_asset_string):
    """
    With a given protolcol parameters calculate the minimum required value for sending a utxo
    """
    func = [
        'cardano-cli',
        'transaction',
        'calculate-min-value',
        '--protocol-params-file',
        file_path+file_name,
        '--multi-asset',
        multi_asset_string
    ]
    return output(func)


def hash_script_data(value):
    """
    Get the hash value of some script data
    """
    if check_if_file_exists(value):
        value_type = [
            '--script-data-file',
            value
        ]
    else:
        value = str(value)
        if not check_if_valid_json(value):
            value = '"{}"'.format(value)
        value_type = [
            '--script-data-value',
            value
        ]
    func = [
        'cardano-cli',
        'transaction',
        'hash-script-data',
    ]
    func += value_type
    return output(func)


if __name__ == "__main__":
    print("Testing address.py")

    print('\nHash String Value\n')
    p, e = hash_script_data("Hello")
    print(p)
    print("PASS: ", e == 0)

    print('\nHash String Value\n')
    p, e = hash_script_data('tmp/datum.json')
    print(p)
    print("PASS: ", e == 0)
