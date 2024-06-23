import pprint

matrix = [[1, 2, 3, 4, 5, 6, 7, 2, 1, 2], [2, 63, 1, 234, 5, 6, 1, 2, 4, 56], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [2, 2, 2, 2, 2, 2, 2, 2, 2], [3, 3, 3, 33, 3, 3, 3, 3, 3]]

pprint.pprint(matrix)
print("1: ", matrix[0])
print("2: ", matrix[:2])
print("3: ", matrix[0][2:8])
