import requests
import json
import secrets
from random import randrange
from hashlib import sha256

def req_endpoint(endpoint, port=5000, data=None):
    # Check valid request
    get_reqs = ['/nodes/resolve', '/chain', '/mine']
    post_reqs = ['/nodes/register', '/transactions/new']
    if endpoint not in get_reqs and endpoint not in post_reqs:
        print('invalid request')
        return -1
    # Determine request address and method
    base_url = f'http://localhost:{port}'
    url = f'{base_url}{endpoint}'
    is_post = any(kwd in endpoint for kwd in post_reqs)
    if is_post:
        if data is None:
            print('POST requests required data')
            return -1
        else:
            req = requests.post(url, json=data)
    else:
        req = requests.get(url)
    return req.json()

def simulate_transaction(sender=False, recipient=False, amount=False):
    sender = secrets.token_hex(16) if not sender else sender
    recipient = secrets.token_hex(16) if not recipient else recipient
    amount = randrange(1,100) if not amount else amount
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    return transaction


# Interact with BC
# NOTE: initialize nodes fist e.g. using `bash tests/payne_nodes.sh init 2`
nodes = {
    'nodes': [f'http://localhost:{i}' for i in range(5000, 5002)]
}
req_endpoint('/nodes/register', port=5000, data=nodes)
req_endpoint('/chain')
req_endpoint('/transactions/new', data=simulate_transaction('sifan', 'alvaro', 42))
req_endpoint('/mine')
req_endpoint('/nodes/resolve')