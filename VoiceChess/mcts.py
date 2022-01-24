from math import log, sqrt, e, inf
import random
from computerLogic import *


class Node:
    def __init__(self, board) -> None:
        self.state = board
        self.children = set()
        self.parent = None
        self.N = 0
        self.n = 0
        self.v = 0


class MCTS:
    def __init__(self) -> None:
        pass

    @staticmethod
    def ucb(curr_node):
        ans = curr_node.v+2 * \
            (sqrt(log(curr_node.N+e+(10**-6))/(curr_node.n+(10**-10))))
        return ans

    @staticmethod
    def rollout(curr_node: Node, color_str, iterations=6):
        print("ite=", iterations)
        if iterations == 0:
            result = Heuristic.calculate(curr_node.state)

            if result > 10:
                return 1, curr_node
            elif result < -10:
                return -1, curr_node
            else:
                return 0.5, curr_node
        print("Prije is game overa")
        if Heuristic.is_game_over(curr_node.state):
            result = Heuristic.calculate(curr_node.state)
            print("Usao ovde a result je: ", result)
            if result > 5000:
                return 1, curr_node
            elif result < -5000:
                return -1, curr_node
            else:
                return 0.5, curr_node
        print("Posle is game overa")
        all_moves = curr_node.state.get_possible_moves(color_str)
        print("all_moves=", len(all_moves))
        if len(all_moves) == 0:
            result = Heuristic.calculate(curr_node.state)
            print("Usao ovde a result je: ", result)
            if result > 5000:
                return 1, curr_node
            elif result < -5000:
                return -1, curr_node
            else:
                return 0.5, curr_node
        for i in all_moves:
            child = Node(i)
            child.parent = curr_node
            curr_node.children.add(child)
        print("izasao iz fora")
        rnd_state = random.choice(list(curr_node.children))
        print("pozivam rollout ponovo")
        return MCTS.rollout(rnd_state, get_opponent_color(color_str), iterations-1)

    @staticmethod
    def expand(curr_node, color, iterations):
        if len(curr_node.children) == 0:
            return curr_node

        if iterations < 0:
            return curr_node

        if color == curr_node.state.computer_color:
            max_ucb = -inf
            sel_child = None
            for i in curr_node.children:
                tmp = MCTS.ucb(i)
                if tmp > max_ucb:
                    max_ucb = tmp
                    sel_child = i

            return MCTS.expand(sel_child, get_opponent_color(color), iterations - 1)

        else:
            min_ucb = inf
            sel_child = None
            for i in curr_node.children:
                tmp = MCTS.ucb(i)
                if tmp < min_ucb:
                    min_ucb = tmp
                    sel_child = i
            return MCTS.expand(sel_child, get_opponent_color(color), iterations - 1)

    @staticmethod
    def rollback(curr_node, reward):
        curr_node.n += 1
        curr_node.v += reward
        while curr_node.parent is not None:
            curr_node.N += 1
            curr_node = curr_node.parent
        return curr_node

    @staticmethod
    def mcts_pred(curr_node: Node, color_str, iterations=10):
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
            curr_node.children.add(child)
            map_state_move[child] = i

        while iterations > 0:
            if color_str == curr_node.state.computer_color:
                max_ucb = -inf
                sel_child = None
                for i in curr_node.children:
                    tmp = MCTS.ucb(i)
                    if tmp > max_ucb:
                        max_ucb = tmp
                        sel_child = i
                print("Ulazim u expand")
                ex_child = MCTS.expand(sel_child, get_opponent_color(color_str), 6)
                print("Ulazim u rollout")
                reward, state = MCTS.rollout(ex_child, color_str)
                print("Ulazim u rollback")
                curr_node = MCTS.rollback(state, reward)
                print("izasao iz rollbacka")
                iterations -= 1
            else:
                min_ucb = inf
                sel_child = None
                for i in curr_node.children:
                    tmp = MCTS.ucb(i)
                    if tmp < min_ucb:
                        min_ucb = tmp
                        sel_child = i
                print("Ulazim u expand else")
                ex_child = MCTS.expand(sel_child, get_opponent_color(color_str), 6)
                print("Ulazim u rollout else")
                reward, state = MCTS.rollout(ex_child, color_str)
                print("Ulazim u rollback else")
                curr_node = MCTS.rollback(state, reward)
                print("Izasao iz rollback else")
                iterations -= 1

            color_str = get_opponent_color(color_str)

        if color_str == curr_node.state.computer_color:

            mx = -inf
            selected_move = ''
            for i in curr_node.children:
                tmp = MCTS.ucb(i)
                if tmp > mx:
                    mx = tmp
                    selected_move = map_state_move[i]

            if Heuristic.calculate(selected_move) > 5000:
                return 100000
            elif Heuristic.calculate(selected_move) < -5000:
                return -100000

            return selected_move
        else:
            mn = inf
            selected_move = ''
            for i in curr_node.children:
                tmp = MCTS.ucb(i)
                if tmp < mn:
                    mn = tmp
                    selected_move = map_state_move[i]

            if Heuristic.calculate(selected_move) > 5000:
                return 100000
            elif Heuristic.calculate(selected_move) < -5000:
                return -100000

            return selected_move
