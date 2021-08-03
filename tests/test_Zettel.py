import src.Zettel as Zettel
import unittest


class testZettel(unittest.TestCase):

    def test_extract_cases(self):
        test_string = """
        # bulia
        #test1 #üüüber
        
        ## Text
        
        uaeiu
        
        ## Quelle 
        
        ueai
        
        ## Links
        1324.md
        
        """

        extracted_tags = Zettel.extract_tags(test_string)
        self.assertIn("#test1", extracted_tags)
        self.assertIn("#üüüber", extracted_tags)
        self.assertEqual(len(extracted_tags), 2)

if __name__ == '__main__':
    unittest.main()


