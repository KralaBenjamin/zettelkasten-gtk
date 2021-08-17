import src.Zettel as Zettel
import unittest


class testZettel(unittest.TestCase):


    """
    Test, if there are normal tags
    """
    def test_extract_tags_positive_case(self):
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
    """
    Test for invalid tags
    """
    def test_extract_tags_negative_case(self):


        test_string = """
        # bulia
        #uae#auieaie ####uaeaiue # uaeuaieua
        
        ## Text
        
        uaeiu
        
        ## Quelle 
        
        ueai
        
        ## Links
        1324.md
        
        """

        extracted_tags = Zettel.extract_tags(test_string)
        self.assertEqual(len(extracted_tags), 0)

    """
    Test for a valid title
    """
    def test_extract_title_positive_case(self):

        test_string = """
# uaeuaejjjjjjjöööööyuae öäppeüäöp uaeuaeaueiuaei
#test1
        
## Text

uaeiu

### Quelle 

ueai

#### Links
1324.md
        
        """

        extracted_title = Zettel.extract_title(test_string)

        self.assertEqual(extracted_title, "uaeuaejjjjjjjöööööyuae öäppeüäöp uaeuaeaueiuaei")

    """
    Test for an empty title
    """
    def test_extract_title_empty_title(self):
        test_string = """
        # 
        #test1
                
        ## Text
        
        uaeiu
        
        ### Quelle 
        
        ueai
        
        #### Links
        1324.md
        
        """
        with self.assertRaises(Exception):
            extracted_title = Zettel.extract_title(test_string)


    """
    Test for double title. must throw exception
    """
    def test_extract_title_double_title(self):
        test_string = """
        # Titel1
        #test1
                
        # Titel2
        
        uaeiu
        
        ### Quelle 
        
        ueai
        
        #### Links
        1324.md
        
        """
        with self.assertRaises(Exception):
            extracted_title = Zettel.extract_title(test_string)

    """
    Test if no title is given.
    """
    def test_extract_title_no_title(self):
        test_string = """
        #test1
                
        ## Titel2
        
        uaeiu
        
        ### Quelle 
        
        ueai
        
        #### Links
        1324.md
        
        """
        with self.assertRaises(Exception):
            extracted_title = Zettel.extract_title(test_string)

    """
    Title must be in the beginning
    """
    def test_extract_title_no_first_title(self):
        test_string = """
        ## Text
        #test1
                
        # Titel2
        
        uaeiu
        
        ### Quelle 
        
        ueai
        
        #### Links
        1324.md
        
        """
        with self.assertRaises(Exception):
            extracted_title = Zettel.extract_title(test_string)

    """
    Test for working case
    """
    def test_extract_section_positive_case(self):
        test_string = """
        # Text
        #test1
                
        ## Tütel2
        1
        2
        üüüääää
        
        ## Tütel3
        
        #### Linksuaeiu
        1324.md
        
        """

        extracted_section = Zettel.extract_section(test_string, "Tütel2")
        self.assertIn("1", extracted_section)
        self.assertIn("2", extracted_section)
        self.assertIn("üüüääää", extracted_section)
        self.assertEqual(len(extracted_section), 3)

    """
    checks if parsing throws exception for double existing sections
    """
    def test_extract_section_double_sections(self):
        test_string = """
        # Text
        #test1
                
        ## Tütel2
        1
        2
        üüüääää
        
        ## Tütel2
        1324.md
        
        """

        with self.assertRaises(Exception):
            Zettel.extract_section(test_string, "Tütel2")

    """
    checks if parsing throws exception for not existing section
    """
    def test_extract_section_no_sections(self):
        test_string = """
        # Text
        #test1
                
        ## Tütel5
        1
        2
        üüüääää

        
        """

        with self.assertRaises(Exception):
            Zettel.extract_section(test_string, "Tütel2")


    def test_extract_section_no_content_section(self):
        test_string = """
        # Text
        #test1
                
        ## Tütel2
        ## Tütel3
        1324.md
        
        """

        extracted_section = Zettel.extract_section(test_string, "Tütel2")
        self.assertEqual(len(extracted_section), 0)

if __name__ == '__main__':
    unittest.main()


