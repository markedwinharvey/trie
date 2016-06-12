#!/usr/bin/env python
'''
trie.py generates a trie data structure (a forest of tries) based on words listed in wordlist.txt. 
After generating the data structure, a while-loop allows fast lookup for any listed word completions
based on user input. 
'''
from string import ascii_lowercase as s

#--------begin define classes--------#	
class trie:
	def __init__(self,root):
		self.root=node(root,parent=None,terminus=False,depth=0)
class node:
	def __init__(self,val,parent,terminus,depth):
		self.val=val			#--letter represented by this node
		self.parent=parent
		self.children=[]		
		self.terminus=terminus	#--True if word is complete
		self.depth=depth
#--------end define classes--------#

#--------begin generate forest--------#
def generate_forest():
	
	forest={}
	for i in range(len(s)):				#--generate forest of tries, one trie for each root letter (a-z)
		t=trie(s[i])
		forest[s[i]] = t
		
	with open('wordlist.txt','r') as f:	#--get wordlist
		wordlist = f.read().split()
	
	#----begin generate unique node paths----#
	for word in wordlist:
		curr_node_list = [forest[word[0]].root]
		
		for letter in range(1,len(word)):			
			
			terminus=False
			if letter == len(word)-1:
				terminus=True

			if not word[letter] in [x.val for x in curr_node_list[-1].children]:	
				#--if node not found, generate new node and append to children [] of parent and curr_node_list			
				n=node(word[letter],curr_node_list[-1],terminus,letter)
				curr_node_list[-1].children.append(n)
				curr_node_list.append(n)
			else:
				#--node exists; get node and append to curr_node_list
				for child in curr_node_list[-1].children:
					if child.val == word[letter]:
						curr_node_list.append(child)
						break
							
	return forest
	#----end generate unique node paths----#
#--------end generate forest--------#

#--------begin find resp--------#
def find_resp(resp,curr_node_list):
	matches=[]
	for i in range(1,len(resp)):
		for n in curr_node_list[-1].children:
			if resp[i] == n.val:		
				curr_node_list.append(n)
				if n.terminus and len(resp) == len(curr_node_list):
					matches.append(resp[:i+1])
				break
		else:	#no match for next letter found
			return 'No matches for: '+resp,curr_node_list,matches
	return None,curr_node_list,matches
#--------end find resp--------#
		
#--------begin main--------#	
def main():	
						
	forest = generate_forest()
	
	while 1:
		resp = raw_input('Enter input or ! to quit: ').lower()
		if resp == '!': break
		if any(x not in s for x in resp):
			print 'Enter valid characters a-z.';continue
		
		curr_node_list = [forest[resp[0]].root]
	
		msg,curr_node_list,matches = find_resp(resp,curr_node_list)
		if msg: print msg; continue							#no matches to resp
		
		def scan_trie(curr_node_list):
			for n in curr_node_list[-1].children:
				if n.terminus:								#add word if word-ending is found
					matches.append(resp+''.join([x.val for x in curr_node_list][len(resp):])+n.val)
				if n.children:
					curr_node_list.append(n)
					scan_trie(curr_node_list)
			curr_node_list.pop()
		
		scan_trie(curr_node_list)		
	
		print 'matches',matches
#--------end main--------#	

if __name__ == '__main__':
	main()