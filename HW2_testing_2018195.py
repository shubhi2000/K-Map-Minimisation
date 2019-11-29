# Shubhi Singhal
# 2018195
# Section- A
# Group- 3

import unittest
from HW2_2018195 import minFunc



class testpoint(unittest.TestCase):
	def test_minFunc(self):
		self.assertEqual(minFunc(3,"(0,1,2,5,6,7) d -"),"Simplified expression: w'y' + wx + x'y")
		self.assertEqual(minFunc(4,"(0,1,2,3,4,5,6) d (7,8,9,10,11,12,13,14,15)"),"Simplified expression: 1")
		self.assertEqual(minFunc(4,"(4,8,10,11,12,15) d (9,14)"),"Simplified expression: wx' + wy + xy'z'")
		self.assertEqual(minFunc(4,"(2,4,5,6,10) d (12,13,14,15)"),"Simplified expression: xy' + yz'")
		self.assertEqual(minFunc(4,"(1,3,10) d (0,2,8,12)"),"Simplified expression: w'x' + x'z'")
		
                
if __name__=='__main__':
	unittest.main()
