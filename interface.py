
from collections import Counter 
import glob, os, re 
from collections import defaultdict    
import nltk 
import sys    
import time 
import glob, os, operator
from math import log
from Tkinter import * 
from nltk.corpus import stopwords  
import pickle


def tokenizeWithStopword(text, lowercase=True): 
    text = text.lower() if lowercase else text 
    for match in re.finditer(r"\w+(\.?\w)*", text):  
        if not match in stopwords.words('english'): 
            yield match.group() 

class CosineIRSystem:
    """A very simple Information Retrieval System. The constructor 
    s = IRSystem() builds an empty system. Next, index several 
    documents with s.index_document(ID, text). Then ask queries 
    with s.query('term1', 'term2') to retrieve the top n matching 
    documents."""
    
    def __init__(self):
        "Initialize an IR Sytem."
        self.N = 0
        self.lengths = Counter()
        self.tdf = defaultdict(Counter)
        self.doc_ids = []
        self._all_set = False
        
    def __repr__(self):
        return '<IRSystem(b={self.b}, k1={self.k1}, N={self.N})>'.format(self=self)
        
    def index_document(self, doc_id, words):
        "Add a new unindexed document to the system."
        self.N += 1
        self.doc_ids.append(doc_id)
        for word in words:
            self.tdf[word][doc_id] += 1
            self.lengths[doc_id] += 1
        self._all_set = False
        
    def index_collection(self, filenames):
        "Index a collection of documents."
        for filename in filenames:
            self.index_document(os.path.basename(filename), 
                                tokenizeWithStopword(open(filename).read()))
    
    def _document_frequency(self):
        "Return the document frequency for each term in self.tdf."
        return {term: len(documents) for term, documents in self.tdf.items()}
    
    def score(self, doc_id, *query):
        "Score a document for a particular query using Okapi BM25."
        score = 0
        length = self.lengths[doc_id]
        for term in query:
            tf = self.tdf[term][doc_id]
            df = self.df.get(term, 0)
            idf = log((self.N - df + 0.5) / (df + 0.5))
            score += (idf * tf)
        return score
    
    def query(self, *query):
        """Query an indexed collection. Returns a ranked list of doc ID's sorted by
        the computation of Okapi BM25."""
        if not self._all_set:
            self.df = self._document_frequency()
            self.avg_len = sum(self.lengths.values()) / self.N
            self._all_set = True
            
        scores = {doc_id: self.score(doc_id, *query) for doc_id in self.doc_ids}
        return sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        
    
    def present(self, results):
        "Present the query results as a list."  
        results = results[0:10] 
        top10 = []
        for doc_id, score in results: 
            top10.append("%5.2f | %s" % (100 * score, doc_id))
            print("%5.2f | %s" % (100 * score, doc_id)) 
        return top10 
        global top10
            
    def present_results(self, *query):
        "Query the collection and present the results."
        return self.present(self.query(*query))




class OkapiIRSystem:
    """A very simple Information Retrieval System. The constructor 
    s = IRSystem() builds an empty system. Next, index several 
    documents with s.index_document(ID, text). Then ask queries 
    with s.query('term1', 'term2') to retrieve the top n matching 
    documents."""
    
    def __init__(self, b=0.75, k1=1.2):
        "Initialize an IR Sytem."
        self.N = 0
        self.lengths = Counter()
        self.tdf = defaultdict(Counter)
        self.doc_ids = []
        self.b = b
        self.k1 = k1
        self._all_set = False
        
    def __repr__(self):
        return '<IRSystem(b={self.b}, k1={self.k1}, N={self.N})>'.format(self=self)
        
    def index_document(self, doc_id, words):
        "Add a new unindexed document to the system."
        self.N += 1
        self.doc_ids.append(doc_id)
        for word in words:
            self.tdf[word][doc_id] += 1
            self.lengths[doc_id] += 1
        self._all_set = False
        
    def index_collection(self, filenames):
        "Index a collection of documents."
        for filename in filenames:
            self.index_document(os.path.basename(filename), 
                                tokenizeWithStopword(open(filename).read()))
    
    def _document_frequency(self):
        "Return the document frequency for each term in self.tdf."
        return {term: len(documents) for term, documents in self.tdf.items()}
    
    def score(self, doc_id, *query):
        "Score a document for a particular query using Okapi BM25."
        score = 0
        length = self.lengths[doc_id]
        for term in query:
            tf = self.tdf[term][doc_id]
            df = self.df.get(term, 0)
            idf = log((self.N - df + 0.5) / (df + 0.5))
            score += (idf * (tf * (self.k1 + 1)) / 
                          (tf + self.k1 * (1 - self.b + (self.b * length / self.avg_len))))
        return score
    
    def query(self, *query):
        """Query an indexed collection. Returns a ranked list of doc ID's sorted by
        the computation of Okapi BM25."""
        if not self._all_set:
            self.df = self._document_frequency()
            self.avg_len = sum(self.lengths.values()) / self.N
            self._all_set = True
            
        scores = {doc_id: self.score(doc_id, *query) for doc_id in self.doc_ids}
        return sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        
    
    def present(self, results):
        "Present the query results as a list."  
        results = results[0:10] 
        top10 = []
        for doc_id, score in results: 
            top10.append("%5.2f | %s" % (100 * score, doc_id))
            print("%5.2f | %s" % (100 * score, doc_id)) 
        return top10 
        global top10
            
    def present_results(self, *query):
        "Query the collection and present the results."
        return self.present(self.query(*query))





class IRapp(Frame): 
	
	def __init__(self, master): 
		Frame.__init__(self, master) 
		self.grid()  
		self.create_app()   
	
	
	def create_app(self):   

		self.sim = IntVar() 
		self.pos = IntVar()

		self.builder = Label(self, text = "Choose your indexing preferences") 
		self.builder.grid(row = 2, column = 0, columnspan = 3, sticky = W) 

		
		Radiobutton(self, text = "Cosine", variable = self.sim,  
		value = 1).grid(row = 3, column = 1, sticky = W) 


		 
		Radiobutton(self, text = "Okapi", variable = self.sim,  
		value = 2).grid(row = 4, column = 1, sticky = W) 
	

		
		Radiobutton(self, text = "With POS tagging", variable = 			self.pos, value = 1).grid(row = 5, column = 1, sticky = W) 


		
		Radiobutton(self, text = "Without POS", variable = self.pos,  
		value = 2).grid(row = 6, column = 1, sticky = W) 


		self.build_button = Button(self, text = "Build New Index",  
		command = self.indexing)
		self.build_button.grid(row = 3, column = 3, sticky = W) 

		self.save_button = Button(self, text = "Save Index", command = 			self.saving) 
 		self.save_button.grid(row = 4, column = 3, sticky = W)	 

		self.load_button = Button(self, text = "Load Existing Index",  
		command = self.loading)
		self.load_button.grid(row = 5, column = 3, sticky = W) 	

		self.instruction = Label(self, text = "Enter the query") 
		self.instruction.grid(row = 8, column = 0, sticky = W)  

		self.query = Entry(self) 
		self.query.grid(row = 8, column = 2, columnspan = 3, sticky = W)  

		self.submit_button = Button(self, text = "Submit", command = self.querying) 
		self.submit_button.grid(row=9, column = 1, sticky = W)  


		self.text = Text(self, width = 60, height = 30, wrap = WORD)   
		self.instruction2 = Label(self, text = "Displaying top 10 results") 
		self.instruction2.grid(row = 11, column = 1, columnspan = 2, sticky = W)  
		self.text.grid(row = 12, column = 1, columnspan = 2, sticky = W)  

		

	def indexing(self):  
		
		meas1 = self.sim.get() 
		toggle1 = self.pos.get() 
		
		if toggle1 == 1: 
			inputPath = 'data/CranfieldDocsPOS/*.txt'
		else: 
			inputPath = 'data/CranfieldDocsParse/*.txt'
		
		if meas1 == 1: 
			s = CosineIRSystem()    
			global s 
			start = time.clock()
			s.index_collection(glob.glob(inputPath))  
			end = time.clock() 
			runtime = (end-start)
			message2 = "Index construction complete - using cosine similarity" 
			message3 = "Index construction took " + str(runtime) + " seconds"
			
		elif meas1 == 2: 
			s = OkapiIRSystem()    
			global s 
			start = time.clock()
			s.index_collection(glob.glob(inputPath))  
			end = time.clock() 
			runtime = (end-start)
			message2 = "Index construction complete - using Okapi similarity" 
			message3 = "Index construction took " + str(runtime) + " seconds"  

		else: 
			message2 = "Needs user parameter selections" 
			message3 = "Please try again"

		def set_text_newline(s):	
			self.text.insert(INSERT, '\n' + s)
		
		self.text.delete(0.0, END)
		set_text_newline(message2) 
		set_text_newline(message3)

				

	def saving(self):   
		def set_text_newline(s):	
			self.text.insert(INSERT, '\n' + s)
		with open('saved_index.pkl', 'wb') as output: 
			pickle.dump(s, output, pickle.HIGHEST_PROTOCOL) 
		self.text.delete(0.0, END) 
		set_text_newline('The index was saved')

	def loading(self):   
		def set_text_newline(s):	
			self.text.insert(INSERT, '\n' + s)
		with open('saved_index.pkl', 'rb') as input: 
			s = pickle.load(input)   
		global s
		self.text.delete(0.0, END) 
		set_text_newline('An index was loaded, please query')

	def querying(self):  
		def set_text_newline(s):	
			self.text.insert(INSERT, '\n' + s)
		queryStr = self.query.get()     
		queryStr = str(queryStr)
		splitVar = re.split(" ", queryStr)
		prepQuery = tuple(splitVar)  
		s.present_results(*prepQuery) 
		self.text.delete(0.0, END)
		res = top10  
		for i in range(len(res)): 
			set_text_newline(res[i]) 







root = Tk() 
root.title("Retrieval System") 
root.geometry("750x550") 
app = IRapp(root) 

root.mainloop()
