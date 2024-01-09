interface IAirdropMiner:
    def mint(_data_pool: DynArray[bytes32, 100], _epoch:DynArray[uint64, 100], _attestations:DynArray[uint64, 100], _sig: Bytes[65]): nonpayable


