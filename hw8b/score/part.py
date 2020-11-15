###############################################################################

# Do not alter, add, or delete import statements
from .staff import Staff


class Part:

    def __init__(self, partid, name=None, shortname=None):
        self.partid = partid
        self.name = name
        self.shortname = shortname
        self.staffs = []
        self.score = None

    def __str__(self):
        return str(f'<{self.__class__}: P{self.partid} {hex(id(self))}>')

    def __repr__(self):
        return str(f'<{self.__class__}: P{self.partid}>')

    def __iter__(self):
        return iter(self.staffs)

    def add_staff(self, staff):
        if (not isinstance(staff, Staff)):
            raise TypeError(f'Invalid type: {type(staff)}')
        self.staffs.append(staff)

    def staff_ids(self):
        return len(staffs)

    def num_staffs(self):
        return [s.id for s in staffs]
