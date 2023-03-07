import pickle

# Load the addresses from the pickle file
with open('output/contract_addresses_verified.pickle', 'rb') as f:
    addresses = pickle.load(f)

# Prepend 'https://etherscan.io/address/' to each address
addresses_with_url = [f'https://etherscan.io/address/{address}' for address in addresses]

# Save the addresses to a file
with open('output/addresses_with_url.txt', 'w') as f:
    for address in addresses_with_url:
        f.write(f'{address}\n')
