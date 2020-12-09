# Use backtracking to solve a sudoku puzzle
# Puzzle is specified as a list of 81 integers in [0..9]

# Draws from the database at Project Euler problem 96.

# output(candidate): format the solved puzzle and return a
# preformatted string for the solution; only called once
# a solution has been found
def output(candidate):
    outString = ''
    
    for rowIndex in range(9):
        row = [str(_) for _ in candidate[9*rowIndex:9*rowIndex + 9]]
        rowString = ''.join(row[0:3]) + '|' + ''.join(row[3:6]) + '|' + ''.join(row[6:])
        outString += rowString + '\n'

        if rowIndex in [2, 5]:
            outString += '---+---+---\n'

    return outString[:-1]

# accept(candidate): we are only testing already-checked
# sudoku tables, so we only check whether we have any unfilled
# squares left in the puzzle; return candidate if it is a full
# solution, otherwise False.
def accept(candidate):
    #if not reject(candidate) and 0 not in candidate:
    if 0 not in candidate:
        return candidate

# getChildren(candidate): generate all the valid extensions of the 
# current candidate, by finding the first insertion point and eliminating
# common entries from the row, column, or subsquare. If no valid extension
# exists, then return an empty list.
def getValidChildren(candidate):
    # Find the first occurence of 0 in the list, and replace
    # using the digits 1 through 9
    children = []
    
    if 0 in candidate:
        cell = candidate.index(0)
        row = cell // 9
        col = cell % 9
        digitSet = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Find all the entries sharing this row
        rowEntries = {candidate[9*row + _] for _ in range(9)}

        # Find all the entries sharing this column
        colEntries = {candidate[col + 9*_] for _ in range(9)}
        
        # Find all the entries sharing the subsquare
        rowAnchor = 3*(row // 3)
        colAnchor = 3*(col // 3)
        subSquareEntries = {candidate[9*(rowAnchor + i) + (colAnchor + j)] for i in range(3) for j in range(3)}

        badDigits = {0}.union(rowEntries, colEntries, subSquareEntries)
        digitList = list({1, 2, 3, 4, 5, 6, 7, 8, 9} - badDigits)

        for digit in digitList:
            nextCandidate = candidate[0:cell] + [digit] + candidate[cell + 1:]
            children.append(nextCandidate)

    return children

# backtrack(candidate):
# Test if the candidate fails; if so, return False
# Test if the candidate is a solution; if so, return the candidate
#   and call output to print it
# Then generate all the children and recurse. If we run out of children
# without finding a solution, return False
def backtrack(candidate):
    #if reject(candidate):
    #    return False

    if accept(candidate):
        #output(candidate)
        return candidate

    children = getValidChildren(candidate)

    for ch in children:
        nextBranch = backtrack(ch)
        if nextBranch:
            return nextBranch
        else:
            continue

    return False

# Download the puzzle from my database of puzzles, 1-indexed
def getPuzzle(n):
    with open('puzzle_database.txt') as f:
        data = f.readlines()[10*(n - 1) + 1:10*(n - 1) + 10]

    puzzle = []
    for line in data:
        puzzle += [int(line[_]) for _ in range(9)]

    return puzzle

codeSum = 0

for index in range(1, 51):
    print('Solving puzzle ' + str(index))
    puzzle = getPuzzle(index)
   
    solution = backtrack(puzzle)
    code = 100*solution[0] + 10*solution[1] + solution[2]

    print(f'Three-digit code is {code}')
    codeSum += code

print(f'Sum of all three-digit codes: {codeSum}')
