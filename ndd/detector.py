# Detector class
#
# Written by Parker Moore (pjm336)
# http://www.parkermoore.de

import os
from pkgutil import get_data
from .ndindex import NearDuplicatesIndex

class Detector:
    def __init__(self, source, dest):
        self.source_dir = source
        self.dest_dir = dest
        self.check_files = [(d, self.source_dir) for d in os.listdir(source) if os.path.isfile(os.path.join(source, d)) and d[0] != "." ]
        self.files = [(d, self.dest_dir) for d in os.listdir(dest) if os.path.isfile(os.path.join(dest, d)) and d[0] != "." ]

        self.index = NearDuplicatesIndex()

        # Calculate near-duplicates index
        for file in self.files:
            filename = self.filename(file[0], file[1])
            doc = self.get_doc(filename)
            self.index.append(doc, filename)

    def get_doc(self, file):
        with open(file, encoding='utf-8') as f:
            doc = f.read().strip().strip(",.!|&-_()[]<>{}/\"'").strip().split(" ")
            return doc

    def get_source_files(self):
        return self.check_files

    # Public: returns the full relative path from the base dir of the project
    #         to the filename input
    #
    # filename - the filename relative to the test directory
    #
    # Returns full filename (including test directory)
    def filename(self, filename, source):
        return "%s/%s" % (source, filename)

    # Public: checks for near-duplicates in the set of files based on jaccard
    #         coefficient threshold of 0.5
    #
    # Returns a string containing formatted names and coefficients of 
    #   documents whose jaccard coefficient is greater than 0.5
    def check_for_duplicates(self):
        matches = []
        for indx1, f1 in enumerate(self.check_files):
            file1 = self.filename(f1[0], f1[1])
            doc = self.get_doc(file1)
            sketch = self.index.get_sketch(doc, file1)
            for indx2, f2 in enumerate(self.files[indx1+1:]):
                file2 = self.filename(f2[0], f2[1])
                jaccard = self.index.get_jaccard(sketch, file2)
                if jaccard > 0.5:
                    matches.append((f1, f2, jaccard))
        return matches
