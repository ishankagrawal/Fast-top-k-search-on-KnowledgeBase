#import sys
import pickle
import re

f_sameAs = open("yago-wd-sameAs.nt", encoding = "cp437")
f_facts = open("yago-wd-facts.nt", encoding = "cp437")
#f_sameAs = open("yago-wd-sameAs.nt", "r")
#f_facts = open("yago-wd-facts.nt", "r")

edge_list = []
byte_dict = {}
#sys.stdout = open("log.txt","w")
def getAttrib(link):
	return " ".join(link.split('/')[-1][:-1].split('_')).lower()
def getEdge(link):
	temp1 = link.split('/')[-1][:-1]
	temp2 = temp1[0].upper() + temp1[1:]
	return " ".join(re.findall('[A-Z][^A-Z]*',temp2)).lower()
print("Populating entity data in RAM from sameAs file")
entities_data = []
#ent_data_sorted = []
for i,line in enumerate(f_sameAs):
	if("wikidata.org" in line):
		l1 = getAttrib(line.split()[0])
		l2 = getAttrib(line.split()[2])#[36:-1]
		entities_data.append([l1,l2])
		#ent_data_sorted.append([l,i])
	if(i%1000000==0):
		print("processed: " + str(i+1))
		print("wikidata entries found: " + str(len(entities_data)))
	if(i > 5000000): # shortcut, delete this line for larger dataset
		break
#def sortfunc(e):
#	return e[0]
#ent_data_sorted.sort(key = sortfunc)
#print(entities_data)
#print(ent_data_sorted)
ent_data_dict = {entity[0]: i for i,entity in enumerate(entities_data)}
#print(ent_data_dict)


print("Populating adj list using facts file and entity data")

cur_byte = 0
edge_counter = 0
graph = [[] for _ in range(len(entities_data))]
k = 0
for j,line in enumerate(f_facts):
	try:
		l = line.split()
		l0 = getAttrib(l[0])#[36:-1]
		t0 = ent_data_dict[l0]
		l2 = getAttrib(l[2])#[36:-1]
		t2 = ent_data_dict[l2]
		l1 = getEdge(l[1])#[19:-1]
		edge_list.append(l1)
		graph[t0].append([t2,edge_counter])
		edge_counter+=1

	except KeyError:
		k = k+1
		#if(k%10000==1):
			#print("Keys not found: ",k)
			#print("Following data may be from previous entries")
			#print("From:",l0,t0)
			#print("To: ",l2,t2)
			#print("Link: ",l1,j)
	if(j%100000==0):

		print("Processed: ",j)
		print("Facts discarded: ",k)

print("Processed: ",j)
print("Facts discarded: ",k)
print("Processing complete, closing files")
f_sameAs.close()
f_facts.close()
print("Files closed, now dumping data")

f_entities_data = open("entities_data", "wb")
pickle.dump(entities_data,f_entities_data)
f_entities_data.close()

f_ent_data_dict = open("ent_data_dict", "wb")
pickle.dump(ent_data_dict,f_ent_data_dict)
f_ent_data_dict.close()

f_graph = open("graph", "wb")
pickle.dump(graph,f_graph)
f_graph.close()

edge_file = open("edge_file","wb")
pickle.dump(edge_list,edge_file)
f_byte_dict= open("byte_dict","wb")
print("creating offset")
pickle.dump(byte_dict,f_byte_dict)


print("Data dumped using pickle")

input("Press key to exit")

