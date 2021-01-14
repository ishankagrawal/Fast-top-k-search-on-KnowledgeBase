
import spacy 
nlp = spacy.load('en_core_web_sm')

"""

def get_gettokens(query):
	return nlp(query.lowers())
def get_head(tokens):
	for token in tokens:
		if token.dep_ == """



def parse_q(query):
	tokens = nlp(query.lower())
	m_edge = ""
	head = ""
	subjects = []
	edges = []
	cursubj = ""
	issub = False
	isCenter = False
	for i,token in enumerate(tokens):
		if(token.pos_=="NOUN" or token.pos_ == "PROPN"):
			cursubj+=token.text + " "
			issub = True
		else:
			if(issub):
				issub = False
				subjects.append(cursubj)
				cursubj = ""
		
	if(cursubj != ""):
		subjects.append(cursubj)
	

	verbs = 0
	for i,token in enumerate(tokens):
		if(token.pos_ == "VERB"):
			verbs += 1
	if(len(subjects) > verbs):
		if(len(subjects)==2):
			if(nlp(subjects[0])[0].pos_ == "NOUN"):
				head = subjects[1]

				edges.append(subjects[0])
				subjects.remove(subjects[0])

			else:
				head = subjects[0]

				edges.append(subjects[1])
				subjects.remove(subjects[1])


		else:
			isCenter = True
			for i,subj in enumerate(subjects):
				if(i%2==0):
					edges.append(subj)
					subjects.remove(subj)
	if(verbs>len(subjects)):
			curedge = ""
			isedge = False
			isCenter = True
			for token in tokens:
				if(token.pos_ not in ["PROPN", "NOUN", "PRON", "PUNCT"] and (tokens[0].text not in ["what" , "where" , "how" , "which" , "why" , "when" , "who", "whom"])):
					curedge+= token.text + " "
					isedge = True
				else:
					if(isedge):
						edges.append(curedge)
						isedge = False
						curedge = ""
			if(curedge != ""):
				edges.append(curedge)

	


	if(len(subjects)==verbs):
		if(len(subjects)==1):
			head = subjects[0]
			edge = ""
			for token in tokens:
				if(token.pos_ not in ["PROPN", "NOUN", "PRON", "PUNCT"] and (tokens.text  not in ["what" , "where" , "how" , "which" , "why" , "when" , "who" , "whom"])):
					edge+= token.text + " "
			
			edges.append(edge)
		else:
			curedge = ""
			isedge = False
			isCenter = True
			for token in tokens:
				if(token.pos_ not in ["PROPN", "NOUN", "PRON" , "PUNCT"] and (tokens[0].text not in ["what" , "where" , "how" , "which" , "why" , "when" , "who"])):
					curedge+= token.text + " "
					isedge = True
				else:
					if(isedge):
						edges.append(curedge)
						isedge = False
						curedge = ""
			if(curedge != ""):
				edges.append(curedge)
	if(len(edges)>len(subjects)):
		print("ed")
		subjects = subjects + [""]*(len(edges)-len(subjects))
	if(len(subjects)>len(edges)):
		print("ok")
		edges = edges + [""] * (len(subjects)-len(edges))
	if(len(edges)==1):
		m_edge = edges[0]

	print(head,subjects,edges,m_edge,isCenter)
	return (head,subjects,edges,m_edge,isCenter)


#print(parse_q(tokens))
			













 

#for token in tokens:
    
#    print(token.text, "-->", token.dep_, "-->", token.pos_)