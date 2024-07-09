import os
from random import choice
from copy import deepcopy


board: list[list[str]] = [['[*]', '[*]', '[*]', '[*]'],
                          ['[*]', '[*]', '[*]', '[*]'],
                          ['[*]', '[*]', '[*]', '[*]'],
                          ['[*]', '[*]', '[*]', '[*]']]

last_printed: list[list[str]] = list()


def print_board(*, repeat: bool = False) -> None:
    """
    Prints the boards.

    :param repeat: should the board print if is has not changed since it was
    last printed.
    """
    global last_printed
    if last_printed == board and not repeat:
        return None

    print()
    for row in range(len(board)):
        for col in range(len(board[row])):
            print(board[row][col], end="")
        print()
    print()

    last_printed = deepcopy(board)


def match_presence_and_info(state: list[list[str]]) -> tuple[int, dict]:
    """
    Determine whether there is a match on the given board and return the 
    details of the match position.

    :param state: a 2-d array representing a board
    :return: a tuple containing a boolean which represents the presence
    of a match, and a dictionary containing the match position details
    """
    match_present: bool = False
    match_info: dict[str: tuple] = {"high": (-1, -1), "low":(-1, -1), "left":(-1, -1), "right":(-1, -1)}

    for row in range(len(state)):
        for col in range(len(state[row])):
            current: str = state[row][col]
            if current == "[*]":
                continue

            # check for vertical match
            down_search_index: int = row + 1
            while down_search_index < len(state) and state[down_search_index][col] == current:
                down_search_index += 1
            lowest_point: int = down_search_index - 1

            up_search_index: int = row - 1
            while up_search_index > -1 and state[up_search_index][col] == current:
                up_search_index -= 1
            highest_point: int = up_search_index + 1

            chain_length: int = lowest_point - highest_point + 1
            if chain_length >= 3:
                match_present = True
                match_info["high"] = (highest_point, col)
                match_info["low"] = (lowest_point, col)

            # check for a horizontal match
            right_search_index: int = col + 1
            while right_search_index < len(state[row]) and state[row][right_search_index] == current:
                right_search_index += 1
            rightmost_point: int = right_search_index - 1

            left_search_index: int = col - 1
            while left_search_index > -1 and state[row][left_search_index] == current:
                left_search_index -= 1
            leftmost_point: int = left_search_index + 1

            chain_length = rightmost_point - leftmost_point + 1
            if chain_length >= 3:
                match_present = True
                match_info["left"] = (row, leftmost_point)
                match_info["right"] = (row, rightmost_point)

    return match_present, match_info


def check_current_match(state: list[list[str]]) -> bool:
    """
    Determine only whether a match is present, without generating match details.

    :param state: a 2-d array representing a board
    :return: whether a match is present
    """
    match_data: tuple = match_presence_and_info(state)
    return match_data[0]


def check_potential_match() -> bool:
    """
    Determine whether a possible match exists on the board.

    :return: whether a possible match exists
    """
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "[*]":
                continue
            # check if upward swipe will produce a match
            if row > 0:
                temp: list[list[str]] = deepcopy(board)
                temp[row][col], temp[row-1][col] = temp[row-1][col], temp[row][col]
                match_present: bool = check_current_match(temp)
                if match_present:
                    return True
            
            # check if downward swipe will produce a match
            if row < len(board)-1:
                temp = deepcopy(board)
                temp[row][col], temp[row+1][col] = temp[row+1][col], temp[row][col]
                match_present = check_current_match(temp)
                if match_present:
                    return True      

            # check if leftward swipe will produce a match         
            if col > 0:
                temp = deepcopy(board)
                temp[row][col], temp[row][col-1] = temp[row][col-1], temp[row][col]
                match_present = check_current_match(temp)
                if match_present:
                    return True
            
            # check if rightward swipe will produce a match
            if col < len(board[row])-1:
                temp = deepcopy(board)
                temp[row][col], temp[row][col+1] = temp[row][col+1], temp[row][col]
                match_present = check_current_match(temp)
                if match_present:
                    return True
    return False            


def initialize_board() -> None:
    """
    Generate a random starting board.
    """
    letters: list[str] = ['A', 'D', 'F', 'G', 'X']
    for row in range(len(board)):
        for col in range(len(board[row])):
            board[row][col] = f"[{choice(letters)}]"
    match_present: bool = check_current_match(board)
    potential_match: bool = check_potential_match()

    while match_present or not potential_match:
        for row in range(len(board)):
            for col in range(len(board[row])):
                board[row][col] = f"[{choice(letters)}]"

        match_present = check_current_match(board)
        potential_match = check_potential_match()


def swipe(cellspace: int, direction: str) -> None:
    """
    Swipe the contents of a cell space in a given direction.

    :param cellspace: the position on the board to be swiped.
    :param direction: the direction to swipe in.
    """
    global board

    row: int = int(cellspace // 4.1)
    col: int = (cellspace % 4) - 1 if cellspace%4 else 3

    temp: list[list[str]] = deepcopy(board)

    match direction.lower().strip():
        case 'w':
            if row == 0:
                print("\ncannot swipe\n")
                return None
            temp[row][col], temp[row-1][col] = temp[row-1][col], temp[row][col]
        case 's':
            if row == len(board)-1:
                print("\ncannot swipe\n")
                return None
            temp[row][col], temp[row+1][col] = temp[row+1][col], temp[row][col]
        case 'a':
            if col == 0:
                print("\ncannot swipe\n")
                return None
            temp[row][col], temp[row][col-1] = temp[row][col-1], temp[row][col]
        case 'd':
            if col == len(board[0])-1:
                print("\ncannot swipe\n")
                return None
            temp[row][col], temp[row][col+1] = temp[row][col+1], temp[row][col]

    
    match_data = match_presence_and_info(temp)
    match_present = match_data[0]
    if match_present:
        #handle match
        board = deepcopy(temp)
        handle_all_matches()
    else:
        print("\nno match\n")


def handle_match(info: dict[str: tuple[int]]) -> None:
    """
    Given certain match details, remove a match from the board and replace each
    cell letter with '*'.

    :param info: a dictionary containing the postions of the match.
    """
    #vertical
    high_point, low_point = info["high"], info["low"]

    if high_point[0] != -1:
        col: int = high_point[1]
        for row_val in range(high_point[0], low_point[0]+1):
            board[row_val][col] = f"[*]"

    # horizontal
    left_point, right_point = info["left"], info["right"]

    if left_point[0] != -1:
        row: int = left_point[0]
        for col_val in range(left_point[1], right_point[1]+1):
            board[row][col_val] = f"[*]"


def handle_all_matches() -> None:
    """
    Handle all matches on the board.
    """
    match_data: tuple[bool, dict] = match_presence_and_info(board)
    match_present: bool = match_data[0]
    match_info: dict[str: tuple[int]] = match_data[1]

    while match_present:
        handle_match(match_info)

        match_data: tuple[bool, dict] = match_presence_and_info(board)
        match_present: bool = match_data[0]
        match_info: dict[str: tuple[int]] = match_data[1]
   

def drop_floating_letters() -> None:
    """
    Drop any floating letters into their proper postion.
    """
    for row in range(len(board)-2, -1, -1):
        for col in range(len(board[row])):
            if board[row][col] == "[*]":
                continue

            pointer: int = row + 1
            while pointer < len(board) and board[pointer][col] == "[*]":
                pointer += 1
            switch: int = pointer - 1

            board[row][col], board[switch][col] = board[switch][col], board[row][col]

    match_data: tuple[bool, dict] = match_presence_and_info(board)
    match_present: bool = match_data[0]
    while match_present:
        print_board()
        handle_all_matches()
        print_board()
        drop_floating_letters()
        print_board()
        match_data: tuple[bool, dict] = match_presence_and_info(board)
        match_present: bool = match_data[0]


def replace_matched_letters() -> None:
    """
    Replaces all '*' cell spaces with new letters, ensuring a possible match
    is present.
    """
    global board
    board_copy: list[list[str]] = deepcopy(board)
    letters: list[str] = ['A', 'D', 'F', 'G', 'X']
    for row in range(len(board)):
        for col in range(len(board[row])):
            current: str = board[row][col]
            if current == "[*]":
                board[row][col] = f"[{choice(letters)}]"
    possible_match: bool = check_potential_match()

    while not possible_match:
        board = deepcopy(board_copy)
        for row in range(len(board)):
            for col in range(len(board[row])):
                current: str = board[row][col]
                if current == "[*]":
                    board[row][col] = f"[{choice(letters)}]"
        possible_match: bool = check_potential_match()

    match_data: tuple[bool, dict] = match_presence_and_info(board)
    match_present: bool = match_data[0]
    while match_present:
        print_board()
        handle_all_matches()
        print_board()
        drop_floating_letters()
        print_board()
        replace_matched_letters()
        match_data: tuple[bool, dict] = match_presence_and_info(board)
        match_present: bool = match_data[0]


if __name__ == "__main__":
    print("Match 3")
    print("-------")
    print("This program recreates the basic mechanics of a match 3 game on a 4x4 grid.\n"
          "Enter a position on the board, the numbering starts as 1 in the top left and ends at 16 in the bottom right.\n"
          "Then enter a direction to swipe in using the 'W/A/S/D' keys.\n"
          "Enter 'exit' to exit the program.")

    initialize_board()
    print_board()

    while True:
        while True:
            cell_space: str = input("Enter a cell space(1-16): ").lower().strip()

            if cell_space == "exit":
                os._exit(1)

            try: 
                cell_space: int = int(cell_space)
            except ValueError:
                print("Invalid Input: Enter a number from 1-16.\n")
            else: 
                if cell_space < 1 or cell_space > 16:
                    print("Invalid Input: Space number out of bounds.\n")
                else: break

        while True:
            direction: str = input("Enter a direction: ").lower().strip()

            if direction == "exit":
                os._exit(1)

            if direction not in ('w', 'a', 's', 'd'):
                print("Invalid Input: Invalid direction. Enter W/A/S/D.\n")
            else: break
            
        swipe(cell_space, direction)
        print_board()
        drop_floating_letters()
        print_board()
        replace_matched_letters()
        print_board()
