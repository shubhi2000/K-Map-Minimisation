# CSE 101 - IP HW2
# K-Map Minimization 
# Name: Shubhi Singhal
# Roll Number: 2018195
# Section: A
# Group: 3
# Date: 19/10/18

def minFunc(numVar, stringIn):
	"""
        This python function takes function of maximum of 4 variables
        as input and gives the corresponding minimized function(s)
        as the output (minimized using the K-Map methodology),
        considering the case of Don’t Care conditions.

	Input is a string of the format (a0,a1,a2, ...,an) d(d0,d1, ...,dm)
	Output is a string representing the simplified Boolean Expression in
	SOP form.

        No need for checking of invalid inputs.
        
	Do not include any print statements in the function.
	"""
	n=numVar               										  # n is the number of variables
	f=stringIn													  # f is the function which is to be minimized

	if n==1:
		stringOut="Simplified expression: " + str(n)			
		exit()

	if f.find(")")>=0 and f.find(",")>=0:						  
		l1=list(map(int,f[1:f.find(")")].split(",")))             # l1 is a list of minterms of the function
	else:
		l1=[]                                                              

	if f.find ("(",f.find("d")) > 0 :                             # checking if there is any don't care term
		l2=list(map(int,f[f.find("(",f.find("d"))+1 : f.find(")",f.find("d"))].split(",")))   # l2 is a list of don't care terms

	else:                                                                                                                            
		l2=[]                                                     # if there is no don't care term, then make l2 an empty list

	l=l1+l2

	p=2**n
	for i in range(p):
		if i in l and i!=p-1:
			continue
		elif i in l and i==p-1:
			return "Simplified expression: 1"					# including the condition when simplified expression is 1
			
		else:
			break

	if l==[]:
		return "Simplified expression: 0"						# including the condition when simplified expression is 1
		

	l1binary=[]                                                  # l1binary is the list of minterms converted to binary form

	for c in l1:
		s=""
		for i in range(n):
			s=str(c%2)+s
			c=c//2
		l1binary.append(s)

	l2binary=[]													  # l2binary is the list of don't care terms converted to binary form

	for c in l2:
		s=""
		for i in range(n):
			s=str(c%2)+s
			c=c//2
		l2binary.append(s)

	l=l1binary + l2binary										  # l is the list of minterms and don't care terms

	def combine(l):												 # combine function combines the terms of the function 
		list=[]
		for i in range(len (l)):		
			for j in range(i+1,len(l)):
				count=0
				flag=0
				for k in range(n):
					if l[i][k]=="-" and l[j][k]!="-" or l[i][k]!="-" and l[j][k]=="-":
						flag+=1
				if flag==0:
					for k in range(n):
						if l[i][k]!=l[j][k]:
							count+=1

				if count == 1 :
					s=""
					for k in range(n):
						if l[i][k]!=l[j][k]:
							s+="-"
						else:
							s+=l[i][k]

					if s not in list:	
						list.append(s)

		return list

	def primeimp(p):											# primeimp function takes a list of implicants as argument and returns a list of implicants which are prime implicants  
		for i in range(len(p[-1])):
			p[-1][i]=p[-1][i]+"*"								
		for a in range (len(p)-1,0,-1):
			for i in range(len(p[a-1])):
				count=0
				for j in range(len(p[a])):
					for k in range(n):
						if p[a][j][k]!="-" and p[a-1][i][k]!="-" and p[a][j][k]!=p[a-1][i][k] or p[a-1][i][k]=="-" and p[a][j][k]!="-":
							count+=1
							break
				if count==len(p[a]):
					p[a-1][i]+="*"
		return p


	if n==2:
		p2=combine(l)
		p4=combine(p2)
		p=[l1binary,p2,p4]
		prime=primeimp(p)

	
	if n==3:
		p2=combine(l)
		p4=combine(p2)
		p8=combine(p4)
		p=[l1binary,p2,p4,p8]
		prime=primeimp(p)

	if n==4:
		p2=combine(l)
		p4=combine(p2)
		p8=combine(p4)
		p16=combine(p8)
		p=[l1binary,p2,p4,p8,p16]
		prime=primeimp(p)                                   # prime is a list of all implicants with an "*" with the elements which are prime implicants

	primeimplicants=[]                                      # primeimplicants is a list of all prime implicants 
	for i in range(len(prime)):
		for j in range (len(prime[i])):
			if "*" in prime[i][j]:
				primeimplicants.append(prime[i][j][0:n])


	epi=[]													# epi is the list of all essential prime implicants

	for i in l1binary:
		count=0
		e=[]
		for j in range(len(primeimplicants)):
			for k in range(n):
				if primeimplicants[j][k]=="-" or primeimplicants[j][k]!="-" and primeimplicants[j][k]==i[k]:
					if k<(n-1):
						continue
					else:
						count+=1
						e.append(primeimplicants[j])
				else:
					break

		if count==1:
			if e[0] not in epi:
				epi.append(e[0])


	remterms=[]                                                          # remterms is a list of terms which are not covered in essential prime implicants

	for i in l1binary:
		count=0
		for j in epi:
			for k in range(n):
				if j[k]=="-" or j[k]!="-" and j[k]==i[k]:
					continue
				else:
					count+=1
					break

		if count==len(epi):
			remterms.append(i)

	d={}                                                                 # d is the dictionary with remterms as the keys and the value of the key is the list of prime implicants associated with the key

	for i in remterms:
		d[i]=[]
		for j in primeimplicants:
			if j not in epi:
				for k in range(n):
					if j[k]=="-" or j[k]==i[k]:
						if k<(n-1):
							continue
						else:
							d[i].append(j)
					else:
						break

	for i in d:
		count=0
		for j in d[i]:
			for k in d.keys():
				if k!=i:
					for a in range(len(d[k])):
						if d[k][a][:n]==j:
							d[i][count]+="*"
			count+=1



	for i in d:
		max=0
		for j in range(len(d[i])):
			if d[i][j].count("*") > max:					# finding out the implicants which include maximum number of terms and are of maximum size
				max=d[i][j].count("*")						# and removing the rest terms from the dictionary
		for k in range(len(d[i])):
			if d[i][k].count("*")!=max:
				d[i][k]=""

		max=0
		for j in range(len(d[i])):
			if d[i][j].count("-") > max:
				max=d[i][j].count("-")
		for k in range(len(d[i])):
			if d[i][k].count("-")!=max:
				d[i][k]=""

		a=len(d[i])
		for j in range(a):
			if d[i][j]!="":
				d[i].append(d[i][j])

		d[i]=d[i][a:]

	func=[]													# func and func1 contain the list of terms that should be included in the minimised function other than the terms in epi

	for j in d:
		count=0
		for i in d[j]:
			if i[:n] in func:
				count+=1

		if count==0:
			func.append(d[j][0][:n])

	func1=[]

	for j in d:
		count=0
		for i in d[j]:
			if i[:n] in func1:
				count+=1

		if count==0:
			if len(d[j])>1:
				func1.append(d[j][1][:n])
			else:
				func1.append(d[j][0][:n])


	if len(func1)<len(func):
		f=func1
	else:
		f=func

	list1=[]

	def var(a,k):											 # var function takes a and k as the arguments
		if k==0:											 # a is the number or element that has to be converted to a variable
			v="w"											 # and k is its position which determines the variable that will be assigned to a
		elif k==1:
			v="x"
		elif k==2:
			v="y"
		else:
			v="z"
		if a=="0":
			return v+"'"
		elif a=="1":
			return v
		else:
			return ""

	f=epi+f 												# f now includes all the terms that need to be given in the answer

	for x in f:												# converting the terms of f to there variable form
		s=""
		for k in range(n):								
			s+=var(x[k],k)
		list1.append(s)

	list1.sort()											# sorting the terms of the expression in lexicographical order

	s=""
	p=len(list1)

	for i in range(p):
		if i==p-1:
			s+=list1[i]
		else:
			s+=list1[i]+" + "								# writing the list of terms in expression form in which are terms are separated by "+" sign

	stringOut="Simplified expression: " + s 				# stringOut is our simplified expression

	return stringOut

