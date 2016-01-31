# Boggle Game Player
**Final Project from the Art of Problem Solving Python Programming Course**

- This is the third problem described in the PDF file AOPS-python-homework-12.pdf. My solution differs from the provided ways of solving the problem.
- The program generates a 4x4 game board for the player
- Asks the player to enter a word, checks that the word is valid in a dictionary and is a valid word on the displayed board.
- Keeps track of user's scores
- Exits after displaying longest possible word for that board layout.

Limitations:
- Board generation is hard coded for a 4x4 board, but that part should not be too hard to generalize.

## Details
- My program begins with the function getDictionary(), which reads the lines in a file and creates a new dictionary. The function puts each word in the dictionary with the word as both the key and value. It returns the dictionary. To do the optional part of the project, this function also creates a prefix dictionary - I will describe details of the prefix dictionary later.
- Then, the function makeGrid() makes a grid by choosing a random die from the 16 Boggle dice and then picking a random side of that die. No die is reused. It then fills the first available blank space in the grid with the selected letter on the die. I keep the 16 Boggle dice in a list. Each member of the Boggle Dice list is itself a list - each with two members. If the first member (at 0th index) of the die is False, that means it has not been used yet. The second member contains all six letters on the die. If after randomly selecting a die from 16 dice, we find a die that has been used, we keep moving to the next die ((position + 1) modulo 16) until we find a die that has not yet been used. Once such an unused die has been found, we set the 0th element of the die to True to mark it as used and one of the sides of the die with a letter is randomly chosen. That letter is placed in the proper position in the frame of the grid, and eventually, the completed grid is returned.
- With the grid and dictionary ready, we can now run the game like this:
```
While game is ON:
1. Print grid of letters to play with [printGrid()]
2. Get the player’s input
3. If the input is not a blank:
    If input is at least 3 letters long, has not already been successfully used and is a real word in the dictionary:
      Find all positions in the grid where the first letter of the input appears
        For each possible starting position in the grid of first letter of the word [findStartingPositions()]:
          Mark the starting position as used by adding it to visitedLetters list
          If rest of the letters of the word are in the grid [isInGrid()]: 
            Print appropriate message
            Record score in list of scores
    Else:
      Print appropriate message
   Else:
     Print total score and all valid words entered by player with the corresponding score. Game is over.
# End of the while loop
```
- The fundamental piece of this program is the isInGrid() function. Its purpose is to figure out whether or not a word is present in the grid - it returns True when the whole word has been found or False if it has not. The main idea is to check all neighbors from the current position in grid and select some of the neighbors to recursively search for the next candidate letter. We only pick neighboring letters that we have not visited before and that match the next letter in the word that user typed. I used a list called visitedList to keep the visited positions [row, column] on the grid. This new visitedList is the only thing that changes in each recursive call. This list tells us two things:
  1. the length of this list tells us which is the next letter in the word being checked
  2. the last item of this list tells us the current position in the grid.
- One important thing is that I had to make a new copy of the visitedList every time I was ready to recurse so that I would not modify the visitedList that was passed in to the current call of isInGrid().
isInGrid() uses a helper function called getMatchingPositions() that first generates a list of all neighbors. For example, it returns 3 neighbors in a list for a corner letter, but returns 8 neighbors for a center letter. From these neighbors, it selects the non-visited neighbors that have a matching letter and adds them to a list called matchingPositions, which is returned back to isInGrid().

### Optional part of project: Finding the longest word in the grid:
- I used most of my code from the isInGrid() function to do this part. As I described before, this function checks all neighbors of the current position in grid and selects some of these neighbors to recursively search. In the case of the Boggle game player, we only pick neighboring letters that match the next letter in the word that the user typed. In case of finding the longest word we have to match the next possible letter sequences that will create a valid word in the dictionary. We will have to build a special purpose dictionary for this that will contain ALL valid letter sequences for all words in the basic word dictionary. For example, if the word dictionary contains words BAM, BAN, BAT, BET and BEST, the letter sequence dictionary will contain word sequences stored in nested dictionaries with nesting level as deep as the longest word in the dictionary.It will have a structure like this:

```
B : { A : { M : {},
                N : {},
                T : {}
                },
        E : { S : { T : {}
                        },
              T : {}
                  }
       }
```

- Using this type of dictionary, we can check all neighbors of the current letter and select only the neighbors whose letter matches the letter sequence in the dictionary. We can keep recursing until we either find the end of a sequence in the dictionary or can find no usable neighbors in the grid.
We could write a simple minded search for this, without using this letter-sequence dictionary. However, this requires generating all possible word sequences within the grid. I think this would be incredibly slow and wasteful because this might require generating more than a billion candidate words, based on a rough estimate.

### Testing:
- I tested out my program in various ways. One of my games is shown below to show this. The grid follows:
```
HORE OETI EEOC AUNT
```
- I started out with various words that could be found on the grid such as:
```
ore, tore, teen, toe, aunt, cite, tire, hot, ton, tic, cot, hoe, rote, tone, cone, and noir.
```
- Then, I tried out a word "cit", which I did not believe to be a word, to make sure my program was working correctly. As expected, the program asked me to enter another word. It did the same for the word "eeoc".
- I tried out "tore", which had obviously been used already, and the program asked me to enter another word. Furthermore, I tried out "it", which was obviously too short (being less than 3 letters long), and the program asked me to enter another word.
- I continued the game and ended with a total score of 22. The program also told me that the longest possible word to make in the grid was "tricot".
- I played many other games like this on the Boggle Player to ensure the program worked. For example, sometimes, I checked to make sure I had not repeated a position that had already be used to create a word. If a grid had an "S" and an "I" on it, then I would not able to write out the word "sis". I performed similar tests on other cases and am fairly satisfied with the results. Here are some other test runs I did:
```
RAII IAHJ RURV ATBD
Enter your word (leave blank to quit): Here's your score:
TOTAL SCORE: 0
Thanks for playing!
Let me see...I bet I can find a long word. Please give me a moment to think...
I found URARI
```
- Another test run with different types of player mistakes I checked for:
```
OWPO
MUWN
ISRL
LRTT
Enter your word (leave blank to quit): mom MOM is NOT in grid!
OWPO
MUWN
ISRL
LRTT
Enter your word (leave blank to quit): pow POW is a valid word!
OWPO MUWN ISRL LRTT
Enter your word (leave blank to quit): zzbb ZZBB is NOT in the dictionary!
OWPO
MUWN
ISRL
LRTT
Enter your word (leave blank to quit): sum SUM is a valid word!
OWPO
MUWN
ISRL
LRTT
Enter your word (leave blank to quit): sum SUM has already been used!
OWPO
MUWN
ISRL
LRTT
Enter your word (leave blank to quit): no NO is NOT at least 3 letters long!
OWPO MUWN ISRL LRTT
Enter your word (leave blank to quit): Here's your score:
POW scores 1
SUM scores 1
TOTAL SCORE: 2
Thanks for playing!
Let me see...I bet I can find a long word. Please give me a moment to think...
I found STRUM
```
