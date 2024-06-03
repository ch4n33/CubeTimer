from cubetimer.cube import Cube, formula_from_stirng

if __name__ == '__main__':
    cube = Cube(4)
    # cube.show()
    cube.attempt_formula(formula_from_stirng(3, "l b d"))
    cube.show()
    while(True):
        try:
            i = input()
            if i == 'q':
                break
            cube.attempt_formula(formula_from_stirng(3, i))
            cube.show()
        except ValueError as e:
            print(e)
            print('Invalid rotation')
            break