# @version 0.3.7
"""
@title Token Minter in  airdrop stage
@author Pan
@license MIT
"""

struct AttestationAmount:
    epoch: uint64
    amount: uint64
    data_pool: bytes32


interface RIDOERC20:
    def transfer(_to : address, _value : uint256) -> bool: nonpayable

interface DataPools:
    def user_extractable_reward(_addr: address, _amounts: DynArray[AttestationAmount, 30],_sig: Bytes[65]) -> uint256: nonpayable


event Minted:
    recipient: indexed(address)
    minted: uint256


token: public(address)
data_pool: public(address)

# minter -> user -> can mint?
allowed_to_mint_for: public(HashMap[address, HashMap[address, bool]])

@external
def __init__(_token: address, _data_pool: address):
    self.token = _token
    self.data_pool = _data_pool

@internal
def _mint_for(_for: address, _amounts: DynArray[AttestationAmount, 30], _sig: Bytes[65]):
    extractable_reward: uint256 = DataPools(self.data_pool).user_extractable_reward(_for,_amounts,_sig)
    if extractable_reward != 0:
        RIDOERC20(self.token).transfer(_for,extractable_reward)
        log Minted(_for,extractable_reward)


@external
@nonreentrant('lock')
def mint_for(_for: address, _amounts: DynArray[AttestationAmount, 30], _sig: Bytes[65]):
    """
    @notice Mint tokens for `_for`
    @dev Only possible when `msg.sender` has been approved via `toggle_approve_mint`
    @param _amounts is the slice including the (epoch, attestation amount, data_pool) 
    @param _for Address to mint to
    """
    if self.allowed_to_mint_for[msg.sender][_for]:
        self._mint_for(_for,_amounts,_sig)

@external
@nonreentrant('lock')
def mint(_amounts: DynArray[AttestationAmount, 30], _sig: Bytes[65]):
    """
    @notice Mint everything which belongs to `msg.sender` and send to them
    @param _amounts is the slice including the (epoch, attestation amount, data_pool) 
    @param _sig Signature of RIDO on _amount
    """
    self._mint_for(msg.sender, _amounts, _sig)


@external
def toggle_approve_mint(minting_user: address):
    """
    @notice allow `minting_user` to mint for `msg.sender`
    @param minting_user Address to toggle permission for
    """
    self.allowed_to_mint_for[minting_user][msg.sender] = not self.allowed_to_mint_for[minting_user][msg.sender]
