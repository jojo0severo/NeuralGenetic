from ag_functions import AGFunctions
import multiprocessing
import numpy as np
np.random.seed(23)


class ParallelRunner:
    def __init__(self, population_size, network_conf, file, mutation_chance, ignored_amount):
        self.population = []

        self.population_size = population_size
        self.core_number = multiprocessing.cpu_count() - 1
        self.ag_functions = AGFunctions(file, mutation_chance, ignored_amount, network_conf)

    def run(self, generations, stats_percent=None):
        if not stats_percent:
            stats_percent = (generations // 10) or 1

        with multiprocessing.Pool(processes=self.core_number) as pool:
            self.__init_parallel_chunks(pool)

            for i in range(1, generations + 1):
                self.__evaluate_parallel_chunks(pool)
                self.ag_functions.select(self.population)

                if i % stats_percent == 0:
                    self.ag_functions.show_stats(i, [score for _, score in self.population[:3]])

                self.__reproduce_parallel_chunks(pool)
                self.__mutate_parallel_chunks(pool)

            pool.close()
            pool.join()

    def __init_parallel_chunks(self, pool):
        cores = self.core_number - 1
        chunks = [self.population_size // cores for _ in range(cores)]
        chunks.append(self.population_size % cores)

        for chunk in pool.imap_unordered(self.ag_functions.init_population, chunks):
            self.population.extend(chunk)

    def __evaluate_parallel_chunks(self, pool):
        chunk_size = self.population_size // self.core_number + (self.population_size % self.core_number > 0)

        iterable = self.__loop_iter(self.population, 0, self.population_size)
        chunks = self.__get_chunks(iterable, self.population_size, chunk_size)

        for chunk in pool.imap_unordered(self.ag_functions.evaluate, chunks):
            self.population.extend(chunk)

    def __reproduce_parallel_chunks(self, pool):
        current_size = len(self.population)
        difference = (self.population_size - current_size) * 2

        chunk_size = difference // self.core_number
        while chunk_size == 0 or chunk_size % 2 != 0:
            chunk_size += 1

        np.random.shuffle(self.population)
        if difference > current_size:
            iterable = self.__loop_iter(self.population, (difference - current_size), current_size + 1)
        else:
            iterable = self.__loop_iter(self.population, 0, current_size)

        copy = self.population[:]
        chunks = self.__get_chunks(iterable, difference, chunk_size)
        for chunk in pool.imap_unordered(self.ag_functions.reproduce, chunks):
            copy.extend(chunk)

        self.population = copy

    def __mutate_parallel_chunks(self, pool):
        chunk_size = self.population_size // self.core_number + (self.population_size % self.core_number > 0)

        iterable = self.__loop_iter(self.population, 0, self.population_size)
        chunks = self.__get_chunks(iterable, self.population_size, chunk_size)

        for chunk in pool.imap_unordered(self.ag_functions.mutate, chunks):
            self.population.extend(chunk)

    @staticmethod
    def __loop_iter(iterable, additions, iterable_size):
        counter = 0
        while iterable_size > 0:
            if additions > 0:
                if counter == iterable_size - 1:
                    counter = 0

                curr = iterable[counter]
                counter += 1
                additions -= 1

            else:
                curr = iterable.pop(0)

            yield curr

            iterable_size -= 0 if additions > 0 else 1

    @staticmethod
    def __get_chunks(iterable, chunks_amount, chunk_size):
        while chunks_amount > 0:
            chunk = []
            counter = 0
            while counter < chunk_size and chunks_amount > 0:
                chunk.append(next(iterable))
                counter += 1
                chunks_amount -= 1

            yield chunk


if __name__ == '__main__':
    r = ParallelRunner(150, [(8, 8), (8, 8), (8, 4)], 'board.txt', 30, 0)
    r.run(2000, stats_percent=100)
