import random
from settings import grid_size, ships_lengths

def generate_random_ship_position(length):
    """
    Generates a random position for a ship of given length.
    Ensures the ship fits within the game board.

    :param length: The length of the ship.
    :return: A tuple containing the starting position (row, col), and orientation ('horizontal' or 'vertical').
    """
    orientation = random.choice(['horizontal', 'vertical'])
    if orientation == 'horizontal':
        row = random.randint(0, grid_size - 1)
        col = random.randint(0, grid_size - length)
    else:
        row = random.randint(0, grid_size - length)
        col = random.randint(0, grid_size - 1)
    
    return (row, col), orientation

def check_overlap(ship_position, existing_ships,length):
    """
    Checks if a newly generated ship position overlaps with any existing ships.

    :param ship_position: The position and orientation of the new ship (as returned by generate_random_ship_position).
    :param existing_ships: A list of positions and orientations of already placed ships.
    :return: True if there is an overlap, False otherwise.
    """
    new_ship_cells = get_ship_cells(ship_position[0], ship_position[1], length)
    for existing_ship in existing_ships:
        existing_ship_cells = get_ship_cells(existing_ship[0], existing_ship[1], existing_ship[2])
        if set(new_ship_cells) & set(existing_ship_cells):  # Check for intersection
            return True
    return False

def get_ship_cells(start_pos, orientation, length):
    """
    Generates a list of cells occupied by a ship given its start position, orientation, and length.

    :param start_pos: The starting position of the ship (row, col).
    :param orientation: The orientation of the ship ('horizontal' or 'vertical').
    :param length: The length of the ship.
    :return: A list of tuples representing the cells occupied by the ship.
    """
    cells = []
    for i in range(length):
        if orientation == 'horizontal':
            cells.append((start_pos[0], start_pos[1] + i))
        else:  # vertical
            cells.append((start_pos[0] + i, start_pos[1]))
    return cells

def generate_fleet_positions():
    """
    Generates non-overlapping positions for a fleet based on the game's ship lengths.

    :return: A list of ship positions and orientations for the entire fleet.
    """
    fleet_positions = []
    for length in ships_lengths:
        while True:
            position, orientation = generate_random_ship_position(length)
            if not check_overlap((position, orientation, length), fleet_positions):
                fleet_positions.append((position, orientation, length))
                break
    return fleet_positions
