import unittest
import starterpack

class TestPile(unittest.TestCase):
    def test_transfer(self):
        p1 = starterpack.Pile([1,2])
        p2 = starterpack.Pile([3,4])
        p1.transfer_to(p2, [2])
        self.assertEqual(set(p2.cards), set([2,3,4]))
        self.assertEqual(p1.cards, [1])

if __name__ == '__main__':
    unittest.main()