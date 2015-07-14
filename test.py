from __future__ import print_function
import nolambda

l = [1, 2, 3, 4, 5]

#print(map(_ + 1, l))
print(map(str(_ * _) + str((_ + 1) * 2), l))

l2 = [[0,1,2], [1,2,3], [2,3,4], [3,4,5], [4,5,6], [5,6,7]]
print(filter(5 in _, l2))

print(filter((5 in _) and (4 in _), l2))

