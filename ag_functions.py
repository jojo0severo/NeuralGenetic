from neural_network import NeuralNetwork
from board import Board
import numpy as np


class AGFunctions:
    def __init__(self, file, mutation_chance, ignored_amount, network_conf):
        self.board = Board(file)
        self.mutation_chance = mutation_chance
        self.ignored_amount = ignored_amount
        self.network_conf = network_conf
        self.best = [None, -1]

    def init_population(self, population_size: int) -> list:
        population: list = []
        while population_size > 0:
            population.append((NeuralNetwork(layers=self.network_conf, init_layers=True), 0))
            population_size -= 1

        return population

    def show_stats(self, generation: int, scores: list) -> None:
        print(f'\n\nShowing statistcs of population: {generation}\n')

        scores_size: int = len(scores)
        print('Best overall: ', self.best[1])
        print('Score rank:\n\t1 - ', scores[0], end='')
        if scores_size > 1:
            print('\n\t2 - ', scores[1], end='')
        if scores_size > 2:
            print('\n\t3 - ', scores[2], end='')

        print('\n\nDisplaying execution of best Neural Network:\n')

        path: list = [tuple(self.board.start_pos)]
        path_size: int = 0
        res, pos = self.board.move(path[-1], self.best[0].forward(self.board.get_data(path[-1])))
        while res != 1:
            if path_size == 70:
                break

            path.append(pos)
            path_size += 1
            res, pos = self.board.move(path[-1], self.best[0].forward(self.board.get_data(path[-1])))

        print(self.board.build_execution(path), '\n')

    def evaluate(self, population_chunk: list) -> list:
        chunk_size: int = len(population_chunk)

        i: int = 0
        while i < chunk_size:
            points: float = 0
            path_size: int = 1
            path: list = [self.board.start_pos]
            model: NeuralNetwork = population_chunk[i][0]

            res, pos = self.board.move(path[-1], model.forward(self.board.get_data(path[-1])))
            while res != 1:
                if res == 3:
                    points += 50
                    break

                if path_size == 70:
                    break

                j: int = path_size - 2
                while j >= 0:
                    if path[j] == pos:
                        res = 0
                        break

                    j -= 1

                points += res
                path.append(pos)
                path_size += 1

                res, pos = self.board.move(path[-1], model.forward(self.board.get_data(path[-1])))

            population_chunk[i] = (model, points)
            i += 1

        return population_chunk

    def select(self, population_chunk: list) -> None:
        population_chunk.sort(key=lambda x: x[1], reverse=True)

        insert: bool = True
        if population_chunk[0][1] > self.best[1]:
            self.best = tuple(population_chunk[0])
            insert: bool = False

        if self.ignored_amount > 0:
            del population_chunk[-self.ignored_amount:]

        curr_size: int = len(population_chunk)

        threshold: float = 100
        factor: float = round((85 / curr_size), 2)

        i: int = 0
        while i < curr_size:
            if np.random.randint(0, 100) > threshold:
                del population_chunk[i]
                curr_size -= 1
            else:
                i += 1

            threshold -= factor

        if insert:
            population_chunk.append(self.best)

    def reproduce(self, population_chunk: list) -> list:
        chunk_size: int = len(population_chunk) // 2

        i: int = 0
        while i < chunk_size:
            population_chunk[i] = (population_chunk.pop(i)[0] // population_chunk[i][0], 0)
            i += 1

        return population_chunk

    def mutate(self, population_chunk: list) -> list:
        chunk_size: int = len(population_chunk)

        i: int = 0
        while i < chunk_size:
            j: int = 0
            while j < population_chunk[i][0].size:
                self.__mutate(population_chunk[i][0].weights[j])
                self.__mutate(population_chunk[i][0].bias[j])
                j += 1

            i += 1

        return population_chunk

    def __mutate(self, x: np.array):
        start_column: int = x.shape[1] - 1

        line: int = x.shape[0] - 1
        while line >= 0:
            column: int = start_column
            while column >= 0:
                if np.random.randint(0, 100) < self.mutation_chance:
                    x[line, column] = np.random.random_integers(-1, high=1)

                column -= 1
            line -= 1
