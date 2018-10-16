import os
import itertools
import collections
import random
import math
import sys

experiment_no = sys.argv[1]

script_dir = os.path.dirname(__file__) 
rel_path = "selected-features-indices.txt"
abs_file_path = os.path.join(script_dir, rel_path)

file = open(abs_file_path, "r")
selected_features = file.readlines()
selected_features[:] = [line.rstrip('\n') for line in selected_features]
file.close()

#print(selected_features)
num = list()
for i in range(0,5000):
	num.append(i)

for i in range(len(selected_features)):

	cc=int(selected_features[i])
	cc=cc-1
	selected_features[i] = str(cc)
	

features_dic= dict(zip(selected_features,num))
#print(features_dic)
#--------------------------------------------------

script_dir = os.path.dirname(__file__) 
rel_path = "train_data.txt"
abs_file_path = os.path.join(script_dir, rel_path)

file = open(abs_file_path, "r")

selected_instances = file.readlines()
selected_instances[:] = [line.rstrip('\n') for line in selected_instances]
file.close()



label=list()

for d in selected_instances:
	v = d[0]
	b = int(v)
	c = d[1]

	if c==' ':
		if b>=7:
			label.append(1)
		if b<=4:
			label.append(-1)
	else:
		label.append(1)	
matrix = list()



for item in selected_instances:
	length = len(item)
	count=0
	col =list()
	for kk in range(1,5001):
		col.append(0)

	
	# while count!=length:
	# 	flag=0
	# 	while(count!=length):
	# 		if item[count]==' ':
	# 			break
	# 		count=count+1
	# 	if count==length:
	# 		break	
	# 	count=count+1
	# 	stri = item[count]
	# 	count=count+1
	# 	while(item[count]!=':'):
	# 		stri = stri+item[count]
	# 		count=count+1
	# 	if stri in features_dic:
	# 		col[features_dic[stri]]=1
	it_list = item.split()
	for it in it_list[1:]:
		features = it.split(':')
		if features[0] in features_dic.keys():
			# print(features[0])
			col[features_dic[features[0]]] = 1

	matrix.append(col)


index=0
for item in matrix:
	item.insert(0,label[index])
	index=index+1


file = open("test.txt", "w")
for key in matrix[5]:
	file.write(str(key))
	file.write('\n')
#-------------------------------------------------

script_dir = os.path.dirname(__file__) 
rel_path = "test_data.txt"
abs_file_path = os.path.join(script_dir, rel_path)

file = open(abs_file_path, "r")

selected_test_instances = file.readlines()
selected_test_instances[:] = [line.rstrip('\n') for line in selected_test_instances]
file.close()

test_label=list()

for d in selected_test_instances:
	v = d[0]
	b = int(v)
	c = d[1]

	if c==' ':
		if b>=7:
			test_label.append(1)
		if b<=4:
			test_label.append(-1)
	else:
		test_label.append(1)	



test_matrix = list()

for item in selected_test_instances:
	length = len(item)
	count=0
	col =list()
	for kk in range(1,5001):
		col.append(0)

	# while count!=length:
	# 	flag=0
	# 	while(count!=length):
	# 		if item[count]==' ':
	# 			break
	# 		count=count+1
	# 	if count==length:
	# 		break	
	# 	count=count+1
	# 	stri = item[count]
	# 	count=count+1
	# 	while(item[count]!=':'):
	# 		stri = stri+item[count]
	# 		count=count+1
	# 	if stri in features_dic:
	# 		col[features_dic[stri]]=1

	it_list = item.split(' ')
	for it in it_list[1:]:
		features = it.split(':')
		if features[0] in features_dic.keys():
			# print(features[0])
			col[features_dic[features[0]]] = 1

	test_matrix.append(col)	

index=0
for item in test_matrix:
	item.insert(0,test_label[index])
	index=index+1

#------------------------------
def height(node):
    if node.left==None and node.right==None:
        return 0; 
 
    else :
        lDepth = height(node.left)
        rDepth = height(node.right)

        if (lDepth > rDepth):
            return lDepth+1
        else:
            return rDepth+1


#--------------------------------------------------

class tree_node:
	def __init__(self):
		self.feature =0
		self.left =None
		self.right =None
		self.pu = 0
		self.nu = 0
		self.height=0
		

		


#---------------
def checkpos(examples,matrix):
	flag=1	
	for item in examples:
		if matrix[item][0]!=1:
			flag=0
			break
			
	return flag		

def checkneg(examples,matrix):
	flag=1	
	for item in examples:
		if matrix[item][0]!=-1:
			flag=0
			break
	return flag		


def calc(examples,matrix):
	countpos=0
	for item in examples:
		if (matrix[item][0]==1):
			countpos=countpos+1
	return countpos		


def entropy(pos,neg):
	pos=float(pos)
	neg=float(neg)
	pos_ratio=float(0)
	neg_ratio=float(0)
	pos_log=float(0)
	neg_log=float(0)
	if(pos!=0):
		pos_ratio = pos*1.0/(pos+neg)
		pos_log = math.log(pos_ratio,2)
	if neg!=0:
		neg_ratio = neg*1.0/(pos+neg)
		neg_log = math.log(neg_ratio,2)
	if pos==0 or neg==0:
		return float(0)
	return -pos_ratio*pos_log - neg_ratio*neg_log

def info_gain(boss_entropy,examples,matrix,att):
	posmore=0
	posless=0
	negmore=0
	negless=0

	for exam in examples:
		if(matrix[exam][att]==1):
			if(matrix[exam][0]==1):
				posmore=posmore+1
			else:
				negmore=negmore+1
		else:
			if(matrix[exam][0]==1):
				posless=posless+1
			else:
				negless=negless+1
	posentropy = entropy(posmore,negmore)							
	negentropy = entropy(posless,negless)

	pos_sum=float(posmore+negmore)
	neg_sum=float(posless+negless)
	total = pos_sum+neg_sum
	baby_entropy = 	(pos_sum/total)*posentropy + (neg_sum/total)*negentropy
	if baby_entropy==0.0:
		return -1
	#print(baby_entropy)
	return boss_entropy-baby_entropy						

def find_feature(boss_entropy,examples,matrix,attributes):
	temp = 0
	selected_feature=-1
	for attribute in attributes:
		i_gain = info_gain(boss_entropy,examples,matrix,attribute)
		

		if i_gain>(temp+1e-3):
			selected_feature=attribute
			temp=i_gain
	#print(temp)		
	return selected_feature		


def ID3(examples,matrix,attributes,height=0):
	
	root = tree_node()
	root.height=height
	if checkpos(examples,matrix)==1 or checkneg(examples,matrix)==1:
		if(checkpos(examples,matrix)==1):
			root.pu=1
			root.nu=0
		else:
			root.nu=1
			root.pu=0	
		return root
	
	total = len(examples)
	positive = calc(examples,matrix)
	negative = total-positive
	#print(positive)
	#print(negative)
	root.pu = positive
	root.nu = negative
	boss_entropy =entropy(positive,negative)
	
	selected_feature = find_feature(boss_entropy,examples,matrix,attributes)	
	#print('selected feature:')
	#print(selected_feature)
	if selected_feature==-1:
		return root		
	root.feature=selected_feature
	#attributes.remove(selected_feature)
	
	example1=list()
	example2=list()
	
	for lp in examples:
		if matrix[lp][selected_feature]==1:
			example2.append(lp)
		else:
			example1.append(lp)	
	
	
	root.left = ID3(example1,matrix,attributes,height+1)
	root.right = ID3(example2,matrix,attributes,height+1)
	
	return root	
		
def LeafCount(node,height=9999):
    if node is None:
        return 0
    if((node.left is None and node.right is None)or height==0):
        return 1
    else:
        return LeafCount(node.left,height-1) + LeafCount(node.right,height-1)


def NodeCount(node,height=9999):
    if not node or height==0:
        return 0

    return 1 + NodeCount(node.left,height-1) + NodeCount(node.right,height-1)



#-----------------------------------------------------


if(experiment_no=='2'):


	print('----Creating the decision tree----')
	examples = list()
	for nn in range(1000):
		examples.append(nn)

	attributes=list()
	for pp in range(1,5001):
		attributes.append(pp)

	root = ID3(examples,matrix,attributes)

	def cal(test_row,root):
		if root.left==None and root.right==None:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1	

	sum2=0
	count=0
	for item in matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==matrix[count][0]:
			sum2=sum2+1
		count=count+1			

	print('Accuracy of decision tree is: ')
	print(sum/10)
	print('Accuracy on training set:')
	print(sum2/10)
	print('Height of the above tree is ',height(root))
	print('Number of leaves = ',LeafCount(root))
	print('Total nodes = ',NodeCount(root))
	print('\n')
	print('================================================')

	print('\n----Doing Early Stopping with height = 90----')

	def cal(test_row,root):
		if (root.left==None and root.right==None )or root.height==92:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1	


	sum2=0
	count=0
	for item in matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==matrix[count][0]:
			sum2=sum2+1
		count=count+1	
			
	print('Accuracy on training with early stopping of height 90: ')
	print(sum2/10)
	print('Accuracy on testing with early stopping of height 90: ')
	print(sum/10)
	print('Number of leaves = ',LeafCount(root,90))
	print('Total nodes = ',NodeCount(root,90))
	print('\n')
	print('================================================')




	print('\n----Doing Early Stopping with height = 80----')


	def cal(test_row,root):
		if (root.left==None and root.right==None )or root.height==80:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1	

	sum2=0
	count=0
	for item in matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==matrix[count][0]:
			sum2=sum2+1
		count=count+1	
			

	print('Accuracy on training with early stopping of height 80: ')
	print(sum2/10)
	print('Accuracy on testing with early stopping of height 80: ')
	print(sum/10)
	print('Number of leaves = ',LeafCount(root,80))
	print('Total nodes = ',NodeCount(root,80))
	print('\n')
	print('================================================')


	print('\n----Doing Early Stopping with height = 70----')


	def cal(test_row,root):
		if (root.left==None and root.right==None )or root.height==70:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1	

	sum2=0
	count=0
	for item in matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==matrix[count][0]:
			sum2=sum2+1
		count=count+1	
			

	print('Accuracy on training with early stopping of height 70: ')
	print(sum2/10)
	print('Accuracy on testing with early stopping of height 70: ')
	print(sum/10)
	print('Number of leaves = ',LeafCount(root,70))
	print('Total nodes = ',NodeCount(root,70))
	print('\n')
	print('================================================')

	print('\n----Doing Early Stopping with height = 50----')


	def cal(test_row,root):
		if (root.left==None and root.right==None )or root.height==50:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1	

	sum2=0
	count=0
	for item in matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==matrix[count][0]:
			sum2=sum2+1
		count=count+1	
			

	print('Accuracy on training with early stopping of height 50: ')
	print(sum2/10)
	print('Accuracy on testing with early stopping of height 50: ')
	print(sum/10)
	print('Number of leaves = ',LeafCount(root,50))
	print('Total nodes = ',NodeCount(root,50))
	print('\n')
	print('================================================')

	print('\n----Doing Early Stopping with height = 30----')


	def cal(test_row,root):
		if (root.left==None and root.right==None )or root.height==30:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1	

	sum2=0
	count=0
	for item in matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==matrix[count][0]:
			sum2=sum2+1
		count=count+1	
			

	print('Accuracy on training with early stopping of height 30: ')
	print(sum2/10)
	print('Accuracy on testing with early stopping of height 30: ')
	print(sum/10)
	print('Number of leaves = ',LeafCount(root,30))
	print('Total nodes = ',NodeCount(root,30))
	print('\n')
	print('================================================')


	print('\n----Doing Early Stopping with height = 10----')


	def cal(test_row,root):
		if (root.left==None and root.right==None )or root.height==10:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1	

	sum2=0
	count=0
	for item in matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==matrix[count][0]:
			sum2=sum2+1
		count=count+1	
			

	print('Accuracy on training with early stopping of height 10: ')
	print(sum2/10)
	print('Accuracy on testing with early stopping of height 10: ')
	print(sum/10)
	print('Number of leaves = ',LeafCount(root,10))
	print('Total nodes = ',NodeCount(root,10))
	print('\n')
	print('================================================')

	split=list()
	for i in range(5000):
		split.append(0)
	def inorderTraversal(root):
		if root:
			inorderTraversal(root.left) 
			c=root.feature
			split[c]=split[c]+1
			inorderTraversal(root.right)
		else:
			return
	inorderTraversal(root)
	
	for it in range(5000):
		if split[it]!=0:
			print(it,':',split[it])


#------------------------------------
if(experiment_no=='3'):
	
	print('----Creating the decision tree----')
	examples = list()
	for nn in range(1000):
		examples.append(nn)

	attributes=list()
	for pp in range(1,5001):
		attributes.append(pp)

	root = ID3(examples,matrix,attributes)

	def cal(test_row,root):
		if root.left==None and root.right==None:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1		

	print('Accuracy of decision tree is: ')
	print(sum/10)




	print('----Adding 0.5% noise----')
	copy_mat = list()

	for item in matrix:
		copy_mat.append(item)

	random_indexes=list()

	total_indexes=list()

	for i in range(1000):
		total_indexes.append(i)

	count=0

	while count!=5:
		id = random.choice(total_indexes)
		if id not in random_indexes:
			random_indexes.append(id)
			count=count+1		
	
	for i in range(5):
		copy_mat[random_indexes[i]][0] = 0- copy_mat[random_indexes[i]][0]

	examples = list()
	for nn in range(1000):
		examples.append(nn)

	attributes=list()
	for pp in range(1,5001):
		attributes.append(pp)

	root = ID3(examples,copy_mat,attributes)


	def cal(test_row,root):
		if root.left==None and root.right==None:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1		

	print('Accuracy of decision tree with 0.5% noise is: ')
	print(sum/10)
	

	#------------
	print('----Adding 1% noise----')
	copy_mat2 = list()

	for item in matrix:
		copy_mat2.append(item)

	random_indexes2=list()

	total_indexes2=list()

	for i in range(1000):
		total_indexes2.append(i)

	count2=0

	while count2!=10:
		id = random.choice(total_indexes2)
		if id not in random_indexes2:
			random_indexes2.append(id)
			count2=count2+1		


	for i in range(10):
		copy_mat2[random_indexes2[i]][0] = 0- copy_mat2[random_indexes2[i]][0]


	examples = list()
	for nn in range(1000):
		examples.append(nn)

	attributes=list()
	for pp in range(1,5001):
		attributes.append(pp)

	root2 = ID3(examples,copy_mat2,attributes)
	

	def cal(test_row,root):
		if root.left==None and root.right==None:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root2)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1		

	print('Accuracy of decision tree with 1% noise is: ')
	print(sum/10)

	#---


	print('----Adding 5% noise----')
	copy_mat4 = list()

	for item in matrix:
		copy_mat4.append(item)

	random_indexes4=list()

	total_indexes4=list()

	for i in range(1000):
		total_indexes4.append(i)

	count4=0

	while count4!=50:
		id = random.choice(total_indexes4)
		if id not in random_indexes4:
			random_indexes4.append(id)
			count4=count4+1		


	for i in range(50):
		copy_mat4[random_indexes4[i]][0] = 0- copy_mat4[random_indexes4[i]][0]



	examples = list()
	for nn in range(1000):
		examples.append(nn)

	attributes=list()
	for pp in range(1,5001):
		attributes.append(pp)

	root4 = ID3(examples,copy_mat4,attributes)

	def cal(test_row,root):
		if root.left==None and root.right==None:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root4)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1		

	print('Accuracy of decision tree with 5% noise is: ')
	print(sum/10)


	#--
	print('----Adding 10% noise----')
	copy_mat3 = list()

	for item in matrix:
		copy_mat3.append(item)

	random_indexes3=list()

	total_indexes3=list()

	for i in range(1000):
		total_indexes3.append(i)

	count3=0

	while count3!=100:
		id = random.choice(total_indexes3)
		if id not in random_indexes3:
			random_indexes3.append(id)
			count3=count3+1		


	for i in range(100):
		copy_mat3[random_indexes3[i]][0] = 0- copy_mat3[random_indexes3[i]][0]


	examples = list()
	for nn in range(1000):
		examples.append(nn)

	attributes=list()
	for pp in range(1,5001):
		attributes.append(pp)

	root3 = ID3(examples,copy_mat3,attributes)



	def cal(test_row,root):
		if root.left==None and root.right==None:
			if root.pu>root.nu:
				return 1
			else:
				return -1	
		if(test_row[root.feature]==1):
			return cal(test_row,root.right)
		else:
			return cal(test_row,root.left)	

	sum=0
	count=0
	for item in test_matrix:
		out = cal(item,root3)
		#print(out,test_matrix[count][0])
		if out==test_matrix[count][0]:
			sum=sum+1
		count=count+1		

	print('Accuracy of decision tree with 10% noise is: ')
	print(sum/10)

#-----------------------------------------------
if(experiment_no=='4'):
	print('Prunning displayed error atlast moment. Hence Removed')

#--------------
if(experiment_no=='5'):
	result_mat=list()
	train_result_mat=list()
	random_features=list()
	for io in range(20):
		col=list()
		count=0
		while count!=2000:
			pick = random.choice(selected_features)
			col.append(pick)
			count=count+1
		random_features.append(col)	
	
	for io in range(20):
		print('Creating')
		fea = random_features[io]
		aise = list()
		for vv in range(2000):
			aise.append(vv)

		myfeadic = dict(zip(fea,aise))

		my_mat=list()
		for item in selected_instances:

			length = len(item)
			count=0
			col =list()
			for kk in range(1,2001):
				col.append(0)

			it_list = item.split(' ')
			for it in it_list[1:]:
				features = it.split(':')
				if features[0] in myfeadic:
					#print(features[0],' y')
					col[myfeadic[features[0]]] = 1

			my_mat.append(col)


		index=0
		for item in matrix:
			item.insert(0,label[index])
			index=index+1


		examples = list()
		for nn in range(1000):
			examples.append(nn)

		attributes=list()
		for pp in range(1,2001):
			attributes.append(pp)

		root = ID3(examples,matrix,attributes)


		def cal(test_row,root):
			if root.left==None and root.right==None:
				if root.pu>root.nu:
					return 1
				else:
					return -1	
			if(test_row[root.feature]==1):
				return cal(test_row,root.right)
			else:
				return cal(test_row,root.left)	

		sum=0
		count=0
		temp=list()
		for item in test_matrix:
			out = cal(item,root)
			temp.append(out)	
		result_mat.append(temp)

		temp2=list()
		for item in my_mat:
			ou = cal(item,root)
			temp2.append(ou)	
		train_result_mat.append(temp2)
				
	
	for mm in range(1,21):
		output_vec = list()	
		for pp in range(1000):
			pos_count=0
			neg_count=0
			for vv in range(mm):
				if(result_mat[vv][pp]==1):
					pos_count=pos_count+1
				else:
					neg_count=neg_count+1
			if(pos_count>=neg_count):
				output_vec.append(1)			
			else:
				output_vec.append(-1)	

	for mm in range(1,21):
		train_output_vec = list()	
		for pp in range(1000):
			pos_count=0
			neg_count=0
			for vv in range(mm):
				if(train_result_mat[vv][pp]==1):
					pos_count=pos_count+1
				else:
					neg_count=neg_count+1
			if(pos_count>=neg_count):
				train_output_vec.append(1)			
			else:
				train_output_vec.append(-1)	


		match=0
		train_match=0
		for kk in range(1000):
			if output_vec[kk]==test_matrix[kk][0]:
				match=match+1
			if train_output_vec[kk]==matrix[kk][0]:
				train_match=train_match+1

		print(mm ,'trees in random forest , train acc = ',train_match/10 , ' test acc=',match/10)












