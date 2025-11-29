from pathlib import Path
from typing import Annotated

from pydantic_xml import attr, element

from .base_reader import BaseReader, ConfiguredXmlModel


class FarmsReader(BaseReader):
    def __init__(self, path: Path) -> None:
        path = path / "farms.xml"
        super().__init__(path)

        self.farms: list[Farm] = self._parse_all(Farm)


class Player(ConfiguredXmlModel, tag="player"):
    unique_user_id: Annotated[str, attr()]
    farm_manager: Annotated[bool, attr()]
    last_nickname: Annotated[str, attr()]
    time_last_connected: Annotated[str, attr()]
    buy_vehicle: Annotated[bool, attr()]
    sell_vehicle: Annotated[bool, attr()]
    buy_placeable: Annotated[bool, attr()]
    sell_placeable: Annotated[bool, attr()]
    manage_contracts: Annotated[bool, attr()]
    trade_animals: Annotated[bool, attr()]
    create_fields: Annotated[bool, attr()]
    landscaping: Annotated[bool, attr()]
    hire_assistant: Annotated[bool, attr()]
    reset_vehicle: Annotated[bool, attr()]
    manage_productions: Annotated[bool, attr()]
    cut_trees: Annotated[bool, attr()]
    manage_rights: Annotated[bool, attr()]
    transfer_money: Annotated[bool, attr()]
    update_farm: Annotated[bool, attr()]
    manage_contracting: Annotated[bool, attr()]


class Players(ConfiguredXmlModel, tag="players"):
    player: Annotated[list[Player], element(tag="player")]


class Statistics(ConfiguredXmlModel, tag="statistics"):
    traveled_distance: Annotated[float, element()]
    fuel_usage: Annotated[float, element()]
    seed_usage: Annotated[float, element()]
    spray_usage: Annotated[float, element()]
    worked_hectares: Annotated[float, element()]
    cultivated_hectares: Annotated[float, element()]
    sown_hectares: Annotated[float, element()]
    sprayed_hectares: Annotated[float, element()]
    threshed_hectares: Annotated[float, element()]
    plowed_hectares: Annotated[float, element()]
    harvested_grapes: Annotated[float, element()]
    harvested_olives: Annotated[float, element()]
    worked_time: Annotated[float, element()]
    cultivated_time: Annotated[float, element()]
    sown_time: Annotated[float, element()]
    sprayed_time: Annotated[float, element()]
    threshed_time: Annotated[float, element()]
    plowed_time: Annotated[float, element()]
    bale_count: Annotated[int, element()]

    # Animal Breeding Counts
    breed_cows_count: Annotated[int, element()]
    breed_sheep_count: Annotated[int, element()]
    breed_pigs_count: Annotated[int, element()]
    breed_chicken_count: Annotated[int, element()]
    breed_horses_count: Annotated[int, element()]
    breed_goats_count: Annotated[int, element()]
    breed_water_buffalo_count: Annotated[int, element()]

    mission_count: Annotated[int, element()]
    revenue: Annotated[float, element()]
    expenses: Annotated[float, element()]
    play_time: Annotated[float, element()]
    planted_tree_count: Annotated[int, element()]
    cut_tree_count: Annotated[int, element()]
    wood_tons_sold: Annotated[float, element()]
    tree_types_cut: Annotated[str, element()]
    pet_dog_count: Annotated[int, element()]
    repair_vehicle_count: Annotated[int, element()]
    repaint_vehicle_count: Annotated[int, element()]
    horse_jump_count: Annotated[int, element()]
    sold_cotton_bales: Annotated[int, element()]
    wrapped_bales: Annotated[int, element()]

    # Vehicle Distances
    tractor_distance: Annotated[float, element()]
    car_distance: Annotated[float, element()]
    truck_distance: Annotated[float, element()]
    horse_distance: Annotated[float, element()]


class DayStats(ConfiguredXmlModel, tag="stats"):
    day: Annotated[int, attr()]

    # Cost/Sale Items
    new_vehicles_cost: Annotated[float, element()]
    sold_vehicles: Annotated[float, element()]
    new_handtools_cost: Annotated[float, element()]
    sold_handtools: Annotated[float, element()]
    new_animals_cost: Annotated[float, element()]
    sold_animals: Annotated[float, element()]
    construction_cost: Annotated[float, element()]
    sold_buildings: Annotated[float, element()]
    field_purchase: Annotated[float, element()]
    field_selling: Annotated[float, element()]

    # Operational Costs/Maintenance/Income
    vehicle_running_cost: Annotated[float, element()]
    vehicle_leasing_cost: Annotated[float, element()]
    property_maintenance: Annotated[float, element()]
    property_income: Annotated[float, element()]
    production_costs: Annotated[float, element()]

    # Sale Income
    sold_wood: Annotated[float, element()]
    sold_bales: Annotated[float, element()]
    sold_wool: Annotated[float, element()]
    sold_milk: Annotated[float, element()]
    sold_products: Annotated[float, element()]

    # Purchase Costs
    purchase_fuel: Annotated[float, element()]
    purchase_seeds: Annotated[float, element()]
    purchase_fertilizer: Annotated[float, element()]
    purchase_saplings: Annotated[float, element()]
    purchase_water: Annotated[float, element()]
    purchase_bales: Annotated[float, element()]
    purchase_pallets: Annotated[float, element()]

    # Various Income/Expenses
    harvest_income: Annotated[float, element()]
    income_bga: Annotated[float, element()]
    mission_income: Annotated[float, element()]
    wage_payment: Annotated[float, element()]
    other: Annotated[float, element()]
    loan_interest: Annotated[float, element()]


class Finances(ConfiguredXmlModel, tag="finances"):
    stats: Annotated[list[DayStats], element(tag="stats")]


class Npc(ConfiguredXmlModel, tag="npc"):
    index: Annotated[int, attr()]
    count: Annotated[int, attr()]


class NpcJobs(ConfiguredXmlModel, tag="npcJobs"):
    npc: Annotated[list[Npc], element(tag="npc")]


class Farm(ConfiguredXmlModel, tag="farm"):
    farm_id: Annotated[int, attr()]
    name: Annotated[str, attr()]
    color: Annotated[int, attr()]
    loan: Annotated[float, attr()]
    money: Annotated[float, attr()]

    players: Annotated[Players, element()]
    statistics: Annotated[Statistics, element()]
    finances: Annotated[Finances, element()]
    npc_jobs: Annotated[NpcJobs, element()]


class Farms(ConfiguredXmlModel, tag="farms"):
    farm: Annotated[list[Farm], element(tag="farm")]
