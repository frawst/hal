"""

GOAL:

1. Know where everyone is
  a) How many ships
  b) Which planets
  c) Where do I stand?

2. Know what planets are around
  a) how far from me and opponents
  b) 'easiness' rating for capture
    - Take a value for it's distance from me vs. from opponents

"""
# People
import hlt
import logging
from math import sqrt

game = hlt.Game("Settler")
logging.info("Starting my Settler bot!")

def set_speed_by_dist(ship):
    dist = ship.calculate_distance_between(ship.closest_point_to(planet))
    if (dist < 15):
        return (hlt.constants.MAX_SPEED - 1)
    elif (dist < 5):
        return hlt.constants.MAX_SPEED/2
    else:
        return hlt.constants.MAX_SPEED


while True:
    game_map = game.update_map()
    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    planet_list = []
    planet_attacked = []
    if planet_list.__len__ == 0:
        for planet in game_map.all_planets():
            planet_list.append(planet.id)
            planet_attacked.append(False)

    logging.info("All planets: " + game_map.all_planets())

    for ship in game_map.get_me().all_ships():
        logging.info("Ent by Dist. to X Ship: " + game_map.nearby_entities_by_distance())
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        for planet in game_map.all_planets():

            if planet.is_owned():
                continue

            if ship.can_dock(planet) and not planet_attacked[planet_list.index(planet.id)]:
                command_queue.append(ship.dock(planet))
                planet_attacked[planet_list.index(planet.id)] = True

            else:

                navigate_command = ship.navigate(
                    ship.closest_point_to(planet),
                    game_map,
                    speed=int(set_speed_by_dist(ship)),
                    ignore_ships=True)

                if navigate_command:
                    command_queue.append(navigate_command)
            break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END