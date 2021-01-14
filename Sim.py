import nltk
from nltk.corpus import wordnet as wn
import math

def node_similarity(n1,n2,weights):
	bag1 = n1.lower().split()
	bag2 = n2.lower().split()
	res = 0

	
	for word1 in bag1:

		for word2 in bag2:
			if(word1 == word2):
				#print("matched" + " " + word1 + " " + word2)

				res+=((1/math.log(1+len(bag2)))*weights[0])


	
	for i in range(min(len(bag1),len(bag2))):
		if(bag1[i][0]==bag2[i][0]):
			res += weights[1]/(1+nltk.edit_distance(bag1[i],bag2[i]))
		if(len(bag1[i])>=3 and len(bag2[i])>=3):
			if(bag1[i][1:3]==bag2[i][1:3]):
				res += weights[2]
	
	return res
def edge_similarity(e1,e2,weights):
	res = 0.0
	res+=node_similarity(e1,e2,weights)
	bag1 = e1.lower().split()
	bag2 = e2.lower().split()

	for word1 in bag1:
		for word2 in bag2:
			w1 = wn.synsets(word1)
			w2 = wn.synsets(word2)
			if(len(w1)*len(w2)>0):
				x = w1[0].wup_similarity(w2[0])
				if(x is not None):
					res+=w1[0].wup_similarity(w2[0])*weights[3]
	return res