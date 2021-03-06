# `paynecoin` (PYN) <!-- omit in toc -->

This repository contains the code for running a toy blockchain that allows you to make transactions and mine `paynecoin`, a made up cryptocurrency for educational purposes.

#### Note

All instructions in this repository assume you have access to a Unix machine (macOS or Linux).

- [1. Installation](#1-installation)
  - [1.1. Python](#11-python)
  - [1.2. Poetry](#12-poetry)
- [2. Running the blockchain](#2-running-the-blockchain)
  - [2.1. Initializing nodes](#21-initializing-nodes)
    - [2.1.1. Manual node initialization](#211-manual-node-initialization)
    - [2.1.2. Bulk node initialization](#212-bulk-node-initialization)
  - [2.2. Interacting with the blockchain](#22-interacting-with-the-blockchain)
    - [2.2.1. Simulating transactions](#221-simulating-transactions)

# 1. Installation

Simply clone this repository to your machine to install.
For example, you can clone this repository to your home directory by running
```sh
cd ~
git clone git@github.com:acarril/paynecoin.git # SSH (recommended), or
git clone https://github.com/acarril/paynecoin.git # HTTPS
```

## 1.1. Python

You will also need a working Python 3.5+ installation. I assume you already have one working, but if not, I recommend installing [Anaconda](https://www.anaconda.com/products/individual).

If you already know how to manage your Python environments and packages, you can skip the following subsection. Just make sure you install the dependencies listed in [`pyproject.toml`](pyproject.toml).

## 1.2. Poetry

We will use [Poetry](https://python-poetry.org/) to easily manage packages and environments.
1. Follow the [installation instructions](https://python-poetry.org/docs/#installation) to set Poetry up in your machine. You can verify that the installation was successful by running the following command without any errors:
```sh
poetry --version
```
2. Navigate to the local copy of this repository and install the defined dependencies for this project. For example, if you cloned the project to your home directory, run
```sh
cd ~/paynecoin
poetry install
```

# 2. Running the blockchain

Navigate to the project's directory (e.g. `cd ~/paynecoin`) and activate the project's Python virtual environment by spawning a new shell:
```sh
poetry shell
```
Everything going forward will assume you are located in the project's directory and initialized its corresponding Poetry shell.

## 2.1. Initializing nodes

Nodes are virtual representations of the agents that will be interacting with the blockchain. First they have to be initialized, at which point they will be assigned a port in the local host (e.g. `http://localhost:5000/`).

### 2.1.1. Manual node initialization

Initialize a node in the development server with
```sh
python paynecoin/api.py
```
This initializes a node in the default port, `5000`.
You can initialize additional nodes in other ports by using the `-p <port>` option. For example,
```sh
python paynecoin/api.py -p 5001
```

Each node is assigned an automatically-generated node UUID. However, you can specify a custom UUID for the node using the `-u <uuid>` option. For example,
```sh
python paynecoin/api.py -u alice
```
Whenever a node mines a block, the reward will be associated to this node UUID.

### 2.1.2. Bulk node initialization

I wrote a simple auxiliary shell script that makes it easier to initialize and terminate nodes in bulk.
The script is in [`tests/payne_nodes.sh`](tests/payne_nodes.sh).
- **Initialize** a sequence of nodes associated to ports `5000, ..., 5000+(i-1)` by running
```sh
bash tests/payne_nodes.sh init [i]
```
where `[i]` is an optional integer; if none is specified, the program will initialize a single node in port `5000`.
For example, you can initialize three nodes associated to ports `5000`, `5001`, and `5002` by running
```sh
bash tests/payne_nodes.sh init 3
```
- **List** the jobs associated to the running nodes using `bash tests/payne_nodes.sh list`.
- **Kill**  all the initialized nodes using `bash tests/payne_nodes.sh kill`

#### Note <!-- omit in toc -->

Node instances are simply Python processes, which can be managed with the usual Unix tools. For example, you can list the processes running the nodes with
```sh
ps ax | grep paynecoin/api.py | grep -v grep
```
You can kill these processes using, for example,
```sh
kill $(ps ax | grep paynecoin/api.py | grep -v grep | awk '{print $1}')
```

## 2.2. Interacting with the blockchain

This implementation serves the blockchain as an API with which we can interact using HTTP requests (i.e. ```GET``` and ```POST```).
An easy way to manage these requests interactively is to use a tool like [Postman](https://www.postman.com/downloads/).

<table>
<thead>
  <tr>
    <th>request</th>
    <th>method</th>
    <th>description</th>
    <th>request body</th>
    <th>request body example</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><pre>/nodes/register</pre></td>
    <td><pre>POST</pre><br></td>
    <td>register a list of new nodes in the form of URLs</td>
    <td>JSON list of URLs</td>
    <td><pre>{<br>    "nodes": [<br>        "http://localhost:5000",<br>        "http://localhost:5001"<br>    ]<br>}</pre></td>
  </tr>
   <tr>
    <td><pre>/nodes/register</pre></td>
    <td><pre>GET</pre><br></td>
    <td>list registered nodes</td>
    <td>NA</td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/nodes/resolve</pre></td>
    <td><pre>GET</pre><br></td>
    <td>implement consensus algorithm to resolve conflicts</td>
    <td>NA</td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/chain</pre></td>
    <td><pre>GET</pre><br></td>
    <td>return full blockchain</td>
    <td>NA</td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/mine</pre></td>
    <td><pre>GET</pre><br></td>
    <td>mine a new block</td>
    <td>NA</td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/transaction</pre></td>
    <td><pre>POST</pre><br></td>
    <td>register a new transaction</td>
    <td>JSON list of transaction parameters</td>
    <td><pre>{<br>    "sender": "alvaro",<br>    "recipient": "jonathan",<br>    "amount": 42<br>}</pre></td>
  </tr>
  <tr>
    <td><pre>/wallets</pre></td>
    <td><pre>GET</pre><br></td>
    <td>get all wallets</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/wallets/{uuid}</pre></td>
    <td><pre>GET</pre><br></td>
    <td>get wallet of {uuid}</td>
    <td></td>
    <td></td>
  </tr>
</tbody>
</table>

### 2.2.1. Simulating transactions

The script [`tests/simulation.py`](tests/simulation.py) contains some functions and code to easily initialize and manage the blockchain using Python.
Take a look at this file and the functions within to register nodes, mine blocks, post transactions and check the blockchain.
Inside the class' modules you can find a video where I explain more details about this script.

