def get_werewolves_moves(board_matrix, species_dict):
    # vampire coordinate
    source_coordinate = []
    opponent_coordinate = []
    human_coordinate = []
    target_coordinate = []

    source_move_bool = []
    num_species_to_move = []

    for x in range(board_matrix.shape[0]):
        for y in range(board_matrix.shape[1]):

            if board_matrix[x][y]['cell_werewolves_count'] > 0:
                source_coordinate.append(x)
                source_coordinate.append(y)

            if board_matrix[x][y]['cell_vampire_count'] > 0:
                opponent_coordinate.append(x)
                opponent_coordinate.append(y)

            if board_matrix[x][y]['cell_human_count'] > 0:
                human_coordinate.append(x)
                human_coordinate.append(y)

    # Calculate the target coordinate

    for index, coordinate in enumerate(source_coordinate):
        if index % 2 != 0:
            continue

        else:
            if source_coordinate[index] == board_matrix.shape[0] - 1:
                target_coordinate.append(source_coordinate[index] - 1)  # if going to hit bottom border, go up
                target_coordinate.append(source_coordinate[index + 1])  # working on y
                num_species_to_move.append(
                    board_matrix[source_coordinate[index]][source_coordinate[index + 1]]['cell_werewolves_count'])

            elif source_coordinate[index] == 0:  # same for upper border
                target_coordinate.append(source_coordinate[index] + 1)
                target_coordinate.append(source_coordinate[index + 1])
                num_species_to_move.append(
                    board_matrix[source_coordinate[index]][source_coordinate[index + 1]]['cell_werewolves_count'])

            else:
                target_coordinate.append(source_coordinate[index] + 1)
                target_coordinate.append(source_coordinate[index + 1])
                num_species_to_move.append(
                    board_matrix[source_coordinate[index]][source_coordinate[index + 1]]['cell_werewolves_count'])

    # Swapping the values
    source_coordinate[::2], source_coordinate[1::2] = source_coordinate[1::2], source_coordinate[::2]
    target_coordinate[::2], target_coordinate[1::2] = target_coordinate[1::2], target_coordinate[::2]

    total_num_moves = len(num_species_to_move)

    return total_num_moves, source_coordinate, target_coordinate, num_species_to_move, source_move_bool


# -----------------------------------------------------------------------------------------------------------------------------

def get_vampires_moves(board_matrix, species_dict):
    # vampire coordinate
    source_coordinate = []
    opponent_coordinate = []
    human_coordinate = []
    target_coordinate = []

    source_move_bool = []
    num_species_to_move = []

    for x in range(board_matrix.shape[0]):
        for y in range(board_matrix.shape[1]):

            if board_matrix[x][y]['cell_vampire_count'] > 0:
                source_coordinate.append(x)
                source_coordinate.append(y)

            if board_matrix[x][y]['cell_werewolves_count'] > 0:
                opponent_coordinate.append(x)
                opponent_coordinate.append(y)

            if board_matrix[x][y]['cell_human_count'] > 0:
                human_coordinate.append(x)
                human_coordinate.append(y)

    # Calculate the target coordinate
    for index, coordinate in enumerate(source_coordinate):
        if index % 2 != 0:
            continue

        else:
            if source_coordinate[index] == board_matrix.shape[0] - 1:
                target_coordinate.append(source_coordinate[index] - 1)
                target_coordinate.append(source_coordinate[index + 1])
                num_species_to_move.append(
                    board_matrix[source_coordinate[index]][source_coordinate[index + 1]]['cell_vampire_count'])

            elif source_coordinate[index] == 0:
                target_coordinate.append(source_coordinate[index] + 1)
                target_coordinate.append(source_coordinate[index + 1])
                num_species_to_move.append(
                    board_matrix[source_coordinate[index]][source_coordinate[index + 1]]['cell_vampire_count'])

            else:
                target_coordinate.append(source_coordinate[index] + 1)
                target_coordinate.append(source_coordinate[index + 1])
                num_species_to_move.append(
                    board_matrix[source_coordinate[index]][source_coordinate[index + 1]]['cell_vampire_count'])

    # Swapping the values
    source_coordinate[::2], source_coordinate[1::2] = source_coordinate[1::2], source_coordinate[::2]
    target_coordinate[::2], target_coordinate[1::2] = target_coordinate[1::2], target_coordinate[::2]

    total_num_moves = len(num_species_to_move)

    return total_num_moves, source_coordinate, target_coordinate, num_species_to_move, source_move_bool

# --------------------------------------------------------------------------------------------------------------------
