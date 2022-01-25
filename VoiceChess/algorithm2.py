from math import ceil
from computerLogic import *


class Node:
    def __init__(self, board) -> None:
        self.state = board
        self.children = []
        self.parent = None


class Algorithm2:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_best_move(curr_node: Node, nodes_to_be_passed):

        board = Heuristic.optimized_minimax(
            curr_node.state, 0, curr_node.state.computer_color, -1000000, 1000000, -1, -1, nodes_to_be_passed)
        return board

    @staticmethod
    def simulation(curr_node: Node, model, color_str):

        all_moves = curr_node.state.get_possible_moves(color_str)

        if len(all_moves) == 0:
            if curr_node.state.check_if_it_is_check(color_str):
                return -100000
            else:
                return 0

        map_state_move = dict()

        for i in all_moves:
            child = Node(i)
            child.parent = curr_node
            curr_node.children.append(child)
            map_state_move[child] = i

        expanded_nodes = []
        not_expanded_nodes = list(set(curr_node.children) - set(expanded_nodes))

        nodes_to_be_passed = []
        for i in range(0, 5):
            sel_child = Algorithm2.get_best_move_according_to_nn(not_expanded_nodes, model, color_str)
            nodes_to_be_passed.append(sel_child.state)
            expanded_nodes.append(sel_child)
            not_expanded_nodes = list(set(curr_node.children) - set(expanded_nodes))

        for i in range(0, 5):
            sel_child = Algorithm2.get_additional_move_according_to_nn(not_expanded_nodes, model, color_str)
            nodes_to_be_passed.append(sel_child.state)
            expanded_nodes.append(sel_child)
            not_expanded_nodes = list(set(curr_node.children) - set(expanded_nodes))

        choosen_move = Algorithm2.get_best_move(curr_node, nodes_to_be_passed)

        return choosen_move

    @staticmethod
    def get_best_moves_nn_and_heuristic_combined(boards, model, color_str):

        choosen_boards = Heuristic.get_best_moves_according_to_heuristic(boards, True, ceil(len(boards) / 2))
        all_moves_on_depth_2 = {}
        all = []

        map_of_boards = {}

        counter = 0
        for board in choosen_boards:
            all_moves_on_depth_2[str(counter)] = board.get_possible_moves(color_str)
            all_moves_on_depth_2[str(counter)] = Heuristic.get_best_moves_according_to_heuristic(
                all_moves_on_depth_2[str(counter)],
                False, ceil(len(all_moves_on_depth_2[str(counter)]) / 2))
            map_of_boards[str(counter)] = board
            all += all_moves_on_depth_2[str(counter)]
            counter += 1

        expanded_nodes = []

        nodes_to_be_passed = []

        for i in range(0, 3):

            max_percentage = -inf
            selected_el = None
            for el in all_moves_on_depth_2.keys():
                not_expanded_nodes = list(all_moves_on_depth_2[el] - set(expanded_nodes))
                value = Algorithm2.get_best_move_according_to_nn_percentage(not_expanded_nodes, model, color_str)
                if value > max_percentage:
                    max_percentage = value
                    selected_el = map_of_boards[el]

            nodes_to_be_passed.append(selected_el)
            expanded_nodes.append(selected_el)

        return nodes_to_be_passed

    @staticmethod
    def get_best_move_according_to_nn_percentage(possible_moves, model, color_str):

        results = {}

        for child in possible_moves:
            results[child] = model.predict(
                convert_matrix_to_array(child.state.fields, child.state.computer_color == color_str).reshape((1, 768)))

        best_results = list(results.keys())

        max_percentage = -inf
        for el in best_results:
            value = results[el][0][2]
            if value > max_percentage:
                max_percentage = value

        return max_percentage

    @staticmethod
    def get_best_move_according_to_nn(possible_moves, model, color_str):

        results = {}

        for child in possible_moves:
            results[child] = model.predict(
                convert_matrix_to_array(child.state.fields, WHITE_COLOR == color_str).reshape((1, 768)))

        flag = 0

        best_results = list(filter(lambda key: (np.argmax(results[key]) == 2), list(results.keys())))
        if len(best_results) == 0:
            flag = 1
            best_results = list(filter(lambda key: (np.argmax(results[key]) == 1), list(results.keys())))
            if len(best_results) == 0:
                flag = 2
                best_results = list(results.keys())

        if flag == 0:
            max_percentage = -inf
            selected_el = None
            for el in best_results:
                value = results[el][0][2]
                if value > max_percentage:
                    max_percentage = value
                    selected_el = el
        elif flag == 1:
            max_percentage = -inf
            selected_el = None
            for el in best_results:
                value = results[el][0][1]
                if value > max_percentage:
                    max_percentage = value
                    selected_el = el
        else:
            min_percentage = inf
            selected_el = None
            for el in best_results:
                value = results[el][0][0]
                if value < min_percentage:
                    min_percentage = value
                    selected_el = el

        return selected_el

    @staticmethod
    def get_additional_move_according_to_nn(possible_moves, model, color_str):
        results = {}

        for child in possible_moves:
            results[child] = model.predict(
                convert_matrix_to_array(child.state.fields, WHITE_COLOR == color_str).reshape((1, 768)))

        flag = 0

        best_results = list(filter(lambda key: (np.argmax(results[key]) == 0), list(results.keys())))
        if len(best_results) == 0:
            flag = 1
            best_results = list(filter(lambda key: (np.argmax(results[key]) == 1), list(results.keys())))
            if len(best_results) == 0:
                flag = 2
                best_results = list(results.keys())

        if flag == 0:
            max_percentage = -inf
            selected_el = None
            for el in best_results:
                value = results[el][0][0]
                if value > max_percentage:
                    max_percentage = value
                    selected_el = el
        elif flag == 1:
            max_percentage = -inf
            selected_el = None
            for el in best_results:
                value = results[el][0][1]
                if value > max_percentage:
                    max_percentage = value
                    selected_el = el
        else:
            min_percentage = inf
            selected_el = None
            for el in best_results:
                value = results[el][0][2]
                if value < min_percentage:
                    min_percentage = value
                    selected_el = el

        return selected_el
