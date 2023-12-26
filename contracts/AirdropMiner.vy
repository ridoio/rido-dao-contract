# @version 0.3.7
"""
@title Token Minter in  airdrop stage
@author Pan
@license MIT
"""

interface RIDOERC20:
    def transfer(_to : address, _value : uint256) -> bool: nonpayable
    def balanceOf(_owner: address) -> uint256: view

interface DataPools:
    def user_extractable_reward(_addr: address, _data_pool: DynArray[bytes32, 30], _epoch:DynArray[uint64, 30], _attestations:DynArray[uint64, 30],_sig: Bytes[65]) -> uint256: nonpayable
    def set_epoch(_epoch :uint64): nonpayable


event Minted:
    recipient: indexed(address)
    minted: uint256


event UpdateMiningParameters:
    time: uint256
    epoch: uint64
    supply: uint256

admin: public(address)
token: public(address)
data_pool: public(address)

WEEK: constant(uint256) = 86400 * 7
INFLATION_DELAY:constant(uint256) = 86400
# RATE_REDUCTION_TIME: constant(uint256) = 2 * WEEK 
RATE_REDUCTION_TIME: constant(uint256) = 0 

REWARD_RATE: constant(uint256)= 3 * 10 ** 18

#Supply variables
minting_epoch: public(uint64)
start_epoch_time: public(uint256)
total_supply: public(uint256)

# minter -> user -> can mint?
allowed_to_mint_for: public(HashMap[address, HashMap[address, bool]])

@external
def __init__(_data_pool: address):
    self.admin = msg.sender
    self.data_pool = _data_pool

@external
def start(_token: address):
    assert self.admin == msg.sender, "only admin can call this func"

    assert self.token == empty(address), "the func could only called once"
    assert self.start_epoch_time == 0, "epoch time should start from 0"

    assert RIDOERC20(_token).balanceOf(self) > REWARD_RATE, "balance in airdrop contract should larger than rewart rate"
    self.token = _token
    self.start_epoch_time = block.timestamp - RATE_REDUCTION_TIME - 86400
    # self.start_epoch_time = block.timestamp - RATE_REDUCTION_TIME - 86400


@internal
def _update_mining_parameters():
    """
    @dev Update mining rate and supply at the start of the epoch
         Any modifying mining call must also call this
    """
    self.start_epoch_time += RATE_REDUCTION_TIME
    self.minting_epoch += 1
    log UpdateMiningParameters(block.timestamp, self.minting_epoch,  self.start_epoch_time)
    DataPools(self.data_pool).set_epoch(self.minting_epoch)


@external
def update_mining_parameters():
    """
    @notice Update mining rate and supply at the start of the epoch
    @dev Callable by any address, but only once per epoch
         Total supply becomes slightly larger if this function is called late
    """
    assert block.timestamp >= self.start_epoch_time + RATE_REDUCTION_TIME, "new epoch is not start" # dev: too soon!
    self._update_mining_parameters()

@external 
def epoch_write() -> uint64:
    """
    @notice Get num of the next mining
            while simultaneously updating mining parameters
    @return num of the epoch
    """
    _start_epoch_time: uint256 = self.start_epoch_time
    if block.timestamp >= _start_epoch_time + RATE_REDUCTION_TIME:
        self._update_mining_parameters()
        
    return self.minting_epoch

@external
def start_epoch_time_write() -> uint256:
    """
    @notice Get timestamp of the current mining epoch start
            while simultaneously updating mining parameters
    @return Timestamp of the epoch
    """
    _start_epoch_time: uint256 = self.start_epoch_time
    if block.timestamp >= _start_epoch_time + RATE_REDUCTION_TIME:
        self._update_mining_parameters()
        return self.start_epoch_time
    else:
        return _start_epoch_time

@external
def future_epoch_time_write() -> uint256:
    """
    @notice Get timestamp of the next mining epoch start
            while simultaneously updating mining parameters
    @return Timestamp of the next epoch
    """
    _start_epoch_time: uint256 = self.start_epoch_time
    if block.timestamp >= _start_epoch_time + RATE_REDUCTION_TIME:
        self._update_mining_parameters()
        return self.start_epoch_time + RATE_REDUCTION_TIME
    else:
        return _start_epoch_time + RATE_REDUCTION_TIME


@internal
def _mint_for(_for: address, _data_pool: DynArray[bytes32, 30], _epoch:DynArray[uint64, 30], _attestations:DynArray[uint64, 30], _sig: Bytes[65]):
    assert _for != empty(address)   # dev: zero address
    if block.timestamp >= self.start_epoch_time + RATE_REDUCTION_TIME:
        self._update_mining_parameters()

    extractable_reward: uint256 = DataPools(self.data_pool).user_extractable_reward(_for,_data_pool, _epoch, _attestations, _sig)
    # extractable_reward:uint256 = 10 ** 18
    if extractable_reward != 0:
        assert self.total_supply + extractable_reward <= convert(self.minting_epoch, uint256) * REWARD_RATE, "get up-boudner of extract"
        RIDOERC20(self.token).transfer(_for,extractable_reward)
        self.total_supply += extractable_reward
        log Minted(_for,extractable_reward)


@external
@nonreentrant('lock')
def mint_for(_for: address, _data_pool: DynArray[bytes32, 30], _epoch:DynArray[uint64, 30], _attestations:DynArray[uint64, 30], _sig: Bytes[65]):
    """
    @notice Mint tokens for `_for`
    @dev Only possible when `msg.sender` has been approved via `toggle_approve_mint`
    @param _data_pool slice of data pool uid
    @param _attestations slice of validate attestation amount
    @param _epoch slice of data pool
    @param _for Address to mint to
    """
    if self.allowed_to_mint_for[msg.sender][_for] or _for == msg.sender:
        self._mint_for(_for, _data_pool, _epoch, _attestations, _sig)

@external
@nonreentrant('lock')
def mint(_data_pool: DynArray[bytes32, 30], _epoch:DynArray[uint64, 30], _attestations:DynArray[uint64, 30], _sig: Bytes[65]):
    """
    @notice Mint everything which belongs to `msg.sender` and send to them
    @param _data_pool slice of data pool uid
    @param _attestations slice of validate attestation amount
    @param _epoch slice of data pool
    @param _sig Signature of RIDO on _amount
    """
    self._mint_for(msg.sender, _data_pool, _epoch, _attestations, _sig)


@external
def toggle_approve_mint(minting_user: address):
    """
    @notice allow `minting_user` to mint for `msg.sender`
    @param minting_user Address to toggle permission for
    """
    self.allowed_to_mint_for[minting_user][msg.sender] = not self.allowed_to_mint_for[minting_user][msg.sender]
