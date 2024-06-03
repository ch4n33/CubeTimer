class Formula:
    def __init__(self, cube_type: str, formula: list[str]) -> None:
        
        for i in formula:
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
        self.formula = formula
    
    def __str__(self) -> str:
        return ' '.join(self.formula)
    
    def __iter__(self):
        return iter(self.formula)

def formula_from_stirng(cube_type: int, formula: str) -> Formula:
    return Formula(cube_type, formula.split())