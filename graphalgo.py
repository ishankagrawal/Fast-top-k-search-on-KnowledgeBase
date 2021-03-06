
import pickle

import bisect
import heapq
import Sim 
import queryToGraph as qg
import json
import time

weights = [1.0,0.7,0.3,0.25]
class match_generator:
	def __init__(self,center,limit,qhead,qedges,qnodes):
		self.center = center
		self.sim_matrix = [[[0,0] for i in range(len(graph[center]))] for j in range(len(qnodes))]
		for i,node in enumerate(qnodes):
			for j,neighbour in enumerate(graph[center]):
				
				
				self.sim_matrix[i][j][0] = 1 + Sim.node_similarity(qhead,entities_data[self.center][0],weights) + Sim.node_similarity(node,entities_data[neighbour[0]][0],weights) + Sim.edge_similarity(qedges[i],edges[neighbour[1]],weights)
				self.sim_matrix[i][j][1] = j
				for row in self.sim_matrix:
					row.sort(key = lambda item: -item[0])
		pq = []
		heapq.heapify(pq)
		heapq.heappush(pq,wrapper_min([0,[],0]))
		for row in self.sim_matrix:
			nextpq = []
			heapq.heapify(nextpq)
			for i in pq:
				for col in row:

					heapq.heappush(nextpq,wrapper_min([self.center,i.m[1]+[col[1]],i.m[2] + col[0]]))
					if(len(nextpq)>limit):
						heapq.heappop(nextpq)
			pq = nextpq
		pq.sort(key = lambda item: -item.m[2])
		self.cur = 0
		self.p_q = pq
	def get_next(self):
		if(self.cur<len(self.p_q)):
			self.cur+=1
			return self.p_q[self.cur-1]
		else:
			return None






def node_similarity(n1,n2):
	bag1 = n1.split()
	bag2 = n2.split()
	res = 0
	
	for word1 in bag1:
		for word2 in bag2:
			if(word1 == word2):
				#print("matched" + " " + word1 + " " + word2)

				res+=1
	res = 0
	if(len(bag1)==len(bag2)):
		for i in range(len(bag1)):
			if(bag1[i][0]==bag2[i][0]):
				res+=0.2
	
	return res
"""def edge_similarity(e1,e2):
	bag1 = e1.split()
	bag2 = e2.split()
	res = 0.0
	for word1 in bag1:
		for word2 in bag2:
			w1 = wn.synsets(word1)
			w2 = wn.synsets(word2)
			if(len(w1)*len(w2)>0):
				x = w1[0].wup_similarity(w2[0])
				if(x is not None):
					res+=w1[0].wup_similarity(w2[0])
	return res"""
class wrapper:
	def __init__(self,match):
		self.m = match
	def __lt__(self,other):
		return self.m[2]>other.m[2]
class wrapper_min:
	def __init__(self,match):
		self.m = match
	def __lt__(self,other):
		return self.m[2]<other.m[2]


f = open("edge_file","rb")
b = open("graph","rb")

d = open("entities_data","rb")
e = open("byte_dict","rb")

print("opened")
graph = pickle.load(b)
b.close()
entities_data = pickle.load(d)
d.close()
byte_dict = pickle.load(e)
e.close()
edges = pickle.load(f)
f.close()
print("loaded")



'''for x in g:
	print(str(x) +" " + str(g[x]))
	i+=1
	if(i>100):
		break
	
	'''
'''iter = 0
for v in graph:
	for n in v:
		f.seek(n[1])
		
		print("v: " + entities[iter][0] + " vertex: " + entities[n[0]][0] + " wikidata:" + entities[n[0]][1] + " edge: " + str(f.read(byte_dict[n[1]])))

	if(iter>=800):
		break
	iter+=1
	'''
	
'''
for i in range(20):
		q = wn.synsets(input("Enter Query"))[0]
		res = ""
		sim = 0.0
		print("Total Entities :" + str(len(entities)) )
		for j,entity in enumerate(entities):

			temp = wn.synsets(entity[0])
			if(len(temp)>=1):
				comp = temp[0]
				
				
				x = q.wup_similarity(comp)
				if(x is None):
					x = 0.0

				if(x>sim):
					res = entity[0]
					sim = x
				if(j%10000==0):
					print(j," Entites processed")
					print(comp)

		print("Edges are")
		for ed in graph[ent_dict[res]]:
			f.seek(ed[1])
			print(str(f.read(byte_dict[ed[1]])) + " " + entities[ed[0]][0])
'''
# for i in range(20):
# 		q = input("Enter Query")
# 		res = ""
# 		sim = 0.0
# 		print("Total Entities :" + str(len(entities)) )
# 		for j,entity in enumerate(entities):
# 			if(node_sim(q,entity[0])>sim):
# 				res = entity[0]
# 				sim = node_sim(q,entity[0])
# 			if(j%10000==0):
# 				print(str(j) + " Queries Processed")

# 		print("Edges are")
# 		for ed in graph[int(ent_dict[res])]:
# 			f.seek(ed[1])
# 			print(str(f.read(byte_dict[ed[1]])) + " " + entities[ed[0]][0])
'''
qhead = str(input("Enter head of query: "))
qnodes = str(input("Enter nodes, comma-separated: ")).split(",")
qedges = input("Enter edges:").split(",")
qlen = len(qnodes) # This does not include head
'''

"""question = input("Enter The Query")
qhead,qnodes,qedges,m_edge,isCenter = qg.parse_q(question)
print ((qhead,qnodes,qedges,m_edge,isCenter))

k = int(input("Number of matches needed: "))
"""
k = 5
"""
isCenter = False
if(qhead=="what"):
	isCenter = True
	qhead = ""
for j,nd in enumerate(qnodes):
	if(nd=="what"):
		m_edge = qedges[j]
	qnodes[j] = ""
	"""




def get_topk_matches(qhead,qnodes,qedges):
		matches = []
		node_matches = []
		# Each entry in matches has a ent id (head), a list of ent ids, and a sim score
		# matches is sorted as per sim scores at the end of each round of algo

		# First half of algo
		# Find top match with each possible head
		print("Entites",len(entities_data))
		for i,entity in enumerate(entities_data):

			node_match_list = [] # id, sim pairs
			match_sim = Sim.node_similarity(entity[0],qhead,weights)


			if len(graph[i]) == 0:
				continue
			# Careful, len(node_match_list)	might now be smaller than len(entities_data)

			for j,qnode in enumerate(qnodes):
				node_match = None
				node_sim = 0

				for m,neighbour in enumerate(graph[i]):
					
					new_node_sim = 1 +  Sim.node_similarity(entities_data[neighbour[0]][0],qnodes[j],weights) #+ Sim.node_similarity(qedges[j],edges[neighbour[1]],weights) 

					if(new_node_sim > node_sim):
						node_sim = new_node_sim
						node_match = neighbour[0]

				node_match_list.append(node_match)
				match_sim += node_sim


			matches.append([i,node_match_list, match_sim])
			if(i%100000==0):
				print(i," nodes done!")



		print("sorting matches")
		matches = sorted(matches,key = lambda item: -item[2])

		final_matches = []
		matches = matches[:k]
		match_dict = {}
		match_heap = [wrapper(match) for match in matches]
		match_generators = [match_generator(match[0],k,qhead,qedges,qnodes) for match in matches]
		for j,match in enumerate(matches):
			match_dict[match[0]] = match_generators[j] 
		heapq.heapify(match_heap)

		match_iter = 0
		while(match_iter < k):
			best_match = heapq.heappop(match_heap)
			
			next_match = match_dict[best_match.m[0]].get_next()
			

			if(next_match is not None):
				
				final_matches.append(next_match)
				to_push = wrapper([match_dict[best_match.m[0]].center,[x for x in next_match.m[1]],next_match.m[2]])
				heapq.heappush(match_heap,to_push)
				match_iter +=1




		'''for match in matches:
			for node in match[1]:
				print(str(entities_data[node])+ " " + str(entities_data[match[0]]))
			print(match[2])'''

		print("Top-K matches are")

		for temp in range(len(final_matches)):
			final_matches[temp] = final_matches[temp].m
		final_matches.sort(key = lambda item: -item[2])
		print(final_matches)
		match_count = 1
		for x in range(k):
			print("Match: ",match_count)
			try:
				for y in final_matches[x][1]:
					
					#print(entities_data[final_matches[x][0]][0] + " " + edges[graph[final_matches[x][0]][y][1]] + " " +  entities_data[graph[final_matches[x][0]][y][0]][0])
					node_matches.append(entities_data[final_matches[x][0]][0] + " " + edges[graph[final_matches[x][0]][y][1]] + " " +  entities_data[graph[final_matches[x][0]][y][0]][0])
				match_count+=1
			except :
				print("Couldn't find more matches")
		return(final_matches,node_matches)



def get_topk_answers(m_edge,isCenter,final_matches):
	res = []
	for center in final_matches:
		if(isCenter):
			res.append([entities_data[center[0]][0],entities_data[center[0]][1]])
		else:
			
			top_score = Sim.edge_similarity(m_edge,edges[graph[center[0]][center[1][0]][1]],weights)
			top_edge = center[1][0]
			for ed in range(len(graph[center[0]])):
				if(Sim.edge_similarity(m_edge,edges[graph[center[0]][ed][1]],weights)>top_score):
					top_edge = ed
					top_score = Sim.edge_similarity(m_edge,edges[graph[center[0]][ed][1]],weights)
			#print(entities_data[graph[center[0]][top_edge][0]][0])
			res.append([entities_data[graph[center[0]][top_edge][0]][0],entities_data[graph[center[0]][top_edge][0]][1]])
	return res



ques_file = open("ques_test.txt","r")
ques_data = []
ques_data = json.load(ques_file)
"""for line in ques_file:
	data = line.split()
	ques_data.append(" ".join(data[3:]))
	print(ques_data[-1])"""
ques_file.close()
res_file = open("answers","wb")
time_file = open("query_times","wb")
match_file = open("matches","wb")
qiter = 0
original_ans = open("original_ans","wb")
for q in ques_data:
	if(qiter%1==0):
		ques = q
		print(q)
		#original_ans.write((str(q["targetValue"]) + "\n").encode("utf-8"))
		if(q[-1]=="False"):
			q[-1] = False
		else:
			q[-1] = True
		qhead,qnodes,qedges,m_edge,isCenter =   q #qg.parse_q(ques)

		s = time.time()
		final_matches,node_matches = get_topk_matches(qhead,qnodes,qedges)
		final_answers = get_topk_answers(m_edge,isCenter,final_matches)
		e = time.time()
		time_file.write(("Question: " + str(ques) + "\n \n").encode("utf-8"))
		time_file.write(("Time taken: " + str(e-s) + " seconds \n \n").encode("utf-8"))
		res_file.write(("Question: " + str(ques) + "\n" + "------------------" + "\n").encode("utf-8"))
		res_file.write(("Top Answers" +  "\n" + "------------------" + "\n").encode("utf-8"))
		for ans in final_answers:
			res_file.write((ans[0] + " ==> www.wikidata.org/wiki/" + ans[1] +  "\n").encode("utf-8"))
		res_file.write(("\n").encode("utf-8"))
		match_file.write(("\n" +    "Question: " + str(ques) + "\n" + "--------------" + '\n').encode("utf-8"))
		match_file.write(("Top Matches"  "\n" + "--------------" + '\n').encode("utf-8"))

		for m in node_matches:
			match_file.write((m + "\n").encode("utf-8"))
		match_file.write(("\n").encode("utf-8"))
	qiter+=1
res_file.close()
match_file.close()
time_file.close()









		



	



	

		







# Second half of algo


#while len(final_matches) < k and len(matches) > 0:
	# Note that less than k final_matches may be found in total

	# To be written





print("ok")

print("closed")
