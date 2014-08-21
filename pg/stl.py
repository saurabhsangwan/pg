from .core import Mesh
import os
import struct

def parse_ascii_stl(data):
    if os.path.exists(data):
        with open(data, 'r') as fp:
            data = fp.read()
    rows = []
    for line in data.split('\n'):
        args = line.strip().lower().split()
        if 'vertex' in args or 'normal' in args:
            rows.append(tuple(map(float, args[-3:])))
    positions = []
    normals = []
    uvs = []
    for i in xrange(0, len(rows), 4):
        n, v1, v2, v3 = rows[i:i+4]
        positions.extend([v1, v2, v3])
        normals.extend([n, n, n])
    return positions, normals, uvs

def parse_binary_stl(data):
    if os.path.exists(data):
        with open(data, 'rb') as fp:
            data = fp.read()
    positions = []
    normals = []
    uvs = []
    count = struct.unpack('<I', data[80:84])[0]
    for i in xrange(count):
        index = 84 + i * 50
        face = struct.unpack('<ffffffffffff', data[index:index+48])
        nx, ny, nz, x1, y1, z1, x2, y2, z2, x3, y3, z3 = face
        positions.append((x1, y1, z1))
        positions.append((x2, y2, z2))
        positions.append((x3, y3, z3))
        normals.append((nx, ny, nz))
        normals.append((nx, ny, nz))
        normals.append((nx, ny, nz))
    return positions, normals, uvs

class STL(Mesh):
    def __init__(self, path):
        super(STL, self).__init__()
        try:
            positions, normals, uvs = parse_binary_stl(path)
        except Exception:
            positions, normals, uvs = parse_ascii_stl(path)
        self.positions = positions
        self.normals = normals
        self.uvs = uvs