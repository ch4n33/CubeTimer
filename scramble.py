import random

class CubeState:
    def __init__(self, cube_type: str, scramble: list[str]) -> None:
        
        for i in scramble:
            match len(i):
                case 1:
                    if i.lower() not in ['u', 'r', 'f', 'd', 'l', 'b']:
                        raise ValueError('Invalid scramble')
                case 2:
                    if i[0].lower() not in ['u', 'r', 'f', 'd', 'l', 'b']:
                        raise ValueError('Invalid scramble')
                    if i[1] not in ['2', "'"]:
                        raise ValueError('Invalid scramble')
                case _:
                    raise ValueError('Invalid scramble')
            # find redundant scramble, not implemented
            
        self.cube_type = cube_type
        self.scramble = scramble
    
    def __str__(self) -> str:
        return ' '.join(self.scramble)


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
    
    def get(self, cube_type: int, length=None) -> CubeState:
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
                
        return CubeState(cube_type, scramble)