import unittest
import os
from tkinter import Tk
from main import delete_duplicates
import random
import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno

class TestDuplicateDeleterIntegration(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.root.withdraw()
        self.temp_folder = os.path.join(os.getcwd(), 'test_folder')
        os.makedirs(self.temp_folder, exist_ok=True)
        self.file_paths = [
            os.path.join(self.temp_folder, 'file1.txt'),
            os.path.join(self.temp_folder, 'file2.exe'),
            os.path.join(self.temp_folder, 'file3.txt'),
            os.path.join(self.temp_folder, 'file4.txt'),
        ]

        # Create files with some content
        for file_path in self.file_paths:
            with open(file_path, 'w') as f:
                if random.randint(0,1) == 1:
                    f.write('Some content')
                else:
                    continue

    def tearDown(self):
        for file_path in self.file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_folder)

    def test_duplicate_deletion(self):
        # Check if duplicate files are correctly deleted
        delete_duplicates(self.temp_folder)
        self.root.withdraw()
        self.assertEqual(len(os.listdir(self.temp_folder)), 3)  # One file is a duplicate
