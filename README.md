# RIDO DAO Contracts

Vyper contracts userd in the RIDO Governance DAO.

## Overoview

RIDO is an Data Mining platform.

## Development

### Dependencies

- `python3` from version 3.8 to 3.11
- [apx](https://docs.apeworx.io/ape/stable/userguides/quickstart.html) verison 0.7 or upper

### Setup

```shell
git clone git@github.com:ridoio/rido-dao-contract.git
cd  rido-dao-contract
```

### Add deploy account 

```shell
ape account imports ${alia}
```

### Deploy contract 

```shell
ape run deploy --network=bsc:testnet:geth
```
