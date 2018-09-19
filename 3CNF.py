###   Normalizing the database using BCNF  ########

import re

list1=[]

for i in range(3):   #### getting input 
	list1.append(raw_input())


  
def fundep(list1):    #### spliitng the list
	fd=list1[1].split(',')
	return fd
def candkey(list1):   #### getting the candidate keys
	candidate_key=list1[2].split(',')
	return candidate_key


def createnew(new_database):  #### breaking  into new database
	Attri=[]
	for i in range(0,len(new_database)):
		for j in range(0,2):
			for k in range(0,len(new_database[i][j])):
				if new_database[i][j][k] not in Attri:
					Attri.append(new_database[i][j][k])
	return Attri


def BCNF(fd,candidate_key):   #### BCNF function
	each_fd=[]
	new_database=[]
	old_database=[]
	Attributes=[]
	old_attributes=[]
	new_attributes=[]
	for i in range(0,len(fd)):
		each_fd=fd[i].split('->')  #### we have left hand side and right hand side rule 
		### check whether the left hand side is a candidate key
		if each_fd[0] not in candidate_key:
			### check for second rule whether it is trivial or not 
			if each_fd[1] not in each_fd[0]:
				temp_fd = each_fd[1]
				for att in each_fd[0] :
					temp_fd = re.sub(att , "" , temp_fd)
				counter_check = 0
				for att in range (len(temp_fd)) :
					counter = 0
					for ck in candidate_key :
						if re.search(att , ck , re.IGNORECASE) :
							counter = 1
							break
					if counter == 0 :
						### third rules not satisfied
						new_database.append([each_fd[0],each_fd[1]])
						new_attributes.append(fd[i])
						counter_check = 1
						break
				if counter_check == 0 :
					old_database.append([each_fd[0],each_fd[1]])
					old_attributes.append(fd[i])
				continue   ### go to the next functional dependency
			else :
				old_database.append([each_fd[0],each_fd[1]])
				old_attributes.append(fd[i])
				continue   ### go to the next functional dependency
		else:
			old_database.append([each_fd[0],each_fd[1]])
			old_attributes.append(fd[i])
		each_fd=[]
	print(old_database)
	Attributes.append([','.join(createnew(old_database)),','.join(old_attributes),','.join(candidate_key)])
	if len(new_database)!=0:
		Attributes.append([','.join(createnew(new_database)),','.join(new_attributes),new_database[0][0]])
	return Attributes




final_Attributes=[]

Attributes=BCNF(fundep(list1),candkey(list1))   #### getting the attributes
final_Attributes.append(Attributes[0])

while len(Attributes)!=1:
	list1=[]
	list1=Attributes[1]
	print(list1)
	Attributes=BCNF(fundep(list1),candkey(list1))
	final_Attributes.append(Attributes[0])


print(final_Attributes)















