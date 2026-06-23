def generate_matrix(n , m ):
    matrix = []
    for i in range(n):
        test = []
        for j in range(m):
            test.append(i+j)
        matrix.append(test)
    return matrix


print(generate_matrix(3,3))


# transposing a  matrix 
# [[1,2,3],
#  [4,5,6],
#  [7,8,9]]

#generate a 4 x 4 matrix 
# [[1,2,3,4],
#  [5,6,7,8],
#  [9,10,11,12],
#  [13,14,15,16]]

# generate a 4 x 4 matrix transpose 
#  [[1,5,9,13],
#   [2,6,10,14],
#   [3,7,11,15],
#   [4,8,12,16]]

# [[1,4,7],
#  [2,5,8],
#  [3,6,9]]

# [[0, 1, 2],
#  [1, 2, 3], 
# [2, 3, 4]]


# def generate_matrix_transpose(matrix ):
#     for i in range(len(matrix )):
#         for j in range(i , len(matrix[i])):
#             matrix[i][j] , matrix[j][i] = matrix[j][i] , matrix[i][j]
#         return matrix 


# print(generate_matrix_transpose(generate_matrix(3,3)))


# def add_one(x):
#    return x + 1

# def triple(x):
#    return 3 * x

# def square(x):
#    return x * x

# composed_fn = compose(square, add_one)
# print(composed_fn(3))  # Output: 16

# result = compose(square, add_one, triple)(3)
# print(result)  # Output: 100


# composer function here : 
# def outvalue(val):
#     def compose(*funcs):
#         for func in funcs:
#             val = func(val)
#         return val
#     return compose
            



# Permuatation algo to make sum of 20 from 1 to 1000 
# def is_sum_20(n):
#     sum = 0
#     while n > 0:
#         digit = n % 10
#         sum += digit
#         n = n // 10
#     return sum ==  20



# def sum_20():
#     count =0
#     for i in range(299, 1001):
#         print(is_sum_20(i))
#         if is_sum_20(i):
#             count += 1
#     return count



print(sum_20())
            

    

