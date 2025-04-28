import sys

# Creates an array from a single line of input.txt.
# The general idea here is that we scan the file, looking for blocks of numbers with no spaces
# in between. These we add as individual items to the array.
def getArrayFromStr(str):
    # A string which contains numbers. We keep adding numbers until we reach a blank space.
    tempEntry = ""
    array = []
    for char in str:
        # If we have a blank space and tempEntry isn't empty, OR we have a newline and tempEntry
        # isn't empty, then we wish to add what is currently in tempEntry to the array.
        if (char == " " and tempEntry != "") or (char == "\n" and tempEntry != ""):
            # We will try to convert tempEntry to a float, then add it to the array.
            try:
                array.append(float(tempEntry))
                # If successful, then we reset tempEntry, so that we do not add any more items
                # until we once again scan numbers.
                tempEntry = ""
            # If we find that some entries were not numbers, then we display an error and
            # shut down the program.
            except:
                print("Incorrect formatting: Entries are not numbers")
                sys.exit()
        # If we are not scanning a blank space, then we add the current number to the string.
        elif char != " ":
            tempEntry = tempEntry + char
    return array

# A simple method to check that each row has the same length.
def checkMatrixFormat(matrix):
    # For each row, we check to see that its length is the same as the first row. If not,
    # we report failure; otherwise, we report success.
    for row in matrix:
        if len(row) != len(matrix[0]):
            return False
    return True

# Reads the Input.txt file in the directory to create a valid n x m matrix.
def createMatrixFromInput():
    # Opens Input.txt in read mode.
    input = open("Input.txt", "r")
    # This is the total number of lines in the file, excluding the final blank line.
    numLines = len(input.readlines())
    # Resets the reader so that we can go through each line individually.
    input.seek(0)

    # Creates the empty matrix we will add to.
    matrix = []
    # For each line, we use a helper method to create another list, which we add to the matrix.
    for i in range(numLines):
        matrix.append(getArrayFromStr(input.readline()))

    # We check to make sure that the final array is in fact a valid matrix. If not, we display an
    # error, and shut down the program.
    if checkMatrixFormat(matrix) == False:
        print("Incorect formatting: Not all rows are the same length")
        sys.exit()
    return matrix

# A helper method to check whether each value below a certain entry is a 0.
def allZeroesBelow(matrix, row, col):
    # Iterates over each row beneath the current row.
    finalRow = len(matrix) - 1
    iterateRow = row + 1
    numZeroes = 0
    # For each entry, checks if it is a 0; if so, adds to a counter.
    while iterateRow <= finalRow:
        if matrix[iterateRow][col] == 0:
            numZeroes = numZeroes + 1
        iterateRow = iterateRow + 1
    # If the value of the counter is the same as the number of rows beneath, then we return true.
    if numZeroes == finalRow - row:
        return True
    return False

# Adds a multiple of one row to another row. Specifically, adds factor * rowToAdd to rowAddedTo.
def rowAdd(matrix, factor, rowToAdd, rowAddedTo):
    # Finds the index of the last column.
    finalCol = len(matrix[0]) - 1

    # Starts at Column 0, and goes through each, applying the necessary addition.
    iterateCol = 0
    while iterateCol <= finalCol:
        # Applies the necessary row operation for this column. Rounds to two places.
        matrix[rowAddedTo][iterateCol] = round((matrix[rowAddedTo][iterateCol] + factor * matrix[rowToAdd][iterateCol]), 2)
        iterateCol = iterateCol + 1
    return matrix

# Divides a row by a constant.
def matrixDivide(matrix, factor, row):
    # Finds the index of the last column.
    finalCol = len(matrix[0]) - 1

    # Goes through each column, applying the necessary multiplication to the relevant entry.
    iterateCol = 0
    while iterateCol <= finalCol:
        matrix[row][iterateCol] = round((matrix[row][iterateCol] / factor), 2)
        iterateCol = iterateCol + 1
    return matrix

# A helper method to smooth out some jankiness and make the RREF matrix nicer for final display.
def makeMatrixPresentable(matrix):
    # Finds the indexes of the last column and last row.
    finalCol = len(matrix[0]) - 1
    finalRow = len(matrix) - 1

    # Iterates through each column for each row.
    currRow = 0
    while currRow <= finalRow:
        currCol = 0
        while currCol <= finalCol:
            # Sometimes, after float division, Python returns -0.0, which is odd to look at.
            # This simply changes such entries to 0.0.
            if matrix[currRow][currCol] == -0.0:
                matrix[currRow][currCol] = 0.0

            # So far, we've been using float type for division. But writing integers as floats
            # is unpleasant. This checks to see if the current entry is actually an integer,
            # and if so, changes its type to int.
            if matrix[currRow][currCol].is_integer():
                matrix[currRow][currCol] = int(matrix[currRow][currCol])
            currCol = currCol + 1
        currRow = currRow + 1

# Reduces a valid matrix to row echelon form, and then to reduced row echelon form.
def reduce(matrix) :
    # Finds the indexes of the last column and last row.
    finalCol = len(matrix[0]) - 1
    finalRow = len(matrix) - 1


    # Creates a row echelon form of the matrix. See Info.txt for an in-depth description.
    # Iterates primarilly over columns, but keeps track of rows too.
    currCol = 0
    currRow = 0
    while currCol <= finalCol and currRow <= finalRow:
        # Checks to see if the current diagonal (or place we want a pivot) is 0
        if matrix[currRow][currCol] == 0:
            # If it is not the case that there are only values of 0 beneath, then we
            # can add one of those rows to the current row to get rid of its 0
            if allZeroesBelow(matrix, currRow, currCol) == False:
                iterateRow = currRow + 1
                # Finds the first row with a non-zero value, and adds it
                while iterateRow <= finalRow:
                    if matrix[iterateRow][currCol] != 0:
                        matrix = rowAdd(matrix, 1, iterateRow, currRow)
                        break
                    iterateRow = iterateRow + 1
            # If we find that all values beneath are zero, we move on to the next column.
            # Importantly, we do not change the row of focus here; we never found a pivot
            # for this row, so we will look for a pivot in the next column.
            else:
                currCol = currCol + 1
                continue
        # If the entry is not 0 (or we made it not 0), then we add multiples of the current row
        # to all the rows beneath such that every value in the column beneath the 0 also
        # becomes 0.
        iterateRow = currRow + 1
        while iterateRow <= finalRow:
            factor = -1 * (matrix[iterateRow][currCol]) / (matrix[currRow][currCol])
            matrix = rowAdd(matrix, factor, currRow, iterateRow)
            iterateRow = iterateRow + 1
        currCol = currCol + 1
        currRow = currRow + 1

    # Create Reduced Row Echelon form. See Info.txt for in-depth description.
    # Iterates over each row
    currRow = 0
    while currRow <= finalRow:
        iterateCol = 0
        pivot = None
        pivotCol = None
        # Iterates through each value of the row
        while iterateCol <= finalCol:
            # When we find the first value that isn't 0 (i.e. the pivot), we set that as our
            # pivot, note the column of the pivot, and end the loop.
            if matrix[currRow][iterateCol] != 0:
                pivot = matrix[currRow][iterateCol]
                pivotCol = iterateCol
                break
            iterateCol = iterateCol + 1

        # Assuming that we found a pivot, we then add multiples of the current row to each row
        # above so as to make all of the values above the pivot equal 0.
        if pivot != None:
            iterateRow = currRow - 1
            while iterateRow >= 0:
                factor = -1 * (matrix[iterateRow][pivotCol]) / (pivot)
                matrix = rowAdd(matrix, factor, currRow, iterateRow)
                iterateRow = iterateRow - 1
            matrix = matrixDivide(matrix, pivot, currRow)
        currRow = currRow + 1
    return matrix

# Creates a matrix from input, then reduces it
reducedMatrix = reduce(createMatrixFromInput())
# We use a helper method to make the matrix a bit more pleasant for display.
makeMatrixPresentable(reducedMatrix)

# Displays RREF
print("Your matrix has been successfully read. Here is its Reduced Row Echelon Form:")
for element in reducedMatrix:
    print(element)

