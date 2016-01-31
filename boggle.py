#!/usr/bin/env python3
# Python Class 926
# Lesson 11 Problem 1
# Author: suchita (216038)

# Project #3: Boggle Game Player

def get_dictionary(prefixDict):
    '''get_dictionary() -> dict
    Returns dict with each word in the dictionary file
    as both a key and a value
    Creates a prefix based dictionaries by breaking each word into letters'''
    # read each line and make a dictionary so that later we
    # can check whether or not the player's input is a word
    inputFile = open('wordlist.txt','r')
    wordList = inputFile.readlines()
    inputFile.close()
    # create a dictionary
    wordDict = {}
    for word in wordList:
        newWord = word.strip().upper()
        # put each word in the dictionary
        wordDict[newWord] = newWord
        tempDict = prefixDict
        # add each letter in the word to the prefix based dictionary
        for letter in newWord:
            # get the value of each letter or give it the value of an empty
            # dictionary if the letter is not in the dictionary
            tempDict[letter] = tempDict.get(letter, {})
            # tempDict is reassigned to the value of the previous tempDict
            # so that we can build a chain of dictionaries using the
            # letters in the word
            tempDict = tempDict.get(letter)
    return wordDict

def make_grid():
    '''make_grid() -> None
    Makes a 4x4 random grid from the sides of the 16 6-sides dice.'''
    import random
    # sides of dice are in a list with word "False" to show
    # a side of the die has not been placed in the grid yet -
    # when the die is used, "False" is changed to "True"
    dice = [[False, 'AAEEGN'],
            [False, 'ELRTTY'],
            [False, 'AOOTTW'],
            [False, 'ABBJOO'],
            [False, 'EHRTVW'],
            [False, 'CIMOTU'],
            [False, 'DISTTY'],
            [False, 'EIOSST'],
            [False, 'DELRVY'],
            [False, 'ACHOPS'],
            [False, 'HIMNQU'],
            [False, 'EEINSU'],
            [False, 'EEGHNW'],
            [False, 'AFFKPS'],
            [False, 'HLNNRZ'],
            [False, 'DELIRX']]
            
    # represent basic frame of the 4x4 grid
    grid = [[' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ']]

    # for each space in grid
    for row in range(4):
        for column in range(4):
            # choose one of the dice
            randomDie = random.randrange(16)
            die = dice[randomDie] # plural: dice, singular: die
            # move forward till we find an unused die
            while die[0] == True:
                randomDie = (randomDie + 1) % 16
                die = dice[randomDie]
            die[0] == True # mark the die as used
            # choose one of the sides on the die
            randNum = random.randrange(6)
            # place the letter on the side onto the grid
            grid[row][column] = die[1][randNum]
    return grid

def print_grid(grid):
    '''print_grid(list) -> None
    Prints a matrix-like structure with 4 rows and 4 columns'''
    # for each space in the grid
    for row in range(4):
        for column in range(4):
            # create grid to show player
            print(grid[row][column] + "  ",end='')
        print('\n')
    return

def copy_list(oldList):
    '''copy_list(list) -> list
    Returns a copy of the previous list'''
    newList = []
    # make a new list to change
    for item in oldList:
        newList.append(item)
    return newList

def get_neighbor_positions(position):
    '''get_neighbor_positions(list) -> list
    Returns a list of positions where a surrounding letter can be'''
    # 8 places for surrounding letters to be
    row = position[0]
    column = position[1]
    # these are the possible positions where the neighboring letter can be
    possibleNeighborPositions = [[row - 1, column - 1], [row - 1, column],
                         [row - 1, column + 1], [row, column - 1],
                         [row, column + 1], [row + 1, column - 1],
                         [row + 1, column], [row + 1, column + 1]]
    neighborPositions = []
    # go through each possible position
    for positions in possibleNeighborPositions:
        # some spaces are not surrounded by letters on 8 sides
        if positions[0] > -1 and positions[0] < 4:
            if positions[1] > -1 and positions[1] < 4:
                # the position has a letter in it
                neighborPositions.append(positions)
    return neighborPositions

def get_matching_positions(grid, currentPosition, letter, visitedLetters):
    '''get_matching_positions(list, list, string, list) -> list
    Returns a list of positions where letter is when only
    looking at the positions surrounding the previous letter'''
    neighbors = get_neighbor_positions(currentPosition)
    matchingPositions = []
    # go through each position
    for position in neighbors:
        if position not in visitedLetters:
            # find out what the row and column of the position is
            row = position[0]
            column = position[1]
            # check if the letter is in this position
            if grid[row][column] == letter:
                matchingPositions.append(position)
    return matchingPositions

def is_in_grid(word, grid, visitedLetters):
    '''is_in_grid(string, list, list) -> boolean
    Returns True if word is in grid and False otherwise'''
    # stop when the whole word has been found
    if len(word) == len(visitedLetters):
        return True
    # this is how many letters in the word we have gone through
    letterIndex = len(visitedLetters)
    # the computer starts counting at 0
    nextLetter = word[letterIndex]
    # this is where we are now
    currentPosition = visitedLetters[letterIndex - 1]
    # find possible places for letter to be around the letter
    matchingPositions = get_matching_positions(grid, currentPosition,
                                             nextLetter, visitedLetters)
    # cannot find letter in grid
    if len(matchingPositions) == 0:
        return False
    for position in matchingPositions:
        # we do not want to change the original list
        newVisitedLetters = copy_list(visitedLetters)
        newVisitedLetters.append(position)
        # we do not need to find another of the same word
        if is_in_grid(word, grid, newVisitedLetters):
            return True
    return False

def find_starting_positions(letter, grid):
    '''find_starting_positions(string, list) -> list
    Returns a list of positions where a letter occurs in the grid'''
    newList = []
    # go through each space in grid
    for row in range(4):
        for column in range(4):
            # check if the letter is in  the position
            if grid[row][column] == letter:
                newList.append([row, column])
    return newList

def is_not_already_used(word, scoreList):
    '''is_not_already_used(string, list) -> boolean
    Returns True if word has not been used and False otherwise'''
    for item in scoreList:
        # we used the word already
        if word == item[0]:
            return False
    return True
    
def get_score(word):
    '''get_score(string) -> int
    Returns score for a word'''
    # score depends on length
    length = len(word)
    if length == 3 or length == 4:
        score = 1
    elif length == 5:
        score = 2
    elif length == 6:
        score = 3
    elif length == 7:
        score = 4
    else:
        score = 6
    # value of each word is returned
    return score

def print_scores(scoreList):
    '''print_scores(list) -> None
    Prints score for each word and prints total score'''
    print("Here's your score:")
    # print the value of each word
    for item in scoreList:
        print(item[0] + " scores " + str(item[1]))
    totalScore = 0
    # find the total of the scores
    for item in scoreList:
        totalScore += item[1] 
    print("TOTAL SCORE: " + str(totalScore))
    print("Thanks for playing!")

def get_matching_prefixes(prefixDict, position, grid, visitedLetters):
    '''get_matching_prefixes(dict, list, list, list) -> list
    Returns all matching positions in dictionary'''
    neighbors = get_neighbor_positions(position)
    matchingPositions = []
    # go through each position
    for position in neighbors:
        if position not in visitedLetters:
            # find out what the row and column of the position is
            row = position[0]
            column = position[1]
            # check if the letter is in this position
            if grid[row][column] in prefixDict:
                # add this position to list
                matchingPositions.append(position)
    return matchingPositions

def word_from_visited_letters(grid, visitedLetters):
    '''word_from_visited_letters(list, list) -> string
    Returns word from positions of visited letters'''
    # we will concatenate various letters to this
    word = ''
    for position in visitedLetters:
        r = position[0]
        c = position[1]
        # letters are joined together into word
        word = word + grid[r][c]
    return word

def find_longest_word(prefixDict, dictionary, grid, visitedLetters,
                      longestWord):
    '''find_longest_word(dict, dict, list, list, string) -> string
    Returns longest word one can make from a certain starting point
    Most of the code is based on is_in_grid()'''
    # stop when you have reached the current dictionary path
    if len(prefixDict) == 0:
        return longestWord
    
    # this is how many letters in the word we have gone through
    letterIndex = len(visitedLetters)
    # this is where we are now
    currentPosition = visitedLetters[letterIndex - 1]
    # find possible places for letter to be around the letter
    matchingPositions = get_matching_prefixes(prefixDict, currentPosition,
                                              grid, visitedLetters)
    
    # cannot find letter from the prefix dictionary in the grid
    if len(matchingPositions) == 0:
        return longestWord
    
    for position in matchingPositions:
        # we do not want to change the original list
        newVisitedLetters = copy_list(visitedLetters)
        newVisitedLetters.append(position)
        # form a word from newVisitedLetters
        word = word_from_visited_letters(grid, newVisitedLetters)
        if len(word) > len(longestWord) and word in dictionary:
            #print(word + ' replaces ' + longestWord + ' as longest')
            # word replaces longestWord as longest
            longestWord = word
        currentLetter = word[len(word) - 1]
        #print(word)
        # we want to find a longer word
        returnedWord = find_longest_word(prefixDict[currentLetter], dictionary,
                                         grid, newVisitedLetters, longestWord)
        if len(returnedWord) > len(longestWord) and returnedWord in dictionary:
            #print(returnedWord + ' replaces ' + longestWord + ' as longest')
            # returnedWord replpaces longestWord as longest
            longestWord = returnedWord

    return longestWord

def print_longest_word(grid, dictionary, prefixDict):
    '''print_longest_word(list, dict) -> string
    Prints message and longest word in grid'''
    print("Let me see...I bet I can find a long word.")
    print("Please give me a moment to think...")
    longestWord = ''
    # going through each position in the grid
    for row in range(4):
        for column in range(4):
            position = [row, column]
            visitedLetters = [position]
            # find the longest word when starting from position
            word = find_longest_word(prefixDict, dictionary, grid,
                                     visitedLetters, longestWord)
            if len(word) > len(longestWord) and word in dictionary:
                #print(word + ' replaces ' + longestWord + ' as longest')
                # word replaces longestWord as longest
                longestWord = word
    print('I found ' + longestWord)
            
def play_game(wordDict, grid, prefixDict):
    '''play_game(dict, list, dict) -> None
    Plays boggle until player inputs a blank
    Prints a grid and asks player to enter word on grid
    Print various responses depending on validity of word given by player
    Print scores and game ends
    Prints longest possible word to create'''
    done = False
    # we do not have any scores yet
    scores = []
    # when the game is running
    while done == False:
        print_grid(grid)
        # letters are made uppercase to make everything easier
        playerInput = input("Enter your word (leave blank to quit): ").upper()
        # if game is not stopped
        if playerInput != '' and playerInput != ' ':
            # word is long enough
            if len(playerInput) >= 3:
                # word has not been used
                if is_not_already_used(playerInput, scores):
                    # word is a real word
                    if playerInput in wordDict:
                        # find out where first letter is
                        positions = find_starting_positions(playerInput[0],
                                                            grid)
                        foundInGrid = False
                        # go through each possible starting point
                        for position in positions:
                            if not foundInGrid:
                                # we have checked this position
                                visitedLetters = [position]
                                if is_in_grid(playerInput, grid,
                                              visitedLetters):
                                    # word can be found in grid
                                    foundInGrid = True
                                    print(playerInput + " is a valid word!\n")
                                    # record score
                                    score = get_score(playerInput)
                                    scores.append([playerInput, score])
                        # word is not in grid
                        if not foundInGrid:
                            print(playerInput + " is NOT in grid!\n")
                    # word is not a real word
                    else:
                        print(playerInput + " is NOT in the dictionary!\n")
                # word has been used
                else:
                    print(playerInput + " has already been used!\n")
            # word is not long enough
            else:
                print(playerInput + " is NOT at least 3 letters long!\n")
        # game is over
        else:
            # print scores
            print_scores(scores)
            print_longest_word(grid, dictionary, prefixDict)
            # stop while loop
            done = True
    return

prefixDict = {}
dictionary = get_dictionary(prefixDict)
grid = make_grid()
# play boggle
play_game(dictionary, grid, prefixDict)
