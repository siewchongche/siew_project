import numpy as np

def sudokusolver(raw_data):

    # Append into board list and convert to numpy array
    board = []
    row_list = raw_data.split(',')
    for row in row_list:
        temp_list = [int(num) for num in row]
        board.append(temp_list)
    board_arr = np.array(board)

    # Function of convert each row and each column from board into dict respectively
    def row_col_dict(board_arr):
        # Dict for each row in board_arr
        row_dict = {}
        for row_num in range(9):
            row_dict[row_num] = board_arr[row_num, :]

        # Dict for each col in board_arr
        col_dict = {}
        for col_num in range(9):
            col_dict[col_num] = board_arr[:, col_num]

        return row_dict, col_dict

    infinity_loop = 0 # To detect whether sudoku can be solved
    error = False
    while 0 in board_arr: # Loop until all empty square solve

        def sudoku_solver(board_arr, direction):
                                    
            is_fit = False # Initial define for whether their is solution in sudoku_solver function 

            # Define direction dict
            row_dict, col_dict = row_col_dict(board_arr)
            direction_dict = row_dict if direction == 'row' else col_dict

            # Define each block from board_arr (3 x 3 square)
            global complete_block_dict # Make global for infinity loop section
            complete_block_dict = {
                'blockA': board_arr[:3, :3], 'blockB': board_arr[:3, 3:6], 'blockC': board_arr[:3, 6:9],
                'blockD': board_arr[3:6, :3], 'blockE': board_arr[3:6, 3:6], 'blockF': board_arr[3:6, 6:9],
                'blockG': board_arr[6:9, :3], 'blockH': board_arr[6:9, 3:6], 'blockI': board_arr[6:9, 6:9]
            }

            # Loop through each direction
            for key_index in direction_dict:
                # Arrange out assume list
                opp_direction_index = 0 # If direction = row, opp_direction_index = column index
                assume_dict = {}
                for each_square in direction_dict[key_index]:
                    # Define opposite_direction
                    if direction == 'row':
                        opposite_direction = board_arr[:, opp_direction_index]
                    elif direction == 'col':
                        opposite_direction = board_arr[opp_direction_index, :]

                    if each_square == 0: # Empty square 
                        assume_list = []
                        for assume in range(1, 10):
                            # Assume number not in other confirm squares within same direction
                            if assume not in direction_dict[key_index]:
                                # Assume number not in other confirm squares within each_square's opposite direction
                                if assume not in opposite_direction:
                                    # Define 3x3 block area based on key_index and opp_direction_index
                                    if key_index in (0, 1, 2):
                                        if opp_direction_index in (0, 1, 2):
                                            block = 'blockA'
                                        if opp_direction_index in (3, 4, 5):
                                            block = 'blockB' if direction == 'row' else 'blockD'
                                        if opp_direction_index in (6, 7, 8):
                                            block = 'blockC' if direction == 'row' else 'blockG'
                                    if key_index in (3, 4, 5):
                                        if opp_direction_index in (0, 1, 2):
                                            block = 'blockD' if direction == 'row' else 'blockB'
                                        if opp_direction_index in (3, 4, 5):
                                            block = 'blockE'
                                        if opp_direction_index in (6, 7, 8):
                                            block = 'blockF' if direction == 'row' else 'blockH'
                                    if key_index in (6, 7, 8):
                                        if opp_direction_index in (0, 1, 2):
                                            block = 'blockG' if direction == 'row' else 'blockC'
                                        if opp_direction_index in (3, 4, 5):
                                            block = 'blockH' if direction == 'row' else 'blockF'
                                        if opp_direction_index in (6, 7, 8):
                                            block = 'blockI'

                                    # Assume number not in other confirm square within 3x3 block
                                    if assume not in complete_block_dict[block]:
                                        assume_list.append(assume)
                                        # Insert/replace possible answer into assume dict with opp direction index as key
                                        assume_dict[opp_direction_index] = assume_list 

                    opp_direction_index += 1

                # Done for each direction dict(key_index) in board
                # Find the answer(only number) in assume list and answer's opp_direction_index(as index for insert answer)
                for assume in range(1, 10):
                    temp = ''
                    for key in assume_dict:
                        if assume in assume_dict[key]: # Assume number in assume_list
                            if assume != temp: # Not duplicate
                                temp = assume # Assume number store into temp for later duplicate checking
                            else:
                                # There is duplicate for the assume number, so it's not the answer
                                # Reset the temp, and break the assume_dict loop
                                temp = ''
                                break

                    if temp != '': # The assume is the only number
                        answer = temp
                        # Find opp_direction_index of answer
                        for key in assume_dict:
                            if answer in assume_dict[key]:
                                answer_index_of_opp_direction = key # answer_index_of_opp_direction example: if row, index of answer's column

                        if direction == 'row':
                            board_arr[key_index, answer_index_of_opp_direction] = answer # Insert answer into board_arr[row, column]
                            # print(f'--->Row {key_index+1}, Column {answer_index_of_opp_direction+1} = {answer}') # For debugging
                        elif direction == 'col':
                            board_arr[answer_index_of_opp_direction, key_index] = answer # Insert answer into board_arr[row, column]
                            # print(f'--->Row {answer_index_of_opp_direction+1}, Column {key_index+1} = {answer}') # For debugging

                        is_fit = True # Answer been fit into corresponding empty square

            return board_arr, is_fit

        # --- Main sudoku solver section --- #
        board_arr, is_fit_row = sudoku_solver(board_arr, 'row')
        board_arr, is_fit_col = sudoku_solver(board_arr, 'col')

        # --- Below is infinity loop section --- #
        # Both row and col of sudoku solver fail to fit answer
        if is_fit_row == False and is_fit_col == False:
            infinity_loop += 1 # Set times of infinity loop (over 2 times = sudoku failed to solve)
            # print('--------------- Infinity loop occured ---------------') # For debugging

            board_arr_temp = board_arr.copy() # Backup board_arr before guess_square in case guess fail

            # Sudoku solved if board_completed == True
            global board_completed # Make global to change bool status if sudoku solved within while loop
            board_completed = False

            # ----- Find empty square to test ----- #
            r_index = 0
            for row in board_arr:
                if board_completed: # Sudoku solved, no need to continue the loop
                    break

                # print(f'Now in row {r_index+1}') # For debugging
                c_index = 0
                for square in row:
                    if board_completed: # Sudoku solved, no need to continue the loop
                        break

                    # print(f'Now in row {r_index+1} col {c_index+1}') # For debugging
                    if square == 0: # Empty square
            # ----- End finding ----- #

                        # ----- Check guess number not in row, column and block ----- #
                        for guess in range(1, 10):
                            if board_completed: # Sudoku solved, no need to continue the loop
                                break

                            # print(f'Now guess for number {guess}') # For debugging
                            if guess not in board_arr[r_index, :]: # Guess not in other confirmed square in same row
                                if guess not in board_arr[:, c_index]: # Guess not in other confirmed square in c_index's column
                                    # Define 3x3 block based on corresponding row index and column index
                                    if r_index in (0, 1, 2):
                                        if c_index in (0, 1, 2):
                                            block = 'blockA'
                                        if c_index in (3, 4, 5):
                                            block = 'blockB'
                                        if c_index in (6, 7, 8):
                                            block = 'blockC'
                                    if r_index in (3, 4, 5):
                                        if c_index in (0, 1, 2):
                                            block = 'blockD'
                                        if c_index in (3, 4, 5):
                                            block = 'blockE'
                                        if c_index in (6, 7, 8):
                                            block = 'blockF'
                                    if r_index in (6, 7, 8):
                                        if c_index in (0, 1, 2):
                                            block = 'blockG'
                                        if c_index in (3, 4, 5):
                                            block = 'blockH'
                                        if c_index in (6, 7, 8):
                                            block = 'blockI'
                                    # Guess not in other confirmed square in corresponding 3x3 block
                                    if guess not in complete_block_dict[block]:
                        # ----- End checking ----- #

                                        # Insert guess number into test board
                                        board_arr_temp[r_index, c_index] = guess
                                        # print(f'Guess {guess} in row {r_index+1}, col {c_index+1}') # For debugging

                                        # ----- Test guess number in board ----- #
                                        while 0 in board_arr_temp: # Loop until all empty square fill with answer
                                            board_arr_temp, is_fit_row = sudoku_solver(board_arr_temp, 'row')
                                            # print(f'is_fit_row = {is_fit_row}') # For debugging
                                            board_arr_temp, is_fit_col = sudoku_solver(board_arr_temp, 'col')
                                            # print(f'is_fit_col = {is_fit_col}') # For debugging

                                            # ----- Expert level sudoku solver ----- #
                                            # Unsolved. Reserved for future expansion
                                            # if infinity_loop == 2: # First test failed. Infinity loop code run for second times
                                            #     board_arr_temp, is_fit_row = sudoku_solver(board_arr_temp, 'row')
                                            #     board_arr_temp, is_fit_col = sudoku_solver(board_arr_temp, 'col')
                                            # ----- End for expert level sudoku solver ----- #
                                            
                                            # Both sudoku solver for row and col failed, so assume that guess number is wrong
                                            if is_fit_row == False and is_fit_col == False:
                                                # Reset the board to status before infinity section
                                                board_arr_temp = board_arr.copy()
                                                break # Guess number wrong, break while loop

                                            # All empty square in board fill with answer
                                            if 0 not in board_arr_temp:
                                                # Replace test board to original board(before infinity loop section)
                                                board_arr = board_arr_temp.copy()
                                                board_completed = True
                                                break # Board completed fill with answer, break while loop
                                        # ----- End testing ----- #

                                    else:
                                        # print(f'Number {guess} cannot fit into row {r_index+1} col {c_index+1}') # For debugging
                                        pass

                                else:
                                    # print(f'Number {guess} cannot fit into row {r_index+1} col {c_index+1}') # For debugging
                                    pass

                            else:
                                # print(f'Number {guess} cannot fit into row {r_index+1} col {c_index+1}') # For debugging
                                pass

                    else:
                        # print(f'Square no. {c_index+1} is not 0 ({square}/{board_arr[r_index, c_index]})') # For debugging
                        pass

                    c_index += 1 # Next column index
                r_index += 1 # Next row index

        # For debugging
        # print('-----Main board-----')
        # print(board_arr)
        # print('--------------------')

        if infinity_loop > 1: # More than 1 times infinity loop: program failed to solve the board
            error = True
            break # Break while loop and end program

        # input('Please ENTER to continue...') # For debugging

    # Convert into rowInString for each row and a list for contain all rowInString for frontend purpose
    raw_data_list = []
    temp = ''
    for row in board_arr:
        for each in row:
            temp += str(each)
        raw_data_list.append(temp)
        temp = ''

    return raw_data_list, error