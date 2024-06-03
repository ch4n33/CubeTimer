from .formula import Formula, formula_from_stirng

import matplotlib.pyplot as plt
import numpy as np


def rotation_parse(rotation:str) -> tuple[str, int]:
    if len(rotation) < 1 or len(rotation) > 2:
        raise ValueError(rotation, ' is Invalid rotation')
    
    rotlayer = 1 if rotation[0].isupper() else 2
    rotation = rotation.lower()
    if rotation[0] not in ['u', 'r', 'f', 'd', 'l', 'b']:
        raise ValueError(rotation, ' is Invalid rotation')
    
    if len(rotation) == 1:
        rotation += ' '
        
    if rotation[1] not in ['2', ' ', "'"]:
        raise ValueError(rotation, ' is Invalid rotation')
    
    if rotation[1] == '2':
        rotcount = 2
    elif rotation[1] == "'":
        rotcount = -1
    else:
        rotcount = 1
    
    return rotation[0], rotcount, rotlayer

class Piece:
    def __init__(self, x,y,z) -> None:
        if x not in range(0,7) or y not in range(0,7) or z not in range(0,7):
            raise ValueError('Invalid piece coloring')
        """
        x : axis of R, -L
        y: axis of U, -D
        z: axis of F, -B
        """
        self.x = x
        self.y = y
        self.z = z
    def rotation(self, rotation:str):
        rotface, rotcount, rotlayer = rotation_parse(rotation)
        
        if rotface == 'u':
            self._U(rotcount)
        elif rotface == 'r':
            self._R(rotcount)
        elif rotface == 'f':
            self._F(rotcount)
        elif rotface == 'd':
            self._D(rotcount)
        elif rotface == 'l':
            self._L(rotcount)
        elif rotface == 'b':
            self._B(rotcount)
        
    def _R(self, rotation:int):
        """
        rotation : -1, 1, 2, -2, etc.
        """
        if rotation % 2 == 0:
            return
        self.y, self.z = self.z, self.y
    def _L(self, rotation:int):
        return self._R(rotation)
    
    def _U(self, rotation:int):
        if rotation % 2 == 0:
            return
        self.x, self.z = self.z, self.x
    
    def _D(self, rotation:int):
        return self._U(rotation)
    
    def _F(self, rotation:int):
        if rotation % 2 == 0:
            return
        self.x, self.y = self.y, self.x
    def _B(self, rotation:int):
        return self._F(rotation)
        
        

class Cube:
    def __init__(self, cube_type:int, formula=None) -> None:
        """
        cube color :
        F : 0 : green
        R : 1 : red
        U : 2 : white
        B : 3 : blue
        L : 4 : orange
        D : 5 : yellow
        no color : 6, example, edge piece or center piece, inner piece
        self.cube[0][0][0] is front top right corner
        """
        if cube_type not in [2,3,4,5]:
            raise ValueError('Invalid cube type')
        if type(formula) is Formula and formula.cube_type != cube_type:
            raise ValueError('Invalid formula for cube type')
        
        self.cube_type = cube_type
        
        self.cube = [[[
            Piece( \
                1 if x == 0 else 4 if x == cube_type-1 else 6, \
                2 if y == 0 else 5 if y == cube_type-1 else 6, \
                0 if z == 0 else 3 if z == cube_type-1 else 6 \
            ) 
            for z in range(cube_type)]
            for y in range(cube_type)]
            for x in range(cube_type)]
        
        self.attempt_formula(formula)
    
    def attempt_formula(self, formula:Formula):
        if formula is None:
            return
        for rotation in formula:
            # print(rotation_parse(rotation))
            self.rotate_orientation(rotation)
            self.rotate_permutation(rotation)
    
    def rotate_orientation(self, rotation:str):
        def valid_piece(x,y,z, rotation:str) -> bool:
            rotface, rotcount, rotlayer = rotation_parse(rotation)
            if rotface == 'u' and y < rotlayer:
                return True
            if rotface == 'r' and x < rotlayer:
                return True
            if rotface == 'f' and z < rotlayer:
                return True
            if rotface == 'd' and y >= self.cube_type - rotlayer:
                return True
            if rotface == 'l' and x >= self.cube_type - rotlayer:
                return True
            if rotface == 'b' and z >= self.cube_type - rotlayer:
                return True
            return False
        for x in range(self.cube_type):
            for y in range(self.cube_type):
                for z in range(self.cube_type):
                    if valid_piece(x,y,z, rotation):
                        # print(x,y,z, rotation, self.cube[x][y][z].x, self.cube[x][y][z].y, self.cube[x][y][z].z)
                        self.cube[x][y][z].rotation(rotation)
                        
                        # print(x,y,z, rotation, self.cube[x][y][z].x, self.cube[x][y][z].y, self.cube[x][y][z].z)
                        # print('----------------')
                    
    def rotate_permutation(self, rotation:str):
        def normalize(rotface, rotcount):
            # dlb rotation is reversed rotation
            if rotface in ['d', 'l', 'b'] and rotcount != 2:
                return -rotcount
            return rotcount
        rotface, rotcount, rotlayer = rotation_parse(rotation)
        rotcount = normalize(rotface, rotcount)
        
        # print(rotface, rotcount, rotlayer)
        if rotface in ['u', 'd']:
            layers = [(x, y if rotface == 'u' else self.cube_type - 1 - y, z) for y in range(rotlayer) for x in range(self.cube_type) for z in range(self.cube_type)]
        elif rotface in ['l', 'r']:
            layers = [(x if rotface == 'r' else self.cube_type - 1 - x, y, z) for x in range(rotlayer) for y in range(self.cube_type) for z in range(self.cube_type)]
        elif rotface in ['f', 'b']:
            layers = [(x, y, z if rotface == 'f' else self.cube_type - 1 - z) for z in range(rotlayer) for x in range(self.cube_type) for y in range(self.cube_type)]
        
        # print(layers)
        new_positions = {}
        
        for x, y, z in layers:
            if rotface == 'u' or rotface == 'd':
                if rotcount == 2:
                    nx, nz = self.cube_type - 1 - x, self.cube_type - 1 - z
                else :
                    (nx, nz) = (self.cube_type - 1 - z, x) if rotcount > 0 else (z, self.cube_type - 1 - x)
                new_positions[(x, y, z)] = (nx, y, nz)
            elif rotface == 'l' or rotface == 'r':
                if rotcount == 2:
                    ny, nz = self.cube_type - 1 - y, self.cube_type - 1 - z
                else:
                    (ny, nz) = (z, self.cube_type - 1 - y) if rotcount > 0 else (self.cube_type - 1 - z, y)
                new_positions[(x, y, z)] = (x, ny, nz)
            elif rotface == 'f' or rotface == 'b':
                if rotcount == 2:
                    nx, ny = self.cube_type - 1 - x, self.cube_type - 1 - y
                else:
                    (nx, ny) = (y, self.cube_type - 1 - x) if rotcount > 0 else (self.cube_type - 1 - y, x)
                new_positions[(x, y, z)] = (nx, ny, z)
        
        temp_cube = [[[self.cube[x][y][z] for z in range(self.cube_type)] for y in range(self.cube_type)] for x in range(self.cube_type)]
        
        # print('new_positions', new_positions)
        for (x, y, z), (nx, ny, nz) in new_positions.items():
            self.cube[nx][ny][nz] = temp_cube[x][y][z]
                    
    
    
    
    def get_face(self, face:str):
        face_colors = {
            'U': 2,
            'F': 0,
            'R': 1,
            'B': 3,
            'L': 4,
            'D': 5
        }
        face = face.upper()
        if face not in face_colors:
            raise ValueError('Invalid face')
        
        face_color = face_colors[face]
        faceinfo = np.zeros((self.cube_type, self.cube_type), dtype=int)
        
        for x in range(self.cube_type):
            for y in range(self.cube_type):
                    faceinfo[y, x] = \
                        self.cube[self.cube_type-1-x][y][0].z if face == 'F' else \
                        self.cube[x][y][self.cube_type-1].z if face == 'B' else \
                        self.cube[self.cube_type-1-x][0][self.cube_type-1-y].y if face == 'U' else \
                        self.cube[self.cube_type-1-x][self.cube_type-1][y].y if face == 'D' else \
                        self.cube[0][y][x].x if face == 'R' else \
                        self.cube[self.cube_type-1][y][self.cube_type-1-x].x  # face == 'L'
        return faceinfo
    
    def plot(self, fig, ax):        
        # Cube face colors
        face_colors = {
            'U': 'white',
            'F': 'green',
            'R': 'red',
            'B': 'blue',
            'L': 'orange',
            'D': 'yellow',
            0 : 'green',
            1 : 'red',
            2 : 'white',
            3 : 'blue',
            4 : 'orange',
            5 : 'yellow',
            6 : 'darkgrey'
        }
        b = self.cube_type
        # Define the layout of the unfolded cube
        faces = [
            ('U', b, 2*b),
            ('L', 0, b), ('F', b, b), ('R', 2*b, b), ('B', 3*b, b),
            ('D', b, 0)
        ]
        
        # Draw the faces
        for face, col, row in faces:
            faceinfo = self.get_face(face)
            ax.text(col + b/2, row - b/2 + 1, face, fontsize=12, ha='center', va='center')
            for i in range(b):
                for j in range(b):
                    facecolor = face_colors[faceinfo[i,j]]
                    if facecolor == 'darkgrey':
                        print('dark grey found in ', i, j, face)
                    square = plt.Rectangle((col + j, row - i), 1, 1, edgecolor='black', facecolor=facecolor)
                    ax.add_patch(square)
                    # Add text to indicate the face
                    
        
        # Set the limits and aspect
        ax.set_xlim(0, 4*b)
        ax.set_ylim(-b, 3*b)
        
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        
        ax.set_aspect('equal')
        ax.axis('off')  # Hide the axes

    def show(self):
        fig, ax = plt.subplots(figsize=(8,8))
        
        self.plot(fig, ax)

        plt.show()

        