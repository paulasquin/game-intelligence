def update_board_matrix(board_matrix, agent_state):
    board_info = list(agent_state['map_commands_raw'])

    print(board_info)
    for i in range(len(board_info)):
        if i % 5 == 0:
            temp_dict = {'cell_human_count': board_info[i + 2], 'cell_vampire_count': board_info[i + 3],
                         'cell_werewolves_count': board_info[i + 4]}
            board_matrix[board_info[i + 1]][board_info[i]] = temp_dict

    return board_matrix


def identify_species(board_matrix, agent_state):
    x_initial = agent_state['start_position'][0]
    y_initial = agent_state['start_position'][1]
    temp_dict = board_matrix[y_initial][x_initial]

    if temp_dict['cell_vampire_count'] > 0:
        species_dict = {'our_species': 'vampires', 'opponent_species': 'werewolves'}
    elif temp_dict['cell_werewolves_count'] > 0:
        species_dict = {'our_species': 'werewolves', 'opponent_species': 'vampires'}
    else:
        raise NameError("Can't guess our species")

    return species_dict
