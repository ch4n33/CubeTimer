import random
from formula import Formula


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
    
    def get(self, cube_type: int, length=None) -> Formula:
        scramble = []
        before = ''
        if length is None:
            length = self.count[cube_type]
        while len(scramble) < length:
            next = random.choice(self.operation[cube_type])
            if next.lower() == before:
                continue
            else:
                scramble.append(next + random.choice(self._rotations))
                before = next.lower()
                
        return Formula(cube_type, scramble)
