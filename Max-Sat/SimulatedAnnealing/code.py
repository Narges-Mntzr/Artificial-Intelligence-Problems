# In the name of God
# Artificial Intelligence course in IUT - HW1
# Solve Max-Sat problem with simulated anneling
# 1401/08/13

from random import choice, random
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd

sampleFile = "Max-Sat/Max-SAT sample/Max-Sat_20_80.txt"

# Sample Variables
clauses = []
varCnt = 0

# Tempreture Variables
t0 = 5
tf = 0.001
max_iterations = 250000
initial_solutions_cnt = 2

def annot_max(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text= "x={}, y={}".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94,0.96), **kw)

def disturb(solution):
    return [1 - var if random() < 0.01 else var for var in solution]

def drawPlot(scores):
    x = [i+1 for i in range (len(scores))]
    y = scores
    
    plt.plot(x, y)
    
    plt.xlabel('scores')
    plt.ylabel('levels')
    
    plt.title('Solve max sat with simulated annealing.')
    annot_max(x,y)
    plt.show()

def evaluate(clause, solution):
    return any([solution[position] == value for position, value in clause])

def evaluate_all(clauses, solution):
    return np.sum([evaluate(clause, solution) for clause in clauses])

def initial_solution():
    return [choice([True, False]) for _ in range(varCnt)]

def next_temperature(i):
    return (t0-tf)/(np.cosh(10*i/max_iterations)) + tf

def readFile():
    with open(sampleFile, 'r') as file:
        all_lines = file.readlines()
    global varCnt
    varCnt,cluasesCnt = list(map(int,all_lines[0].split()))
    all_lines = all_lines[1:]
    
    for line in all_lines:
        clause = line.split()

        newClause=[]
        for num in clause[:-1]:
            newClause.append(to_tuple(num))
        
        clauses.append(newClause)

def simmulated_annealing(initial):
    solution = initial
    score = evaluate_all(clauses, solution)
    temperature = t0
    iterations = 0
    scores = []

    while iterations < max_iterations:
        new_solution = disturb(solution)
        new_score = evaluate_all(clauses, new_solution)
        delta = score - new_score  # Equivalent to E(new_solution) - E(solution)
        if delta <= 0 or random() < np.exp(-delta/temperature):
            solution = new_solution
            score = new_score
        iterations += 1
        scores.append(score)
        temperature = next_temperature(iterations)

    scores = np.array(scores)
    return scores

def to_tuple(n_str):
    n = int(n_str)
    return (abs(n)-1, n >= 0)    



if __name__ == "__main__":
    readFile()
    initial = initial_solution()

    scores = simmulated_annealing(initial)
    drawPlot(scores)
    
