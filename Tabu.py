import numpy as np
from random import randint
import random
from itertools import combinations
import copy
import operator

class Tabu_search:
    def __init__(self,flow, distance, ini_solution, tabu_list_length, max_iteration, max_non_improvement_itr,
                 tabu_range, dynamic_tabu=False, aspiration=False, less_neighbourhood=False, frequency_based=False):
        self.flow = flow
        self.distance = distance
        self.ini_solution = ini_solution
        self.tabu_matrix = np.zeros((20,20))
        self.current_cost = self.calculate_cost(self.ini_solution)
        self.current_solution = self.ini_solution
        self.tabu_list_length = tabu_list_length
        self.max_iteration = max_iteration
        self.best_solution = self.current_solution
        self.best_cost = self.current_cost
        self.total_neighbourhood_attributes = list(combinations(self.ini_solution,2))
        self.neighbourhood_attributes = list(combinations(self.ini_solution,2))
        self.neighbours_list = []
        self.last_improvement_itr = 0
        self.max_non_improvement_itr = max_non_improvement_itr
        self.tabu_range = tabu_range
        self.dynamic_tabu = dynamic_tabu
        self.dynamic_tabu_counter = 20
        self.aspiration = aspiration
        self.less_neighbourhood = less_neighbourhood
        self.frequency_based = frequency_based

    def run(self):
        for n in range(self.max_iteration):

            # use smaller neighbourhood size
            if self.less_neighbourhood:
                random.shuffle(self.total_neighbourhood_attributes)
                self.neighbourhood_attributes = self.total_neighbourhood_attributes[:100]

            # update dynamic tabu list length
            if self.dynamic_tabu:
                if self.dynamic_tabu_counter == 20:
                    self.dynamic_tabu_counter = 0
                elif self.dynamic_tabu_counter == 0:
                    self.tabu_list_length = randint(self.tabu_range[0], self.tabu_range[1])
                else:
                    self.dynamic_tabu_counter = self.dynamic_tabu_counter + 1

            self.get_neighbourhood_values()
            next_move = self.choose_best_non_tabu_move()
            new_cost = self.current_cost + next_move[0] - self.tabu_matrix[max(next_move[1][0],next_move[1][1])][min(next_move[1][0],next_move[1][1])]
            # print("next_move[0]: {}".format(next_move[0]))
            # print("current cost: {}".format(self.current_cost))
            # print("new_cost: {}".format(new_cost))
            # print("best cost: {}".format(self.best_cost))
            # update current solution
            self.swap(next_move[1], self.current_solution)


            if new_cost < self.best_cost:
                # update best cost
                # print("update best")
                self.best_cost = new_cost
                self.best_solution = copy.deepcopy(self.current_solution)
                self.last_improvement_itr = n
            
            if new_cost < self.current_cost:
                # improving
                # print("improving")
                self.last_improvement_itr = n
            else:
                # non_improving
                pass
            self.current_cost = new_cost

            self.update_recency_tabu_list(next_move[1])
            if self.frequency_based:
                self.update_frequency_tabu_list(next_move[1])

            if self.best_cost == 2570:
                # best solution reached
                print("best solution reached")
                print("number of iterations: {}".format(n))
                break

            if n - self.last_improvement_itr > self.max_non_improvement_itr:
                # solution has not been improved for a long time, stopping criteria met
                print("hasn't improving for a long time")
                print("number of iterations: {}".format(n))
                break
        if n == 1999:
            print("max number of iteration reached")
        return self.best_solution, self.best_cost

    def update_recency_tabu_list(self, move):
        for i in range(self.tabu_matrix.shape[0]):
            for j in range(self.tabu_matrix.shape[1]):
                if j>i and self.tabu_matrix[i][j] > 0:
                    # upper triangle
                    self.tabu_matrix[i][j] = self.tabu_matrix[i][j] - 1
        self.tabu_matrix[min(move[0],move[1])][max(move[0],move[1])] = self.tabu_list_length

    def update_frequency_tabu_list(self, move):
        self.tabu_matrix[max(move[0],move[1])][min(move[0],move[1])] -= 1

    def choose_best_non_tabu_move(self):
        # print(self.neighbours_list)
        for i in range(len(self.neighbours_list)):
            # already sorted
            if self.check_recency_tabu(self.neighbours_list[i][1]):
                # it is a tabu move
                if self.aspiration:
                    if self.current_cost + self.neighbours_list[i][0] < self.best_cost:
                        # best solution:
                        print("aspiration!")
                        return self.neighbours_list[i]

                continue
            else:
                return self.neighbours_list[i]
        return self.neighbours_list[0]

    def get_neighbourhood_values(self):
        self.neighbours_list = []
        for move in self.neighbourhood_attributes:
            value = self.calculate_value_of_move(move)
            self.neighbours_list.append((value, move))
        # sort the neighbours list ascending, since we are minimizing the cost
        self.neighbours_list.sort(key = operator.itemgetter(0))

    def check_recency_tabu(self,move):
        #print(move)
        #print("min(move[0],move[1]): {}".format(min(move[0],move[1])))
        if self.tabu_matrix[min(move[0],move[1])][max(move[0],move[1])] > 0:
            return True
        else:
            return False


    def calculate_cost(self, perm):
        allocation = np.identity(20)
        allocation = allocation[perm]
        return self.flow.dot(allocation).dot(self.distance).dot(allocation.transpose()).trace()

    def calculate_value_of_move(self, swap):
        new_solution = copy.deepcopy(self.current_solution)
        self.swap(swap, new_solution)
        new_cost = self.calculate_cost(new_solution)
        if not self.frequency_based:
            return new_cost - self.current_cost
        else:
            return new_cost - self.current_cost + self.tabu_matrix[max(swap[0],swap[1])][min(swap[0],swap[1])]

    def swap(self, swap, permutation):
        temp = permutation[swap[0]]
        permutation[swap[0]] = permutation[swap[1]]
        permutation[swap[1]] = temp


if __name__ == "__main__":
    flow_path = "Flow.csv"
    distance_path = "Distance.csv"
    flow = np.loadtxt(flow_path, delimiter=',')
    distance = np.loadtxt(distance_path, delimiter=',')

    # initial_solution = np.random.permutation(20)
    initial_solution = [17,  8,  0, 14, 16,  5, 12, 11, 15,  1, 13,  2, 10,  3,  7, 18, 19,  4,  9,  6]
    tabu_list_length = 10
    max_iteration = 2000
    max_non_improvement_itr = 20
    tabu_range = (3,20)
    dynamic_tabu = False
    aspiration = False
    less_neighbourhood = False
    frequency_based = False
    tabu = Tabu_search(flow, distance, copy.deepcopy(initial_solution), tabu_list_length, max_iteration, 
                        max_non_improvement_itr, tabu_range, dynamic_tabu, aspiration, less_neighbourhood, frequency_based)
    solution, cost = tabu.run()
    print("initial solution: {}".format(initial_solution))
    print("tabu_list_length: {}".format(tabu_list_length))
    print("dynamic_tabu: {}".format(dynamic_tabu))
    print("aspiration: {}".format(aspiration))
    print("less_neighbourhood: {}".format(less_neighbourhood))
    print("frequency_based: {}".format(frequency_based))
    print("solution: {}".format(solution))
    print("cost: {}".format(cost))


    