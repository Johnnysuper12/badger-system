from tests.sett.fixtures.SushiBadgerLpOptimizerMiniDeploy import SushiBadgerLpOptimizerMiniDeploy
from helpers.token_utils import distribute_test_ether
from scripts.systems.badger_system import connect_badger
import pytest
from brownie import *
from config.badger_config import badger_config, sett_config
from scripts.deploy.deploy_badger import deploy_flow
from scripts.systems.badger_minimal import deploy_badger_minimal

from helpers.constants import *
from helpers.registry import registry
from tests.helpers import create_uniswap_pair, distribute_from_whales
from tests.sett.fixtures.BadgerLpMetaFarmMiniDeploy import BadgerLpMetaFarmMiniDeploy
from tests.sett.fixtures.BadgerRewardsMiniDeploy import BadgerRewardsMiniDeploy
from tests.sett.fixtures.CurveGaugeRenBtcMiniDeploy import CurveGaugeRenBtcMiniDeploy
from tests.sett.fixtures.CurveGaugeSBtcMiniDeploy import CurveGaugeSBtcMiniDeploy
from tests.sett.fixtures.CurveGaugeTBtcMiniDeploy import CurveGaugeTBtcMiniDeploy
from tests.sett.fixtures.HarvestMetaFarmMiniDeploy import HarvestMetaFarmMiniDeploy
from tests.sett.fixtures.SushiBadgerWBtcMiniDeploy import SushiBadgerWBtcMiniDeploy



def generate_sett_test_config(settsToRun, runTestSetts, runProdSetts=False):
    setts = []
    for settId in settsToRun:
        if runTestSetts:
            setts.append({
                'id': settId,
                'mode': "test"
            })
        if runProdSetts:
            setts.append({
                'id': settId,
                'mode': "prod"
            })
    return setts


# ===== Sett + Strategy Test Configuration =====

settsToRun = [
    # "native.badger",
    # "native.renCrv",
    # "native.sbtcCrv",
    # "native.tbtcCrv",
    # "harvest.renCrv",
    # "native.uniBadgerWbtc",
    # "sushi.sushiBadgerWBtc",
    "sushi.sushiWbtcWeth"
]

runTestSetts = True

settTestConfig = generate_sett_test_config(settsToRun, runTestSetts)

@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


# @pytest.fixture()
def badger_single_sett(settConfig):
    deployer = accounts[0]
    guardian = accounts[1]
    keeper = accounts[2]
    strategist = accounts[3]
    governance = accounts[4]

    print(settConfig)

    settId = settConfig['id']

    if settConfig['mode'] == 'test':
        if settId == "native.badger":
            return BadgerRewardsMiniDeploy(
                "native.badger",
                "StrategyBadgerRewards",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy()
        if settId == "native.renCrv":
            return CurveGaugeRenBtcMiniDeploy(
                "native.renCrv",
                "StrategyCurveGaugeRenBtcCrv",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy()
        if settId == "native.sbtcCrv":
            return CurveGaugeSBtcMiniDeploy(
                "native.sbtcCrv",
                "StrategyCurveGaugeSbtcCrv",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy()
        if settId == "native.tbtcCrv":
            return CurveGaugeTBtcMiniDeploy(
                "native.tbtcCrv",
                "StrategyCurveGaugeTbtcCrv",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy()
        if settId == "native.uniBadgerWbtc":
            return BadgerLpMetaFarmMiniDeploy(
                "native.uniBadgerWbtc",
                "StrategyBadgerLpMetaFarm",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy()
        if settId == "harvest.renCrv":
            return HarvestMetaFarmMiniDeploy(
                "harvest.renCrv",
                "StrategyHarvestMetaFarm",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy()
        if settId == "sushi.sushiBadgerWBtc":
            return SushiBadgerWBtcMiniDeploy(
                "sushi.sushiBadgerWBtc",
                "StrategySushiBadgerWbtc",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy()
        if settId == "sushi.sushiWbtcWeth":
            return SushiBadgerLpOptimizerMiniDeploy(
                "sushi.sushiWbtcWeth",
                "StrategySushiLpOptimizer",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy()
    if settConfig['mode'] == 'prod':
        """
        Run vs prod contracts, transferring assets to the test user
        (WIP)
        """
        badger = connect_badger(badger_config.prod_json)

        distribute_test_ether(badger.deployer, Wei("20 ether"))
        distribute_from_whales(badger, badger.deployer)

        return badger


@pytest.fixture(scope="function")
def badger_hunt_unit():
    deployer = accounts[0]
    badger = deploy_badger_minimal(deployer)
    distribute_from_whales(badger, deployer)

    badger.deploy_logic("BadgerHunt", BadgerHunt)
    badger.deploy_badger_hunt()

    source = accounts.at("0x394DCfbCf25C5400fcC147EbD9970eD34A474543", force=True)

    badger.token.transfer(badger.badgerHunt, Wei("100000 ether"), {"from": source})

    return badger


@pytest.fixture(scope="function")
def badger_tree_unit():
    deployer = accounts[0]
    badger = deploy_badger_minimal(deployer)
    distribute_from_whales(badger, deployer)

    badger.deploy_logic("BadgerHunt", BadgerHunt)
    badger.deploy_badger_hunt()

    badger.token.transfer(
        badger.badgerHunt, badger_config.huntParams.badgerAmount, {"from": deployer}
    )

    return badger


@pytest.fixture()
def badger(accounts):
    badger_system = deploy_flow(test=True, outputToFile=False)

    # Distribute Test Assets
    return badger_system


@pytest.fixture()
def badger_prod(accounts):
    badger_system = deploy_flow(test=True, outputToFile=True, uniswap=False)

    # Distribute Test Assets
    return badger_system
