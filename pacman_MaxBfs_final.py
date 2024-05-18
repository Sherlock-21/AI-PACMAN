from typing import Tuple, List
import random as r
import math as m
from queue import Queue

class Game:
    """
    for first arg ----> refs to Y
    for second arg ----> refs to X
    """

    def __init__(
        self,
        size_board=(7, 14),
        number_of_wall=10,
        pacman_position=(3, 7),
        ghost1_position=None,
        ghost2_position=None,
        score=0,
    ) -> None:
        self.size_board = size_board
        self.number_of_wall = number_of_wall
        self.pacman_position = pacman_position
        self.ghost1_position = (3, 9)
        self.ghost2_position = (1, 1)
        self.score = score
        self.board = None
        self.create_board_game()

    def get_score(self) -> int:
        return self.score

    def get_pos_pacman(self) -> Tuple:
        return self.pacman_position

    def get_pos_ghost(self, choice: int) -> Tuple:
        if choice == 1:
            return self.ghost1_position
        elif choice == 2:
            return self.ghost2_position

    def get_board(self) -> List:
        return self.board

    def set_board(self, board) -> None:
        self.board = board

    def set_pos_pacman(self, new_pos) -> None:
    
        if new_pos==None:
            self.pacman_position=self.pacman_position
        else:    
            self.pacman_position = new_pos

    def set_pos_ghost(self, choice: int, new_pos) -> Tuple:
        if choice == 1:
            self.ghost1_position = new_pos
        elif choice == 2:
            self.ghost2_position = new_pos

    def set_score(self, score):
        self.score = score

    def get_size(self):
        return self.size_board

    def create_board_game(self) -> None:
        self.board = [
            ["*" for _ in range(self.size_board[1])] for _ in range(self.size_board[0])
        ]

        counter = 1
        while counter <= self.number_of_wall:
            i, j = r.randint(0, self.size_board[0] - 1), r.randint(
                0, self.size_board[1] - 1
            )
            if (
                (i, j) == self.pacman_position
                or (i, j) == self.ghost1_position
                or (i, j) == self.ghost2_position
                or self.board[i][j] == "|"
            ):
                continue

            self.board[i][j] = "|"
            counter += 1

    def display(self, score: int) -> None:
        for x in range(self.size_board[0]):
            for y in range(self.size_board[1]):
                if (x, y) == self.pacman_position:
                    print("P", end=" ")
                elif (x, y) == self.ghost1_position:
                    print("G", end=" ")
                elif (x, y) == self.ghost2_position:
                    print("G", end=" ")
                else:
                    print(self.board[x][y], end=" ")
            print()
        print(f"                                                Score: {self.score}")

class Ghosts:
    def __init__(self):
        pass

    def move_ghosts(
        self, pos_ghosts1, pos_ghosts2, board, board_size, random=True, action=None
    ) -> Tuple:
        new_pos_ghosts1 = self.randomally_moves(pos_ghosts1, board_size, random, action)
        new_pos_ghosts2 = self.randomally_moves(pos_ghosts2, board_size, random, action)

        if self._is_not_possible(new_pos_ghosts1, board, board_size):
            new_pos_ghosts1 = pos_ghosts1

        if self._is_not_possible(new_pos_ghosts2, board, board_size):
            new_pos_ghosts2 = pos_ghosts2

        return {"ghosts1": new_pos_ghosts1, "ghosts2": new_pos_ghosts2}

    def randomally_moves(self, pos, board_size, random=True, action=None) -> Tuple:
        ways = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

        if random:
            way_key = r.choice(list(ways.keys()))
            way = ways[way_key]

            x, y = pos
            new_x = x + way[0]
            new_y = y + way[1]

        else:
            x, y = pos
            way = ways[action]
            new_x = x + way[0]
            new_y = y + way[1]

        if 0 <= new_x < board_size[0] and 0 <= new_y < board_size[1]:
            return (new_x, new_y)
        else:
            return pos

    def _is_not_possible(self, pos, board, board_size) -> True:
        x, y = pos
        if 0 <= x < board_size[0] and 0 <= y < board_size[1] and board[x][y] != "|":
            return False
        else:
            return True

class Pacman:
    def __init__(self, utility):
        self._ways_possible_for_ghosts = [
            "up",
            "down",
            "left",
            "right",
        ]
        self.utility = utility 

    def _min_max(
        self, state, is_pacman, depth, alpha=float("-inf"), beta=float("-inf")
    ) -> set:
        if self.utility.is_game_finished(state) or depth == 0:
            return self.utility.get_utility(state)

        if is_pacman:
            v = float("-inf")
            actions_values = [
                (action, self._min_max(self.transfer(state, action, 1), 0, depth - 1))
                for action in self._ways_possible_for_pacman(state)
            ]
            v = max(actions_values, key=lambda x: x[1])[1]
            if v >= beta:
                return v
            alpha = max(alpha, v)
            return v
        else:
            actions_values = [
                (action, self._min_max(self.transfer(state, action, 0), 1, depth - 1))
                for action in self._ways_possible_for_ghosts
            ]
            v = min(actions_values, key=lambda x: x[1])[1]
            if v <= alpha:
                return v
            beta = min(beta, v)
            return v

    def best_action(self, state):
        print("----MinMax----")
        actions_values = [
            (
                action,
                self._min_max(
                    self.transfer(create_copy_state(state), action, 1),
                    0,
                    depth=6,
                ),
            )
            for action in self._ways_possible_for_pacman(state)
        ]
        best_word = max(actions_values, key=lambda temp: temp[1])
        best_action, best_score = best_word
        best_action = [
            elements[0] for elements in actions_values if elements[1] == best_score
        ]
        return r.choice(best_action)

    def transfer(self, state, action, is_pacman):
        if is_pacman:
            new_state = create_copy_state(state)
            xp, yp = state.get_pos_pacman()

            board = state.get_board()
            board_size = state.get_size()
            new_pos_pacman = self.moves_pacman((xp, yp), action, board_size, board)
            new_state.set_pos_pacman(new_pos_pacman)
            return new_state

        else:
            G = Ghosts()
            new_state = create_copy_state(state)
            pos_g1 = state.get_pos_ghost(1)
            pos_g2 = state.get_pos_ghost(2)

            board = state.get_board()
            board_size = state.get_size()

            new_pos_ghosts = G.move_ghosts(
                pos_g1, pos_g2, board, board_size, False, action
            )

            new_pos_g1 = new_pos_ghosts["ghosts1"]
            new_pos_g2 = new_pos_ghosts["ghosts2"]

            new_state.set_pos_ghost(1, new_pos_g1)
            new_state.set_pos_ghost(2, new_pos_g2)

            return new_state

    def _ways_possible_for_pacman(
        self,
        state,
    ) -> List:
        x, y = state.get_pos_pacman()
        board = state.get_board()
        board_size = state.get_size()

        actions = []

        if x > 0 and board[x - 1][y] != "|":
            actions.append("up")

        if x < board_size[0] - 1 and board[x + 1][y] != "|":
            actions.append("down")

        if y > 0 and board[x][y - 1] != "|":
            actions.append("left")

        if y < board_size[1] - 1 and board[x][y + 1] != "|":
            actions.append("right")
        return actions

    def moves_pacman(self, pacman_pos, way_posibale, board_size, board) -> set:
        x, y = pacman_pos
        ways = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        dx, dy = ways[way_posibale]
        new_x = x + dx
        new_y = y + dy

        if (
            0 <= new_x < board_size[0]
            and 0 <= new_y < board_size[1]
            and board[new_x][new_y] != "|"
        ):
            return (new_x, new_y)

        else:
            pacman_pos
    
    def bfs(self, state, start):
        board = state.get_board()
        visited = set()
        q = Queue()
        q.put(start)
        while not q.empty():
            x, y = q.get()
            if board[x][y] == "*":
                return (x, y)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]) and board[new_x][new_y]!='|' and (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    q.put((new_x, new_y))
                    
        return None
    
    def best_move(self, state):
        board = state.get_board()
        pos_pacman = state.get_pos_pacman()
        nearest_food = self.bfs(state, pos_pacman)
        nearest_ghost_distance = self.distance_to_nearest_ghost(state, pos_pacman)
        
        
        if nearest_ghost_distance < 3:
            return self.best_action(state)
        
        
        if nearest_food:
            if board[nearest_food[0]][nearest_food[1]]!='|':
                actions = self._ways_possible_for_pacman(state)
                x, y = pos_pacman
                nx, ny = nearest_food
                print("Nearest_food = ",nearest_food)
                print("-----BFS------")
                if nx < x:
                    return "up"
                elif nx > x:
                    return "down"
                elif ny < y:
                    return "left"
                elif ny > y:
                    return "right"
            else:
               
                return self.best_action(state)
        
    def distance_to_nearest_ghost(self, state, pos_pacman):
        min_distance = float('inf')  
        for i in range(1, 3):  
            ghost_pos = state.get_pos_ghost(i)
            distance = self._euclidean_distance(pos_pacman, ghost_pos)
            min_distance = min(min_distance, distance)
        return min_distance
    
    def _euclidean_distance(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


class Utility:
    def __init__(self) -> None:
        pass

    def get_utility(self, state):
        if self.is_pacman_win(state):
            return 1000 + state.score

        if state.get_pos_pacman() == state.get_pos_ghost(
            1
        ) or state.get_pos_pacman() == state.get_pos_ghost(2):
            return state.score - 1000

        return (
            state.score
            + self.distance_from_near_food(state) * 100
            + self.distance_from_near_food(state) * 1000
        )

    def is_game_finished(self, state):
        return (
            self.is_pacman_win(state)
            or state.get_pos_pacman() == state.get_pos_ghost(1)
            or state.get_pos_pacman() == state.get_pos_ghost(2)
        )

    def is_pacman_win(self, state):
        for row in state.get_board():
            if "*" in row:
                return False
        return True

    def distance_from_near_food(self, state):
        pos_pacman = state.get_pos_pacman()
        ghosts1 = state.get_pos_ghost(1)
        ghosts2 = state.get_pos_ghost(2)

        ed1, ed2 = self._euclidean_distance(
            pos_pacman, ghosts1
        ), self._euclidean_distance(pos_pacman, ghosts2)
        return min(ed1, ed2)

    def _euclidean_distance(self, point1, point2):
        return m.sqrt(pow(point1[0] - point1[0], 2) + pow(point2[0] - point2[0], 2))

def create_copy_state(state) -> Game:
    new_board = Game()
    new_board.set_pos_pacman(state.get_pos_pacman())
    new_board.set_pos_ghost(1, state.get_pos_ghost(1))
    new_board.set_pos_ghost(2, state.get_pos_ghost(2))
    new_board.set_score(state.get_score())
    new_board.set_board(state.get_board())
    return new_board

class Play:
    def __init__(self) -> None:
        self.game = Game()
        self.score = self.game.score
        self.ghosts = Ghosts()
        self.state = self.game.get_board()
        self.utility = Utility()
        self.pacman = Pacman(self.utility)

    def start(self):
        while True:
            self.game.display(self.game.get_score())
            if self.utility.is_game_finished(self.game):
                if self.utility.is_pacman_win(self.game):
                    print("***PACMAN WIN !!!***")
                    break
                else:
                    print("**PACMAN LOST !**")
                    break

            best_action = self.pacman.best_move(self.game)
            
            print(best_action,"\n\n")

            
            if best_action is None:
                
                
                best_action = self.pacman.best_action(self.game)
                

            new_pos_pacmans = self.pacman.moves_pacman(
                self.game.get_pos_pacman(),
                best_action,
                self.game.get_size(),
                self.game.get_board(),
            )

            self.game.set_pos_pacman(new_pos_pacmans)

            pos_g1 = self.game.get_pos_ghost(1)
            pos_g2 = self.game.get_pos_ghost(2)

            self.game.score -= 1

            poses = self.ghosts.move_ghosts(
                pos_g1, pos_g2, self.game.get_board(), self.game.get_size()
            )

            self.game.set_pos_ghost(1, poses["ghosts1"])
            self.game.set_pos_ghost(2, poses["ghosts2"])

            if self.game.get_pos_pacman() == self.game.get_pos_ghost(
                1
            ) or self.game.get_pos_pacman() == self.game.get_pos_ghost(2):
                print("***Pacman is caught by a ghost!***")
                break

            if (
                self.game.get_board()[self.game.get_pos_pacman()[0]][
                    self.game.get_pos_pacman()[1]
                ]
                == "*"
            ):
                self.game.score += 10
                board = self.game.get_board()
                board[self.game.get_pos_pacman()[0]][
                    self.game.get_pos_pacman()[1]
                ] = " "
                self.game.set_board(board)

if __name__ == "__main__":
    Play().start()

