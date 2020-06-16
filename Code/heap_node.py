from functools import total_ordering

#Huffman coding is based on designing a Binary Character Code
#in which each character is represented by a unique binary string : codeword
#We then construct a binary tree
#We need the class HeapNode to construct the nodes of the tree.

@total_ordering
class HeapNode:
	def __init__(self, character, frequency):
		self.character = character
		self.frequency = frequency
		self.left = None
		self.right = None

	def __lt__(self, other):
		return self.frequency < other.frequency

	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.frequency == other.frequency
