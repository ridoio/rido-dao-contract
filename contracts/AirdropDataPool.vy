# @version 0.3.7
"""
@title Data Pool in airdrop stage
@author Pan
@license MIT
"""

interface AirdropMinter:
    def epoch_write() -> uint64: nonpayable


#f(s,x_j,n)= s \cdot \sum_{m=0}^{n-1} (\frac{t_1}{t_2})^m + (\frac{t_1}{t_2})^n \cdot (x_j-ns)
struct DataPoolSlope:
    t: decimal
    s: uint64
    reward: uint256


minter: public(address)
admin: public(address)
gaugeController: public(address)

# map(schema uid -> map(epoch -> data pool info))
pools: public(HashMap[bytes32, HashMap[uint64, DataPoolSlope]])

# map(schema uid -> map(epoch -> (total attestation amount)))
totalAttestations: public(HashMap[bytes32, HashMap[uint64, uint64]])

# map(user -> map(epoch->attestation numbers))
userAttestations: public(HashMap[address,HashMap[uint64,uint64]])

mintingEpoch: public(uint64)

@external
def __init__():
    self.admin = msg.sender

@external
def set_minter(_minter: address):
    """
    @notice Set the minter address
    @dev Only callable once, when minter has not yet been set
    @param _minter Address of the minter
    """
    assert msg.sender == self.admin
    assert _minter != empty(address) 
    assert self.minter == empty(address) 
    self.minter = _minter

@external
def set_epoch(_epoch :uint64):
    assert self.minter == msg.sender
    assert self.mintingEpoch < _epoch
    self.mintingEpoch = _epoch

@external
def set_gauge_controller(_gauge_controller: address):
    """
    @notice Set the gauge controller address
    @dev Only callable once, when gauge controller has not yet been set
    @param _gauge_controller Address of the gauge controller
    """
    assert msg.sender == self.admin
    assert _gauge_controller != empty(address) 
    # assert self.gaugeController == empty(address) 
    self.gaugeController = _gauge_controller

@external
def set_data_pools(_schemaUID: bytes32, _t1: uint64, _t2: uint64, _s:uint64, _reward:uint256 ,_epoch: uint64):
    """
    @notice Add or Set new data pool info
    @dev Only admin can call this function
    @param  _schemaUID UID of data pool
    @param _t1 denominator of step in data pool
    @param _t2 moleculestep of step in data pool
    @param _s window size of data pool information
    @param _reward reward of data pool in epoch `_epoch`
    @param _epoch epoch in which reward of data pool is `_reward`
    """
    AirdropMinter(self.minter).epoch_write()

    assert msg.sender == self.gaugeController, "only gauage controller can add new data pool"
    assert _epoch >= self.mintingEpoch, "you can only set current or future data pool info"
    assert _t1 != 0 and _t2 !=0 and _s != 0 and _reward != 0, "invalid params"

    unempty_start: uint64 = self.mintingEpoch
    current_slope:DataPoolSlope = empty(DataPoolSlope)
    if self.pools[_schemaUID][self.mintingEpoch -1].s == 0:
        for i in range (2,9999999):
            if i >= self.mintingEpoch-1:
                break
            if self.pools[_schemaUID][self.mintingEpoch-i].s != 0:
                current_slope = self.pools[_schemaUID][self.mintingEpoch-i]
                unempty_start = self.mintingEpoch-i

        for i in range (unempty_start,unempty_start+99999999):
            if i >= self.mintingEpoch-1:
                break
            self.pools[_schemaUID][i] = current_slope
    _t : decimal = convert(_t1,decimal) / convert(_t2, decimal)
    self.pools[_schemaUID][_epoch] = DataPoolSlope({t:_t , s:_s, reward:_reward})


@external
def update_each_epoch_attestations(_data_pool: DynArray[bytes32, 30], _epoch:DynArray[uint64, 30], _attestations:DynArray[uint64, 30]):
    """
    @notice Update total generated attestations amount in each epoch
    @dev Only admin can call this function
    @param _data_pool slice of data pool uid
    @param _attestations slice of validate attestation amount
    @param _epoch slice of data pool
    """

    assert msg.sender == self.admin
    assert len(_data_pool) == len(_epoch) and len(_epoch) == len(_attestations), "the len of data_pools, epoch and attestation should be same"

    i: int32 = 0
    for _pool in _data_pool:
        if self.totalAttestations[_pool][_epoch[i]] == 0:
            self.totalAttestations[_pool][_epoch[i]] = _attestations[i]
        i+=1


@external
def user_extractable_reward(_addr: address, _data_pool: DynArray[bytes32, 30], _epoch:DynArray[uint64, 30], _attestations:DynArray[uint64, 30],_sig: Bytes[65]) -> uint256:
    """
    @notice Update total generated attestations amount in each epoch
    @dev Only airdrop minter can call this function
    @param _addr the address you want to checkout the extractable
    @param _data_pool slice of data pool uid
    @param _attestations slice of validate attestation amount
    @param _epoch slice of data pool
    """
    assert msg.sender == self.minter
    assert len(_data_pool) == len(_epoch) and len(_epoch) == len(_attestations), "the len of data_pools, epoch and attestation should be same"

    extractableRIDO: uint256 = 0
    _hash: bytes32 = convert(_addr,bytes32)
    
    i: int32 = 0
    for _pool in _data_pool:
        _hash = keccak256(concat(
            _hash,
            convert(_epoch[i],bytes8),
            convert(_attestations[i],bytes8),
            _pool,
        ))
        i+=1

    assert self._ecrecoverSig(_hash,_sig) == self.admin
    
   
    for e in _epoch:
        if self.userAttestations[_addr][e] != 0 and e < self.mintingEpoch:
            continue
        else:
            _totalAttestations: uint64 = self.totalAttestations[_data_pool[i]][e]
            extractableRIDO += self._get_rate_of_pool(_attestations[i],_totalAttestations,_data_pool[i],e)
        
    return extractableRIDO


@internal
@view
def _ecrecoverSig(_hash: bytes32, _sig: Bytes[65]) -> address:
    """
    @dev Recover signer address from a message by using their signature
    @param _hash bytes32 message, the hash is the signed message. What is recovered is the signer address.
    @param _sig bytes signature, the signature is generated using web3.eth.sign()
    """
    if len(_sig) != 65:
        return empty(address)
    # ref. https://gist.github.com/axic/5b33912c6f61ae6fd96d6c4a47afde6d
    # The signature format is a compact form of:
    # {bytes32 r}{bytes32 s}{uint8 v}
    r: uint256 = extract32(_sig, 0, output_type=uint256)
    s: uint256 = extract32(_sig, 32, output_type=uint256)
    v: int128 = convert(slice(_sig, 64, 1), int128)
    # Version of signature should be 27 or 28, but 0 and 1 are also possible versions.
    # geth uses [0, 1] and some clients have followed. This might change, see:x
    # https://github.com/ethereum/go-ethereum/issues/2053
    if v < 27:
        v += 27
    if v in [27, 28]:
        return ecrecover(_hash, convert(v, uint256), r, s)
    return empty(address)

@external
@view
def ecrecoverSig(_hash: bytes32, _sig: Bytes[65]) -> address:
    return self._ecrecoverSig(_hash,_sig)

 

@internal
@view
def _get_rate_of_pool(_amount: uint64, _total: uint64, _data_pool: bytes32, _epoch: uint64) -> uint256:
    slope : DataPoolSlope =  self._get_data_pool_info(_epoch,_data_pool)
    f: uint256 = self._piecewise_function(slope.s, slope.t, _amount)
    return f * slope.reward / (convert(self.totalAttestations[_data_pool][_epoch],uint256) * 10 ** 10)

@external
@view
def get_rate_of_pool(_amount: uint64, _total: uint64, _data_pool: bytes32, _epoch: uint64) -> uint256:
    return self._get_rate_of_pool(_amount,_total,_data_pool,_epoch)


@internal
@view
def _piecewise_function(s: uint64,t: decimal, x: uint64) -> uint256:
    n: uint64 = x/s
    _s: decimal = 0.0
    _ti: decimal = 1.0
    for i in range (9999999):
        if i >= n:
            break
        if i == 0:
            _ti = 1.0
        else:
            _ti = _ti * t

        _s = _s + _ti

    _ti = _ti * t

    _s = convert(s, decimal) * _s
    
    _f: decimal = (_s + _ti * convert(x - n * s,decimal)) * 10000000000.0
    result: uint256 = convert(_f ,uint256)
    return result

@external
@view
def piecewise_function(s: uint64,t1: uint64, t2:uint64, x: uint64) -> uint256:
    t: decimal = convert(t1,decimal) / convert(t2, decimal)
    return self._piecewise_function(s,t,x)

@internal
@view
def _get_data_pool_info(_epoch: uint64, _data_pool: bytes32) -> DataPoolSlope:
    assert _epoch <= self.mintingEpoch
    for i in range (999999999):
        if i > _epoch:
            break

        _slope: DataPoolSlope = self.pools[_data_pool][_epoch-i]
        if _slope.reward != 0:
            return _slope
    return empty(DataPoolSlope)
    
@external
@view
def get_data_pool_info(_epoch: uint64, _data_pool: bytes32) -> (decimal,uint64,uint256):
    '''
    @dev get data pool information in epoch `epoch`
    @param _epoch the epoch you want to checkout
    @param _data_pool the data pool uid you want to check
    '''
    _slope: DataPoolSlope =  self._get_data_pool_info(_epoch,_data_pool)
    return _slope.t, _slope.s,_slope.reward
    

@external
@view
def get_total_attestations(_epoch: uint64, _data_pool: bytes32) -> uint64:
    return self.totalAttestations[_data_pool][_epoch]