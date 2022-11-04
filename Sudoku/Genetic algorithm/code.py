# In the name of God
# Artificial Intelligence course in IUT - HW1
# Solve sudoku problem with genetic algorithm
# 1401/08/13

import numpy 
import random
import math
import matplotlib.pyplot as plt

sampleFile = "Sudoku/sudoku samples/sample2_medium.txt"
SIZE = 9

POPULATOIN_SIZE = 500
SELECTION_RATE = 0.85
MUTATION_RATE = 0.05
BEST_CNT = 20

fitList = []


def annot_max(x, y, ax=None):
    xmax = x[numpy.argmax(y)]
    ymax = y.max()
    text = "x={}, y={}".format(xmax, ymax)
    if not ax:
        ax = plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops = dict(
        arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data', textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94, 0.96), **kw)

def readSudoku():
    try:
        with open(sampleFile, "r") as file:
            all_lines = file.readlines()
            for i in range(len(all_lines)):
                all_lines[i] = list(map(int, all_lines[i].split()))
            return all_lines
    except FileNotFoundError:
        exit("Input file not found.")

def makePopulations(mainSudoko):
    board = []
    for i in range(SIZE):
        board.append([])

    for i in range(SIZE):
        for j in range(SIZE):
            board[i].append([])

    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(1, SIZE+1):
                if (mainSudoko[i][j] == 0):
                    if (not (rowDup(mainSudoko, i, k) or columnDup(mainSudoko, j, k) or subBlockDup(mainSudoko, i, j, k))):
                        board[i][j].append(k)
                else:
                    board[i][j].append(mainSudoko[i][j])
                    break

    populations = []
    for _ in range(POPULATOIN_SIZE):
        person = []
        for i in range(SIZE):
            person.append([])

        for i in range(SIZE):
            row = numpy.zeros(SIZE, dtype=int)
            while (len(list(set(row))) != SIZE):
                for j in range(SIZE):
                    if (mainSudoko[i][j] == 0):
                        row[j] = int(
                            board[i][j][random.randint(0, len(board[i][j]) - 1)])
                    else:
                        row[j] = mainSudoko[i][j]

            person[i] = row

        populations.append(person)

    return populations, updateFit(populations)

def updateFit(populations):
    puplefit = []
    for puple in populations:
        puplefit.append(tuple((puple, findFitness(puple))))
    return puplefit

def mutation(mutationRate, mainSudoku, candidate):
    myrandNum = random.uniform(0, 1.1)

    mutationDone = False
    if (myrandNum < mutationRate):
        while (not mutationDone):
            chosenRow = random.randint(0, 8)

            firstColumn = 0
            secondColumn = 0

            while (firstColumn == secondColumn):
                firstColumn = random.randint(0, 8)
                secondColumn = random.randint(0, 8)

            if (mainSudoku[chosenRow][firstColumn] == 0 and mainSudoku[chosenRow][secondColumn] == 0):
                if (not columnDup(mainSudoku, secondColumn, candidate[chosenRow][firstColumn])
                        and not columnDup(mainSudoku, firstColumn, candidate[chosenRow][secondColumn])
                        and not subBlockDup(mainSudoku, chosenRow, secondColumn, candidate[chosenRow][firstColumn])
                        and not subBlockDup(mainSudoku, chosenRow, firstColumn, candidate[chosenRow][secondColumn])):
                    temp = candidate[chosenRow][secondColumn]
                    candidate[chosenRow][secondColumn] = candidate[chosenRow][firstColumn]
                    candidate[chosenRow][firstColumn] = temp
                    mutationDone = True
    return

def crossOver(crossoverRate, firstParent, secondParent):
    firstChild = numpy.copy(firstParent)
    secondChild = numpy.copy(secondParent)

    myrandNum = random.uniform(0, 1.1)

    first = 2
    second = 1
    if (myrandNum < crossoverRate):
        while (first > second):
            first = random.randint(0, 8)
            second = random.randint(1, 9)

        for i in range(first, second):
            firstChild[i], secondChild[i] = crossoverRows(
                firstChild[i], secondChild[i])

    return firstChild, secondChild

def crossoverRows(firstRow, secondRow):
    firstChildRow = numpy.zeros(SIZE, dtype=int)
    secondChildRow = numpy.zeros(SIZE, dtype=int)

    myCycle = list(range(1, SIZE + 1))
    cycle = 0

    while ((0 in firstChildRow) and (0 in secondChildRow)):
        if (cycle % 2 == 0):
            index = findinCycle(firstRow, myCycle)
            start = firstRow[index]
            myCycle.remove(firstRow[index])
            firstChildRow[index] = firstRow[index]
            secondChildRow[index] = secondRow[index]
            next = secondRow[index]

            while (next != start):
                index = findVal(firstRow, next)
                myCycle.remove(firstRow[index])
                firstChildRow[index] = firstRow[index]
                secondChildRow[index] = secondRow[index]
                next = secondRow[index]

            cycle += 1
        else:
            index = findinCycle(firstRow, myCycle)
            start = firstRow[index]
            myCycle.remove(firstRow[index])
            firstChildRow[index] = secondRow[index]
            secondChildRow[index] = firstRow[index]
            next = secondRow[index]

            while (next != start):
                index = findVal(firstRow, next)
                myCycle.remove(firstRow[index])
                firstChildRow[index] = secondRow[index]
                secondChildRow[index] = firstRow[index]
                next = secondRow[index]

            cycle += 1

    return firstChildRow, secondChildRow

def findinCycle(row, myCycle):
    for i in range(0, len(row)):
        if (row[i] in myCycle):
            return i

def findVal(row, value):
    for i in range(0, len(row)):
        if (row[i] == value):
            return i

def findFitness(person):
    blockArray = numpy.zeros(SIZE, dtype=int)
    rowFit = 0
    columnFit = 0
    blockFit = 0

    for i in range(SIZE):
        rowArray = numpy.zeros(SIZE, dtype=int)
        for j in range(SIZE):
            rowArray[person[i][j] - 1] += 1
        rowFit += (1.0 / len(set(rowArray)))/SIZE

    for i in range(SIZE):
        columnArray = numpy.zeros(SIZE, dtype=int)
        for j in range(SIZE):
            columnArray[int(person[j][i]) - 1] += 1
        columnFit += (1.0 / len(set(columnArray)))/SIZE

    for i in range(0, SIZE, 3):
        for j in range(0, SIZE, 3):
            blockArray[int(person[i][j] - 1)] += 1
            blockArray[int(person[i][j + 1] - 1)] += 1
            blockArray[int(person[i][j + 2] - 1)] += 1

            blockArray[int(person[i + 1][j] - 1)] += 1
            blockArray[int(person[i + 1][j + 1] - 1)] += 1
            blockArray[int(person[i + 1][j + 2] - 1)] += 1

            blockArray[int(person[i + 2][j] - 1)] += 1
            blockArray[int(person[i + 2][j + 1] - 1)] += 1
            blockArray[int(person[i + 2][j + 2] - 1)] += 1

            blockFit += (1.0 / len(set(blockArray))) / SIZE
            blockArray = numpy.zeros(SIZE, dtype=int)

    if (int(rowFit) == 1 and int(columnFit) == 1 and int(blockFit) == 1):
        fitness = 1.0
    else:
        fitness = columnFit * blockFit

    return fitness

def columnDup(mainSudoku, columnNum, value):
    for i in range(SIZE):
        if (mainSudoku[i][columnNum] == value):
            return True
    return False

def rowDup(mainSudoku, rowNum, value):
    for i in range(SIZE):
        if (mainSudoku[rowNum][i] == value):
            return True
    return False

def subBlockDup(mainSudoku, rowNum, columnNum, value):
    minSize = int(math.sqrt(SIZE))
    rowNum = minSize * (int(rowNum / minSize))
    columnNum = minSize * (int(columnNum / minSize))

    for i in range(minSize):
        for j in range(minSize):
            if (mainSudoku[rowNum+i][columnNum+j] == value):
                return True
    return False

def populationSort(populations):
    sortedPopulations = sorted(populations, key=lambda tup: tup[1])
    sortedPopulations.reverse()
    return sortedPopulations

def compete(sortedPopulations):
    firstParent = sortedPopulations[random.randint(
        0, len(sortedPopulations) - 1)]
    secondParent = sortedPopulations[random.randint(
        0, len(sortedPopulations) - 1)]

    firstFit = findFitness(firstParent)
    secondFit = findFitness(secondParent)

    if (firstFit > secondFit):
        better = firstParent
        worse = secondParent
    else:
        better = secondParent
        worse = firstParent

    myRandNum = random.uniform(0, 1)
    if (myRandNum < SELECTION_RATE):
        return better
    else:
        return worse

def solve(mainSudoku):
    initial, initialFit = makePopulations(mainSudoku)

    sortedPopulations = []
    for _ in range(POPULATOIN_SIZE):
        sortedPopulations = populationSort(initialFit)
        fitList.append(sortedPopulations[0][1])
        if (int(sortedPopulations[0][1]) == 1):
            return sortedPopulations[0][0]

        nextPopulation = []

        for i in range(BEST_CNT):
            nextPopulation.append(numpy.copy(sortedPopulations[i])[0])

        for _ in range(BEST_CNT, POPULATOIN_SIZE, 2):
            firstparent = compete(initial)
            secondparent = compete(initial)

            firstchild, secondchild = crossOver(1, firstparent, secondparent)

            mutation(MUTATION_RATE, mainSudoku, firstchild)
            mutation(MUTATION_RATE, mainSudoku, secondchild)

            nextPopulation.append(firstchild)
            nextPopulation.append(secondchild)

        initial = nextPopulation
        initialFit = updateFit(nextPopulation)
    return sortedPopulations[0][0]


def drawPlot(plot):
    x = [i+1 for i in range(len(plot))]
    y = plot

    plt.plot(x, y)

    plt.xlabel('scores')
    plt.ylabel('levels')

    plt.title('Solve max sat with simulated annealing.')
    annot_max(x, y)
    plt.show()


if __name__ == "__main__":
    problem_grid = readSudoku()
    ans_grid = solve(problem_grid)
    for i in ans_grid:
        for j in i:
            print(j, end=" ")
        print()
    drawPlot(numpy.array(fitList))
