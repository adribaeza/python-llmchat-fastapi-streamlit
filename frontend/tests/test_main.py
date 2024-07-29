'''
#####################  Frontend Unit Testing  #########################################
Author: Adrián Baeza Prieto
Github: @adribaeza
Python 3.10+
'''
import unittest
from unittest.mock import patch, MagicMock
from frontend.app.main import clear_chat

class TestClearChat(unittest.TestCase):
    @patch('frontend.app.main.st')
    def test_clear_chat(self, mock_st):
        # Create a fake session state with messages
        mock_st.session_state = MagicMock()
        mock_st.session_state.messages = ["Hello", "World"]
        
        # Ensure chat history is not empty before clearing
        self.assertNotEqual(len(mock_st.session_state.messages), 0)
        
        # Call the clear_chat function
        clear_chat()
        
        # Check if chat history is empty after clearing
        self.assertEqual(len(mock_st.session_state.messages), 0)

if __name__ == '__main__':
    unittest.main()