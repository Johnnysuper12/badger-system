import pytest
from brownie import (
    Wei,
    BadgerHunt,
    accounts,
)

from config.badger_config import badger_config, digg_config
from scripts.deploy.deploy_badger import deploy_flow
from scripts.systems.badger_minimal import deploy_badger_minimal
from scripts.systems.digg_minimal import deploy_digg_minimal
from scripts.systems.constants import SettType
from helpers.token_utils import distribute_test_ether
from scripts.systems.badger_system import connect_badger
from tests.helpers import distribute_from_whales
from tests.sett.fixtures import (
    SushiBadgerLpOptimizerMiniDeploy,
    DiggRewardsMiniDeploy,
    BadgerLpMetaFarmMiniDeploy,
    BadgerRewardsMiniDeploy,
    CurveGaugeRenBtcMiniDeploy,
    CurveGaugeSBtcMiniDeploy,
    CurveGaugeTBtcMiniDeploy,
    HarvestMetaFarmMiniDeploy,
    SushiBadgerWBtcMiniDeploy,
    SushiDiggWbtcLpOptimizerMiniDeploy,
    UniDiggWbtcLpMiniDeploy,
)


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
    # "sushi.sushiWbtcWeth",
    "native.digg",
    # "native.uniDiggWbtc",
    # "native.sushiDiggWbtc",
]

diggSettsToRun = [
    "native.digg",
    "native.uniDiggWbtc",
    "native.sushiDiggWbtc",
]

runTestSetts = True

settTestConfig = generate_sett_test_config(settsToRun, runTestSetts)
diggSettTestConfig = generate_sett_test_config(diggSettsToRun, runTestSetts)


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
        if settId == "native.digg":
            return DiggRewardsMiniDeploy(
                "native.digg",
                "StrategyDiggRewards",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy(sett_type=SettType.DIGG)
        if settId == "native.uniDiggWbtc":
            return UniDiggWbtcLpMiniDeploy(
                "native.uniDiggWbtc",
                "StrategyDiggLpMetaFarm",
                deployer,
                strategist=strategist,
                guardian=guardian,
                keeper=keeper,
                governance=governance,
            ).deploy()
        if settId == "native.sushiDiggWbtc":
            return SushiDiggWbtcLpOptimizerMiniDeploy(
                "native.sushiDiggWbtc",
                "StrategySushiDiggWbtcLpOptimizer",
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
        distribute_from_whales(badger.deployer)

        return badger


@pytest.fixture(scope="function")
def badger_hunt_unit():
    deployer = accounts[0]
    badger = deploy_badger_minimal(deployer)
    distribute_from_whales(deployer)

    badger.deploy_logic("BadgerHunt", BadgerHunt)
    badger.deploy_badger_hunt()

    source = accounts.at("0x394DCfbCf25C5400fcC147EbD9970eD34A474543", force=True)

    badger.token.transfer(badger.badgerHunt, Wei("100000 ether"), {"from": source})

    return badger


@pytest.fixture(scope="function")
def badger_tree_unit():
    deployer = accounts[0]
    badger = deploy_badger_minimal(deployer)
    distribute_from_whales(deployer)

    badger.deploy_logic("BadgerHunt", BadgerHunt)
    badger.deploy_badger_hunt()

    badger.token.transfer(
        badger.badgerHunt, badger_config.huntParams.badgerAmount, {"from": deployer}
    )

    return badger


@pytest.fixture(scope="function")
def digg_distributor_unit():
    badger = connect_badger(badger_config.prod_json)
    deployer = badger.deployer
    devProxyAdminAddress = badger.devProxyAdmin.address
    daoProxyAdminAddress = badger.daoProxyAdmin.address
    digg = deploy_digg_minimal(deployer, devProxyAdminAddress, daoProxyAdminAddress, owner=deployer)

    # deployer should have eth but just in case
    distribute_test_ether(badger.deployer, Wei("20 ether"))

    digg.deploy_airdrop_distributor(
        digg_config.airdropRoot,
        badger.rewardsEscrow,
        digg_config.reclaimAllowedTimestamp,
    )

    totalSupply = digg.token.totalSupply()
    # 15% airdropped
    digg.token.transfer(digg.diggDistributor, totalSupply * .15, {"from": deployer})

    return digg


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
