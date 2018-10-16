import os
import itertools
import collections
import random


script_dir = os.path.dirname(__file__) 
rel_path = "aclImdb/train/labeledBow.feat"
abs_file_path = os.path.join(script_dir, rel_path)

file = open(abs_file_path, "r")

lines = file.readlines()
lines[:] = [line.rstrip('\n') for line in lines]
file.close()

selected_instances = list()    #list containing 500+ and 500- instances

count=0
poscount=0
negcount=0

while count<1000:
	d = random.choice(lines)
	if d not in selected_instances:
		v = d[0]
		b = int(v)
		c = d[1]

		if c==' ':
			if b>=7:
				if poscount!=500:
					poscount=poscount+1
					selected_instances.append(d)
					count =count+1
			if b<=4:
				if negcount!=500:
					negcount=negcount+1
					selected_instances.append(d)
					count=count+1
		else:
			if poscount!=500:
				poscount=poscount+1
				selected_instances.append(d)
				count=count+1


file = open("train_data.txt","w")

for item in selected_instances:
	file.write(item)
	file.write('\n')
file.close()	


script_dir = os.path.dirname(__file__) 
rel_path = "aclImdb/test/labeledBow.feat"
abs_file_path = os.path.join(script_dir, rel_path)

file = open(abs_file_path, "r")

lines = file.readlines()
lines[:] = [line.rstrip('\n') for line in lines]
file.close()

selected_test_instances = list()    #list containing 500+ and 500- instances


count=0
test_pos_count=0
test_neg_count=0

while count<1000:
	d = random.choice(lines)
	if d not in selected_test_instances:
		v = d[0]
		b = int(v)
		c = d[1]

		if c==' ':
			if b>=7:
				if test_pos_count!=500:
					test_pos_count=test_pos_count+1
					selected_test_instances.append(d)
					count =count+1
			if b<=4:
				if test_neg_count!=500:
					test_neg_count=test_neg_count+1
					selected_test_instances.append(d)
					count=count+1
		else:
			if test_pos_count!=500:
				test_pos_count=test_pos_count+1
				selected_test_instances.append(d)
				count=count+1

file = open("test_data.txt","w")

for item in selected_test_instances:
	file.write(item)
	file.write('\n')
file.close()