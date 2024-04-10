class Ship:
    def __init__(self, length, start_pos, orientation):
        """
        Initializes a new ship with a given length, starting position, and orientation.

        :param length: Length of the ship (number of cells it occupies on the board).
        :param start_pos: Starting position of the ship on the board (row, column).
        :param orientation: Orientation of the ship ('horizontal' or 'vertical').
        """
        self.length = length
        self.start_pos = start_pos
        self.orientation = orientation
        self.hits = 0  # Number of times the ship has been hit

    def positions(self):
        """
        Returns a list of all positions occupied by the ship on the board.
        """
        positions = []
        for i in range(self.length):
            if self.orientation == 'horizontal':
                positions.append((self.start_pos[0], self.start_pos[1] + i))
            else:  # vertical
                positions.append((self.start_pos[0] + i, self.start_pos[1]))
        return positions

    def hit(self):
        """
        Marks the ship as being hit. Increases the hit count.
        """
        self.hits += 1

    def is_sunk(self):
        """
        Checks if the ship is sunk (i.e., hit count equals its length).

        :return: True if the ship is sunk, False otherwise.
        """
        return self.hits == self.length

# Example of creating a ship and managing hits
if __name__ == "__main__":
    # Creating a battleship of length 4, starting at position (2, 2), oriented horizontally
    battleship = Ship(length=4, start_pos=(2, 2), orientation='horizontal')
    print("Positions occupied by battleship:", battleship.positions())

    # Simulating hits on the battleship
    battleship.hit()
    battleship.hit()
    print("Is the battleship sunk?", battleship.is_sunk())

    # More hits
    battleship.hit()
    battleship.hit()  # Now it should be sunk
    print("Is the battleship sunk after 4 hits?", battleship.is_sunk())
