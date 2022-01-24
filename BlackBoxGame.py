# Author: Edward Yeung
# Date: 08/6/20
# Description: CS 162 Portfolio Project, creating a BlackBoxGame


class BlackBoxGame:
    """
    Creating a single player 10x10 blackbox game that begins with 25 points
    Currently only implementing one class that will handle all game functionality
    """
    def __init__(self, atom_list):
        self._atoms = atom_list     # stores list of input Atom positions
        self._board_game = []
        self._player_score = 25
        self.add_atom()
        self.atom_guess = []
        self.ray_entry_exit = []  # stores ray entry and exit positions
        self.border_square_list = []
        self.border_square()

    def border_square(self):
        """ Creates the valid border square values and stores them in a list """
        for num in range(1, 9):
            self.border_square_list.append((0, num))
            self.border_square_list.append((9, num))
            self.border_square_list.append((num, 0))
            self.border_square_list.append((num, 9))

    def print_board(self):
        """ Displays current state of game board """
        for i in self._board_game:
            print(*i, sep=" ")

    def add_atom(self):
        """ Adds user input atom location to game board """
        for i in range(10):
            self._board_game.append(["-"] * 10)
        for atoms in self._atoms:
            self._board_game[atoms[0]][atoms[1]] = "A"

    def shoot_ray(self, row, column):
        """ Inputs starting location of a ray into the board and determines if hit, or deflection and updates
            player's score
            This method will call upon other methods to check for deflection/hit/miss detour conditions """
        if (row, column) not in self.border_square_list:        # Checks if ray input is valid
            return False
        if (row, column) not in self.ray_entry_exit:        # Deducts player score if ray input was used
            self._player_score -= 1
        self.ray_entry_exit.append((row, column))           # Stores ray entry to list
        self._board_game[row][column] = "X"

        if row == 0:
            return self.ray_deflection_row_down(row, column)
        elif row == 9:
            return self.ray_deflection_row_up(row, column)
        elif column == 0:
            return self.ray_deflection_column_right(row, column)
        elif column == 9:
            return self.ray_deflection_column_left(row, column)

    def ray_deflection_row_down(self, row, column):
        """ Checks game board for atom's and moves downwards across rows
            Returns None if Atom is hit, else returns tuple of exit ray if miss """
        for row_i in range(row, 9):
            if row == 0 and (self._board_game[1][column-1] == "A" or self._board_game[1][column+1] == "A"):
                return None
            if self._board_game[row_i + 1][column - 1] == "A" and self._board_game[row_i + 1][column + 1] == "A":
                return self.ray_deflection_row_up(row_i, column)
            elif self._board_game[row_i + 1][column - 1] == "A":
                return self.ray_deflection_column_right(row_i, column)
            elif self._board_game[row_i + 1][column + 1] == "A":
                return self.ray_deflection_column_left(row_i, column)
            elif self._board_game[row_i + 1][column] == "A":
                return None
        exit_ray = (9, column)
        if exit_ray not in self.ray_entry_exit:
            self._player_score -= 1
            self.ray_entry_exit.append(exit_ray)
        return exit_ray

    def ray_deflection_row_up(self, row, column):
        """ Checks game board for atom's and moves upwards across rows
            Returns None if Atom is hit, else returns tuple of exit ray if miss """
        for row_i in range(row, 0, -1):
            if row == 9 and (self._board_game[8][column-1] == "A" or self._board_game[8][column+1] == "A"):
                return None
            if self._board_game[row_i - 1][column - 1] == "A" and self._board_game[row_i][column + 1] == "A":
                return self.ray_deflection_row_down(row_i, column)
            elif self._board_game[row_i - 1][column - 1] == "A":
                return self.ray_deflection_column_right(row_i, column)
            elif self._board_game[row_i - 1][column + 1] == "A":
                return self.ray_deflection_column_left(row_i, column)
            elif self._board_game[row_i - 1][column] == "A":
                return None
        exit_ray = (0, column)
        if exit_ray not in self.ray_entry_exit:
            self._player_score -= 1
            self.ray_entry_exit.append(exit_ray)
        return exit_ray

    def ray_deflection_column_right(self, row, column):
        """ Checks game board for atom's and moves to the right across columns
            Returns None if Atom is hit, else returns tuple of exit ray if miss """
        for column_i in range(column, 9):
            if column == 0 and (self._board_game[row - 1][1] == "A" or self._board_game[row + 1][1] == "A"):
                return None
            elif self._board_game[row - 1][column_i + 1] == "A" and self._board_game[row + 1][column_i + 1] == "A":
                return self.ray_deflection_column_left(row, column_i)
            elif self._board_game[row - 1][column_i + 1] == "A":
                return self.ray_deflection_row_down(row, column_i)
            elif self._board_game[row + 1][column_i + 1] == "A":
                return self.ray_deflection_row_up(row, column_i)
            elif self._board_game[row][column_i + 1] == "A":
                return None
        exit_ray = (row, 9)
        if exit_ray not in self.ray_entry_exit:
            self._player_score -= 1
            self.ray_entry_exit.append(exit_ray)
        return exit_ray

    def ray_deflection_column_left(self, row, column):
        """ Checks game board for atom's and moves to the left across columns
            Returns None if Atom is hit, else returns tuple of exit ray if miss """
        for column_i in range(column, 0, -1):
            # checks for edge reflection
            if column == 9 and (self._board_game[row - 1][8] == "A" or self._board_game[row + 1][8] == "A"):
                return None
            elif self._board_game[row - 1][column_i - 1] == "A" and self._board_game[row + 1][column_i - 1] == "A":
                return self.ray_deflection_column_right(row, column_i)
            elif self._board_game[row - 1][column_i - 1] == "A":
                return self.ray_deflection_row_down(row, column_i)
            elif self._board_game[row + 1][column_i - 1] == "A":
                return self.ray_deflection_row_up(row, column_i)
            elif self._board_game[row][column_i - 1] == "A":
                return None
        exit_ray = (row, 0)
        if exit_ray not in self.ray_entry_exit:
            self._player_score -= 1
            self.ray_entry_exit.append(exit_ray)
        return exit_ray

    def guess_atom(self, row, column):
        """ Takes input location to guess an atom and return True if correct, otherwise returns false and updates
            player's score """

        for atom in self._atoms:
            if (row, column) == atom:
                self.atom_guess.append((row, column))
                self._atoms.remove((row, column))
                return True
            elif (row, column) in self.atom_guess:
                return False
            else:
                self._player_score -= 5
                self.atom_guess.append((row, column))
                return False

    def get_score(self):
        """ Returns the players current score """
        return self._player_score

    def atoms_left(self):
        """ Returns the number of atoms currently left on the game board """
        return len(self._atoms)


game = BlackBoxGame([(3,2),(1,7),(4,6),(8,8)])
move_result = game.shoot_ray(3,9)

game.shoot_ray(0,2)
print(game.get_score())