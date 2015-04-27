from data.states import shop, levels, battle, main_menu, death
from data.states import credits
from . import setup, tools
from . import constants as c


MAIN_MENU = 'main menu'
CASTLE = 'castle'
HOUSE = 'house'
INN = 'Inn'
AULOFICER = 'Auloficer'
LUTHIER = 'Luthier'
TAMBOURIER = 'Tambourier'
ARTISAN = 'Artisan'
SCRIPTORIUM = 'Scriptorium'
SUNDRIES = 'Sundries'
MAGIC_SHOP = 'magic shop'
PLAYER_MENU = 'player menu'
FAESLANDING = 'FaesLanding'
OVERWORLD = 'Field1'
SOUTHFIELD = 'SouthField'
WESTFIELD = 'WestField'
BROTHER_HOUSE = 'brotherhouse'
BATTLE = 'battle'
DUNGEON = 'dungeon'
DUNGEON2 = 'dungeon2'
DUNGEON3 = 'dungeon3'
DUNGEON4 = 'dungeon4'
DUNGEON5 = 'dungeon5'
INSTRUCTIONS = 'instructions'
DEATH_SCENE = 'death scene'
LOADGAME = 'load game'
CREDITS = 'credits'


def main():
    """Add states to control here"""
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {MAIN_MENU: main_menu.Menu(),
                  FAESLANDING: levels.LevelState(FAESLANDING),
                  CASTLE: levels.LevelState(CASTLE),
                  HOUSE: levels.LevelState(HOUSE),
                  OVERWORLD: levels.LevelState(OVERWORLD, True),
                  SOUTHFIELD: levels.LevelState(SOUTHFIELD, True),
				  WESTFIELD: levels.LevelState(WESTFIELD, True),
                  BROTHER_HOUSE: levels.LevelState(BROTHER_HOUSE),
                  INN: shop.Inn(),
                  AULOFICER: shop.Auloficer(),
                  LUTHIER: shop.Luthier(),
                  TAMBOURIER: shop.Tambourier(),
                  ARTISAN: shop.Artisan(),
                  SCRIPTORIUM: shop.Scriptorium(),
                  SUNDRIES: shop.Sundries(),
                  MAGIC_SHOP: shop.MagicShop(),
                  BATTLE: battle.Battle,
                  DUNGEON: levels.LevelState(DUNGEON, True),
                  DUNGEON2: levels.LevelState(DUNGEON2, True),
                  DUNGEON3: levels.LevelState(DUNGEON3, True),
                  DUNGEON4: levels.LevelState(DUNGEON4, True),
                  DUNGEON5: levels.LevelState(DUNGEON5, True),
                  INSTRUCTIONS: main_menu.Instructions(),
                  LOADGAME: main_menu.LoadGame(),
                  DEATH_SCENE: death.DeathScene(),
                  CREDITS: credits.Credits()
                  }

    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()
