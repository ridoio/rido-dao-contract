# RIDO DAO Contracts
All contract sources are within this directory.

- AirdropMiner.vy: The miner used in airdrop stage(stage 1)
- AirdropDataPool.vy: The data pool used in airdrop stage(stage 1)
- ERC20RIDO.vy: ERC20 token (RIDO)
- RIDOInfo.vy: How does RIDO been distributed

## Airdrop Miner

Before start airdrop stage, `AirdropMiner` should be allocated ERC20RIDO and ERC20RIDO token
and with time pass, the amount of RIDO that users can extract from `AirdropMiner` contract increase linearly.

As the reward of data mining is allocated periodically, we should define the `epoch` as the duration of one period of time.
Currently, the duration of `epoch` is 1 and the duration of one `epoch` is 2 weeks. Moreover, all attestations created before the start of 
`AirdropMiner` is recorded that created in `epoch 0`. 

And because `AirdropDataPool` contract also record valid attestations amount, data pools info and reward information, so data pool
also should record current epoch which will be updated when update the epoch in `AirdropMiner`.

User can extract their reward by provide withdrawing info. One withdraw should include `(address, data_pool, epoch, user_attestations_amount)`.
To extract reward in bulk and verify the withdrawing info, user should provide `address, []data_pool, []epocjh, []user_attestations_amount,s` where `s` is
ther signature of RIDO signed on the withdrawing info.


## Airdrop Data Pools

This is the main contract of airdrop stage.

### pools : Data Pools information
C

- total attestations: Total attestations of each data pools created in each epoch
- user attestations: user's attestations of each data pools created in each epoch


