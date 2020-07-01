"""
Description
The eight queens puzzle is the problem of placing eight chess queens on an 8×8 chessboard so that no two queens threaten each other; thus, a solution requires that no two queens share the same row, column, or diagonal. The eight queens puzzle is an example of the more general n queens problem of placing n non-attacking queens on an n×n chessboard. (Source : https://en.wikipedia.org/wiki/Eight_queens_puzzle )

Challenge
The challenge is to generate one right sequence through Genetic Programming. The sequence has to be 8 numbers between 0 to 7. Each number represents the positions the Queens can be placed. Each number refers to the row number in the specific column

0 3 4 5 6 1 2 4

0 is the row number in the column 0 where the Queen can be placed

3 is the row number in the column 1 where the Queen can be placed

"""

# Load Libraries
import random
import pandas as pd
import numpy as np

# Define funtion on population
def random_chromosome(size): #making random chromosomes
    return [random.randint(1, n) for _ in range(n)]


# Define Fitness Function
def fitness(chromosome):
    horizontal_collisions = sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * 2 * n
    right_diagonal = [0] * 2 * n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter / (n - abs(i - n + 1))

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))  # 28-(2+3)=23


# Define the probability
def probability(chromosome, fitness):
    return fitness(chromosome) / maxFitness

def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "IncorrectSelection"


# CrossOver of two parents
def reproduce(x, y): #doing cross_over between two chromosomes
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

# Mutation
def mutate(x):  #randomly changing the value of a random index of a chromosome
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x

def genetic_queen(population, fitness, mutation_probability):
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities) #best chromosome 1
        y = random_pick(population, probabilities) #best chromosome 2
        child = reproduce(x, y) #creating two new chromosomes from the best 2 chromosomes
        if random.random() < mutation_probability:
            child = mutate(child)
        print_chromosome(child)
        new_population.append(child)
        if fitness(child) == maxFitness: break
    return new_population

def print_chromosome(chrom):
    print("Chromosome = {},  Fitness = {}"
        .format(str(chrom), fitness(chrom)))


if __name__ == "__main__":
    n = int(input("Enter Number of Queens: "))
    maxFitness = (n * (n - 1)) / 2  # 8*7/2 = 28
    population = [random_chromosome(n) for _ in range(1000)]
    mutation_probability = 0.04
    generation = 1

    while not maxFitness in [fitness(chrom) for chrom in population]:
        print("=== Generation {} ===".format(generation))
        population = genetic_queen(population, fitness, mutation_probability)
        print("")
        print("Maximum Fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1
    chrom_out = []
    print("Solved in Generation {}!".format(generation - 1))
    for chrom in population:
        if fitness(chrom) == maxFitness:
            print("")
            print("One of the solutions: ")
            chrom_out = chrom
            print_chromosome(chrom)

    board = []

    for x in range(n):
        board.append(["x"] * n)

    for i in range(n):
        board[n - chrom_out[i]][i] = "Q"


    def print_board(board):
        for row in board:
            print(" ".join(row))


    print()
    print_board(board)