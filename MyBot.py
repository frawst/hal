
import hlt
import logging
import math
from random import randint

game = hlt.Game("HAL2001")
logging.info("HAL2001 Boot Success.")

visited_planets = []
planned_planets = []

travel_ratio = 0.4

tick = 0

while True:
    
    game_map = game.update_map()
    tick += 1
    max_dist = math.sqrt((game_map.width ** 2) + (game_map.height ** 2))

    command_queue = []
    
    
    if (tick % 15 == 0):
        visited_planets = []
        
    if (tick % 30 == 0):
        planned_planets = []
   
    
    for ship in game_map.get_me().all_ships():
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue
            

        for planet in game_map.all_planets():
        
            if (planet.calculate_distance_between(ship) >= max_dist * travel_ratio):
                continue
                    
            if planet.is_owned():
                # Skip this planet
                continue

            if ship.can_dock(planet):
                command_queue.append(ship.dock(planet))
                visited_planets.append(planet)

            elif planet not in planned_planets:

                navigate_command = ship.navigate(
                    ship.closest_point_to(planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=True)

                if navigate_command:
                    command_queue.append(navigate_command)
                    planned_planets.append(planet)

            
            break

    game.send_command_queue(command_queue)
    # TURN END
# GAME END