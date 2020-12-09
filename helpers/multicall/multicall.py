# Credit: https://github.com/banteg/multicall.py/blob/master/multicall/multicall.py
from typing import List

from brownie import web3

from helpers.multicall import Call
from helpers.multicall.constants import MULTICALL_ADDRESSES


class Multicall:
    def __init__(self, calls: List[Call]):
        self.calls = calls

    def __call__(self):
        aggregate = Call(
            MULTICALL_ADDRESSES[web3.eth.chainId],
            "aggregate((address,bytes)[])(uint256,bytes[])",
        )
        args = [[[call.target, call.data] for call in self.calls]]
        block, outputs = aggregate(args)
        result = {}
        for call, output in zip(self.calls, outputs):
            result.update(call.decode_output(output))
        return result
