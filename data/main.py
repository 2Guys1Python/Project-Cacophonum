from data.states import shop, levels, battle, main_menu, death
from data.states import credits
from . import setup, tools
from . import constants as c


FAES_LANDING = 'faes landing'
MAIN_MENU = 'main menu'
FL_FIELD1 = 'faes landing field 1'
FL_FIELD2 = 'faes landing field 2'
FL_FIELD3 = 'faes landing field 3'
FL_CASTLE = 'faes landing castle'
FL_INN = 'faes landing inn'
FL_SUNDRIES = 'faes landing sundries' #items
FL_AULOFICER = 'faes landing auloficer' #wind
FL_LUTHIER = 'faes landing luthier' #strings
FL_TAMBOURIER = 'faes landing tambourier' #percussion
FL_ARTISAN = 'faes landing artisan' #accessories
FL_SCRIPTORIUM = 'faes landing scriptorium' #songs
HOUSE = 'house'
BATTLE = 'battle'
INSTRUCTIONS = 'instructions'
DEATH_SCENE = 'death scene'
LOADGAME = 'load game'
CREDITS = 'credits'


def main():
    """Add states to control here"""
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {MAIN_MENU: main_menu.Menu(),
                  FAES_LANDING: levels.LevelState(FAES_LANDING),
                  FL_FIELD1: levels.LevelState(FL_FIELD1, True),
				  FL_FIELD2: levels.LevelState(FL_FIELD2, True),
				  FL_FIELD3: levels.LevelState(FL_FIELD3, True),
				  FL_ACADEMY: levels.LevelState(FL_ACADEMY),
                  HOUSE: levels.LevelState(HOUSE),
                  FL_CASTLE: levels.LevelState(FL_CASTLE),
                  FL_INN: shop.Inn(),
                  FL_SUNDRIES: shop.Sundries(),
                  FL_AULOFICER: shop.Auloficer(),
                  FL_LUTHIER: shop.Luthier(),
                  FL_TAMBOURIER: shop.Tambourier(),
				  FL_SCRIPTORIUM: shop.Scriptorium(),
                  BATTLE: battle.Battle(),
                  INSTRUCTIONS: main_menu.Instructions(),
                  LOADGAME: main_menu.LoadGame(),
                  DEATH_SCENE: death.DeathScene(),
                  CREDITS: credits.Credits()
                  }

    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()
