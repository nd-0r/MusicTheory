###############################################################################

# Do not alter, add, or delete import statements
from .ratio import Ratio
from .part import Part


class Score:

    def __init__(self, metadata={}, parts=[]):
        pass

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    def __iter__(self):
        pass

    def get_metadata(self, key, default=None):
        pass

    def set_metadata(self, key, value):
        pass

    def add_part(self, part):
        pass

    def part_ids(self):
        pass

    def num_parts(self):
        pass

    def get_part(self, pid):
        pass

    def print_all_repr(self):
        reprs = []
        indent = '  '
        # Add your code here, don't forget to return the reprs list!

    def print(self):
        pass
