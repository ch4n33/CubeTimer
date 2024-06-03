import random
from .formula import Formula


class Scramble:
    def __init__(self) -> None:
        self.operation =    [
            [],
            [],
            ['U', 'R', 'F'],
            ['U', 'R', 'F', 'D', 'L', 'B'],
            ['U', 'R', 'F', 'D', 'L', 'B', 'u', 'r', 'f', 'd', 'l', 'b'],
            ['U', 'R', 'F', 'D', 'L', 'B', 'u', 'r', 'f', 'd', 'l', 'b']
            ]
        self._rotations = ['2', '', "'"]
        self.count = [0,0,15,25,40,60]
        self.x = ['r', 'l', 'R', 'L']
        self.y = ['u', 'd', 'U', 'D']
        self.z = ['f', 'b', 'F', 'B']
    
    def get(self, cube_type: int, length=None) -> Formula:
        scramble = []
        beforelist = []
        beforetype = None
        if length is None:
            length = self.count[cube_type]
        while len(scramble) < length:
            next = random.choice(self.operation[cube_type])
            if next in beforelist:
                continue
            else:
                if next in self.x:
                    if beforetype is self.x:
                        beforelist.append(next)
                    else:
                        beforelist = [next]
                        beforetype = self.x
                elif next in self.y:
                    if beforelist is self.y:
                        beforelist.append(next)
                    else:
                        beforelist = [next]
                        beforetype = self.y
                else :
                    if beforetype is self.z:
                        beforelist.append(next)
                    else:  
                        beforelist = [next]
                        beforetype = self.z
                
                
                scramble.append(next + random.choice(self._rotations))
                
        return Formula(cube_type, scramble)
