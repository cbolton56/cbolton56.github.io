import json
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import glob as glob 
#import networkx as nx
import matplotlib.pyplot as plt 
from itertools import combinations 
import graph as gx

"""Function initializes a statistical language model from the Spacy 
Python library as nlp. It uses the en_core_web_sm as the standard 
English training set, also available through the Spacy library.

Params: None

Returns: 
    Returns the model object as nlp that has been trianed on en_core_web_sm. """
def init_model(): 
    nltk.download('stopwords')
    nlp = spacy.load('en_core_web_sm')
    return nlp 

"""Function processes text files in a directory. Extracts nodes and edges for the
social network by passing the infile as a string into the extract_edges_nodes function. 
It cleans the results of extract_edges_nodes further and returns the final lists of nodes
and edges as a tuple.

params: 
    nlp: (spacy object) takes the nlp model passed in from main

Returns: 
    Two lists of cleaned nodes and edges in a tuple object. """
def process_files(nlp):
    list_of_files = glob.glob('./*.txt')   
    #Lists for collecting nodes from each file
    edges = []
    nodes = []
    for file_name in list_of_files:
        #Open each file, find all names and store in two temporary lists
        f = open(file_name, 'r')
        infile = f.readlines()
        _edges, _nodes = extract_edges_nodes(infile, nlp)
        #Append temporary lists to the final lists of objects
        for i in _edges: 
            edges.append(i)
        for i in _nodes: 
            nodes.append(i)
    #clean edges and nodes lists
    edges, nodes = clean_edges_nodes(edges, nodes)
    return (nodes, edges)

""" Function processes text files in a directory. Extracts nodes and edges for the
social network by passing the infile as a string into the extract_edges_nodes function. 
It cleans the results of extract_edges_nodes further and returns the final lists of nodes
and edges as a tuple.

params: 
    file: (string object)  
    nlp: (spacy object)

Returns: 
    Two lists of nodes and edges in a tuple object. """
def extract_edges_nodes(file, nlp):
    #Cast the file object, which is a list of words in the file, to a string. 
    file_string =  str(file)
    file_string = file_string.replace(" al ", " al")
    file_string = file_string[:1000000]

    #The nlp model will return a doc object that tags parts of speech and other lingustic features of the document.
    #Note that doc is now of type spacy.tokens.doc.Doc
    doc = nlp(file_string)
    
    #Spacy's entity extraction features can be stored in a tuple. Spacy defines an entity as 
    #a "real world object", that is a person, country, product, or book title. This includes political groups.
    people_places_things = doc.ents

    # Subset to person type entities
    doc_people = filter(lambda x: x.label_ == 'PERSON', people_places_things)
    #In English it is customary to refer to an entity by last name after the first reference to the individual. 
    #Here we can filter instances where people are being mentioned for a second time by excluding mononymic references to people.
    doc_people = filter(lambda x: len(x.text.strip().split()) >= 2, doc_people)
    doc_people = list(map(lambda x: x.text.strip(), doc_people))
    co_occurring_names = list(doc_people)
    nodes = list(co_occurring_names)
    edges = list(combinations(co_occurring_names, 2))
    return (edges, nodes)


""" Function takes in edges and nodes and checks for extra stop words, excluding
    edges and nodes that include certain stopwords as substrings 

params: 
    edges: a list of tuples of edges
    nodes: a list of nodes

Returns: 
    Two lists of nodes and edges in a tuple object, cleaned. """
def clean_edges_nodes(edges, nodes):
    stop_words = ['st.', 'ave', 'north', 'south', 'east', 'west', 'lake', 'rio', 'river', 'nation']
    bad_nodes = []
    bad_edges = []
    #Lower all characters in the nodes list to prevent extra nodes
    nodes = [i.lower() for i in nodes]
    #Cast to a set to eliminate duplicate nodes
    nodes = set(nodes)
    #lower all characters in the list of tuples 
    edges = [(x.lower(), y.lower()) for x,y in edges]
    #filter out loops, ie edges from one vertex to itself
    edges = list(filter(lambda x: x[0] != x[1], edges))
    edges = list(set(edges))

    #We filter our nodes based on added stop words that the machine learning model may miss, namely
    #foreign names of geographical features and political organizations.
    for node in nodes: 
        for word in stop_words: 
            if node.find(word) != -1: 
                bad_nodes.append(node)
    #Filter nodes using set arithmetic.
    nodes = set(nodes) - set(bad_nodes)
    #Also filter edges
    for edge in edges: 
        for word in stop_words: 
            if edge[0].find(word) != -1 or edge[1].find(word) != -1: 
                bad_edges.append(edge)
    
    edges = set(edges) - set(bad_edges)
    return (edges, nodes)

""" Uses graph class to create a graph object .

params: 
    edges: a list of tuples of edges
    nodes: a list of nodess

Returns:  graph object """
def create_graph(nodes, edges):
    G = gx.Graph()
    G.add_nodes(nodes)
    G.add_edges(edges)    
    return G 

""" Writes a JSON file representing the graph object, 
    to be used in uploading interactive graph object to a
    web page.

params: 
    G: a graph object 

Returns:  None (writes to a JSON outfile in directory)"""
def create_json(G): 
    #Data is the main dictionary object to be converted to a JSON file
    data = {"nodes": [], "edges" : []}

    #Creates lists of all nodes and edges (edges are stored in tuples)
    nodes = list(G.nodes())
    edges = list(G.edges())

    #Node dictionary object to be added to the data object: 
    # {"id": the id of the node, "label", the name of the node, "x": the x coordinate
    # of the node on a plane, "y": the y coordinate of the node on a plane, "size": how
    # large the node is when displayed}
    #These individual node dictionaries will be appended to the node list in the data dict.
    for n in nodes:
        d = {"id": n, "label": n, "x": 0, "y": 0, "size": 3}
        data["nodes"].append(d)
    
    #Edge dictionary object to be added to the data object: 
    # {"id": the id of the node, "source": node the edge originates at, "target": end node of edge}
    #Note that the graph is not directed so source and target nodes are arbitrary.
    for idx, e in enumerate(edges):
        temp = {"id": idx, "source": e[0], "target": e[1]}
        data["edges"].append(temp)
    
    #Write dict object to JSON file. 
    with open('data.json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=1))

# Driver routine
def main():
    nlp = init_model()
    nodes, edges = process_files(nlp)
    G = create_graph(nodes, edges)
    create_json(G)

main()