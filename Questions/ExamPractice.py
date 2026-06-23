# In Python, an object is considered falsy if it is:
# None
# False
# Zero (0, 0.0, 0j)
# Empty sequences or collections (”, [], {}, (), set())


# round() takes you nearest even number 
# // takes to the nearest negative infinity
# int() takes to the nearest zero
# print(int(-2.9))
# print(round(-2.5))
# print(round(-3.4))
# print(-2.9//1)




# --- Precedence Order Rules ---
# Precedence order determines which operation to calculate first (like PEMDAS).
# Precedence (high → low):
# 1. ** (Exponents / Powers) — calculated first
# 2. unary - (Negative sign)
# 3. * / // % (Multiplication, Division, Floor Division, Modulo)
# 4. + - (Addition, Subtraction)
# 5. comparisons (>, <, ==)
# 6. not
# 7. and
# 8. or — calculated last

# The ** operator is purely "right-associative", which is a tricky exception.
# It means it evaluates right to left, rather than left to right:
# 2 ** 3 ** 2   # -> 512
#             = 2**(3**2) = 2**9 = 512




#  Trenary Operator
# check = True if 1==1 else False

#ALternative of trenary operator

# check = ("This is the wrong string", "This is the correct string")[1==1]
# print(check)






# Kwwargs ** and args *
# args is used to pass variable number of arguments and it is a tuple
# kwargs is used to pass variable number of keyword arguments and it is a dictionary

# def myfunc(*args, **kwargs):
#     print(args)
#     print(kwargs)

# myfunc(1, 2, 3, 4, 5, name="John", age=30, city="New York")




#UNPACING OPERATOR
# * is used to unpack iterables (lists, tuples, strings)
# ** is used to unpack dictionaries

# list1 = [1, 2, 3]
# list2 = [4, 5, 6]
# list3 = [*list1, *list2]
# print(list3)

# dict1 = {"name": "John", "age": 30}
# dict2 = {"city": "New York", "country": "USA"}
# dict3 = {**dict1, **dict2}
# print(dict3)



# / and * in function arguments 
# if any argument is before / it is positional only argument
# if any argument is after * it is keyword only argument

# def myfunc(a, b, /, c, d, *, e, f):
#     print(a, b, c, d, e, f)

# myfunc(1, 2, 3, 4, e=5, f=6) # right as e , f takes as keyword argument

#Before the / ➡️ You must pass the raw value WITHOUT a name.
#After the * ➡️ You must pass the value WITH a name (Keyword).
#In the middle (or if left unspecified) ➡️ You can do whatever you want! (Name or No Name).




# LAMBDA FUNCTIONS 

# ans = lambda x : x**3
# print(ans(3))
# temp = [1,2,3,4,5,6,7,8,9,10]
# This iterates over the list , by each value goes to the map
# ans = list(map(lambda x : x**2 , temp))
# print(ans)
# This takes as key and we return values as per that 
# ans = sorted(ans , key = lambda x: -x) 
# print(ans)
# This takes lambda pass every list value , but list is also using sort that use lambd 
# ans = list(filter(lambda x: x>-5, sorted(ans , key = lambda x: -x) ))
# print(ans)




# CLOSURES 
# def make_counter():
#     count =0
#     def counter():
#         count=0 # in this case count is local variable and python updating local variable
#         count +=1
#         return count
#     return counter

# def make_counter():
#     count =0
#     def counter():
#         nonlocal count # without nonlocal it will give error because  python thinks count is local variable and it is not assigned any value
#         count +=1
#         return count
#     return counter

# counter = make_counter()
# print(counter())





# List accesssing

# arr[start : end : step]
# start is inclusive
# end is exclusive
# step is the increment

# if you leave the second argument empty it will go till the end of the list
# if you leave the first argument empty it will go from the beginning of the list
# if you leave the third argument empty it will increment by 1

# arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# print(arr[1::2])  jumping 2 steps and going to the en d






# LIST COMPREHENSION
# list Trap :

# ans = [[0]*3]*3
# ans[0][0]= 1
# print(ans)
# changes value of first index of each sub array 


# ans = [0]*3 # here you createing copy of integers not list
# ans[0]= 1
# print(ans)



#


# <------- Practicing Questions ---------->


# words = ["apple", "bat", "banana", "cat"]
# print(sorted(words , key = lambda x : len(x)))


# points = [(2,9), (1,15), (5,4)]
# print(sorted(points , key = lambda x : x[0]+x[1]))


# square of all even numbers 
# print([x**2 for x in range(1,16) if x%2==0])


# given matrix write a one liner 
# matrix = [[1,2],[3,4],[5,6]]
# print([x for x in matrix for x in x])



#sorting by last names 
# names = ["Alice", "Bob", "Charlie", "Dave"]
# print(sorted(names , key= lambda x :x[-1]))


# write a method


# def primte(n):
#     print([x for x in range(2 , n+1) if all(x%y!=0 for y in range(2 , x))])

# primte(10)



# data = [[1,-2,3],[-4,5],[6,-7,8,-9]]

# print([y for  x in data for y in x if y >0])


# data = [[1,2,3],[4,5,6],[7,8]]

# print([ [y for x in data for y in x if y == min(x)] , [y for x in data for y in x if y == max(x)]])

# <------- Zip & Tuple Practice Questions ---------->

# Question 1: Simple Pairing
# Given two lists: names = ["Alice", "Bob", "Charlie"] and ages = [25, 30, 35]
# Write a one-liner that returns: [('Alice', 25), ('Bob', 30), ('Charlie', 35)]


# Question 2: Triples (3-way zip)
# Given three lists: x = [1, 2], y = [10, 20], z = [100, 200]
# Write a one-liner that returns a list of triples: [(1, 10, 100), (2, 20, 200)]


# Question 3: Enumerating with Zip
# Given a list of words: words = ["apple", "banana", "cherry"]
# Use zip() and range() to create a list of tuples with their index:
# Output: [(0, "apple"), (1, "banana"), (2, "cherry")] 


# Question 4: String Analytics One-Liner (Exam Level)
# Given a list: fruits = ["kiwi", "mango", "pear"]
# Create a list of tuples where each tuple is (word, length_of_word, first_letter)
# Expected Output: [('kiwi', 4, 'k'), ('mango', 5, 'm'), ('pear', 4, 'p')]


# max_diff


# result = max(data , key = lambda x : max(x)-min(x))
# print(result)


# func_perfect 
# def func_perfect(n):
#     print([x for x in range(1 , n+1) if all(x%y!=0 for y in range(2 , x))])

# func_perfect(10)

# [0]
# [0 , [0]  ]
# [0 , [0] , 0]
# [0 , [0] , 0 , 1]
# [0 , [0] , 0 , 1 , [1]]
# [0 , [0] , 0 , 1 , [1] , 1]






# a = [['Zabie','Gaker'], ['Zable','Aaker']]
# print(sorted(a , key = lambda x : (x[1].lower() , x[0].lower())))


# a = [[1,5,3] , [4,1,] , [7,0,9]]

# print(sorted(a , key = lambda x :sum(x)/len(x)))

def special_event(n):
    return []