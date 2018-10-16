import os
import itertools
import collections
import random
import math

script_dir = os.path.dirname(__file__) 
rel_path = "aclImdb/imdbEr.txt"
abs_file_path = os.path.join(script_dir, rel_path)

file = open(abs_file_path, "r")

lines = file.readlines()
lines[:] = [line.rstrip('\n') for line in lines]
file.close()
linenu=0
c = len(lines)
nu = list()


for i in range(1,c+1):
	nu.append(i)

tuple = zip(lines, nu)

sorted_tuple = sorted(tuple, key=lambda tup: float(tup[0]))
#print(sorted_tuple)

pos_sorted_tuple=sorted_tuple[87027:89527]
# neg_sorted_tuple=sorted_tuple[17731:20231]
neg_sorted_tuple = sorted_tuple[:2500]
# for item in neg_sorted_tuple:
# 	print(item)

file = open("selected-features-indices.txt","w")
for item in neg_sorted_tuple:
	file.write(str(item[1]))
	file.write('\n')

for item in pos_sorted_tuple:
	file.write(str(item[1]))
	file.write('\n')
file.close()
