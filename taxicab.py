# Python Class 926
# Lesson 5 Problem 8
# Program for finding Taxicab numbers - https://simple.wikipedia.org/wiki/Taxicab_number
# Author: suchita (216038)

def cube(x):
    return x * x * x

def taxicab(n):
    for a in range(1, n + 1):
        a3 = cube(a)
        # skip cubes larger than n
        if a3 <= n:
            # for second number, look for numbers after a
            for b in range(a+1, n+1):
                b3 = cube(b)
                sumCubedOne = a3 + b3
                # skip cubed sums larger than n
                if sumCubedOne <= n:
                    for c in range(a+1, n+1):
                        c3 = cube(c)
                        # skip cubes larger than sumCubedOne
                        if c3 <= sumCubedOne:
                            # for second number, skip numbers smaller than c
                            for d in range(c+1, n+1):
                                d3 = cube(d)
                                sumCubedTwo = c3 + d3
                                if sumCubedOne == sumCubedTwo:
                                    print(str(sumCubedOne) + " is a Taxi Cab number that can be written as ",
                                          str(a) + "^3 + " + str(b) + "^3 = " +
                                          str(c) + "^3 + " + str(d) + "^3 = " +
                                          str(sumCubedTwo)) 
                                    
                    
taxicab(10000)
