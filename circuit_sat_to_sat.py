import sys

input_file = sys.argv[1]
vertexes_match = {}
vertex_counter = 1
sat = []
input_vertexes = []


def add_vertex(v, is_input=False):
    global vertex_counter
    global vertexes_match
    if v in vertexes_match.keys():
        return vertexes_match[v]
    vertexes_match[v] = vertex_counter
    if is_input:
        input_vertexes.append(vertex_counter)
    vertex_counter += 1
    return vertexes_match[v]


def create_new_vertex():
    global vertex_counter
    vertex_counter += 1
    return vertex_counter - 1


def sat_add_and(g, h1, h2):
    sat.extend([[-g, h1], [-g, h2], [g, -h1, -h2]])


def sat_add_or(g, h1, h2):
    sat.extend([[g, -h1], [g, -h2], [-g, h1, h2]])


def sat_add_not(g, h):
    sat.extend([[g, h], [-g, -h]])


def sat_add_id(g, h):
    sat.extend([[g, -h], [-g, h]])


def parse_operation(line):
    gate, operation = line.replace(' ', '').split('=')
    g = add_vertex(gate)
    if operation.startswith('AND'):
        a, b = operation[4:-1].split(',')
        h1, h2 = add_vertex(a), add_vertex(b)
        sat_add_and(g, h1, h2)
    elif operation.startswith('OR'):
        a, b = operation[3:-1].split(',')
        h1, h2 = add_vertex(a), add_vertex(b)
        sat_add_or(g, h1, h2)
    elif operation.startswith('NOT'):
        a = operation[4:-1]
        h = add_vertex(a)
        sat_add_not(g, h)
    elif operation.startswith('NAND'):
        a, b = operation[5:-1].split(',')
        h1, h2 = add_vertex(a), add_vertex(b)
        g1 = create_new_vertex()
        sat_add_and(g1, h1, h2)
        sat_add_not(g, g1)
    elif operation.startswith('NOR'):
        a, b = operation[4:-1].split(',')
        h1, h2 = add_vertex(a), add_vertex(b)
        g1 = create_new_vertex()
        sat_add_or(g1, h1, h2)
        sat_add_not(g, g1)
    elif operation.startswith('NXOR'):
        a, b = operation[5:-1].split(',')
        h1, h2 = add_vertex(a), add_vertex(b)
        g1 = create_new_vertex()
        sat_add_and(g1, h1, h2)
        g2 = create_new_vertex()
        sat_add_not(g2, h1)
        g3 = create_new_vertex()
        sat_add_not(g3, h2)
        g4 = create_new_vertex()
        sat_add_and(g4, g2, g3)
        sat_add_or(g, g1, g4)
    elif operation.startswith('XOR'):
        a, b = operation[4:-1].split(',')
        h1, h2 = add_vertex(a), add_vertex(b)
        g1 = create_new_vertex()
        sat_add_not(g1, h1)
        g2 = create_new_vertex()
        sat_add_not(g2, h2)
        g3 = create_new_vertex()
        sat_add_and(g3, g1, h2)
        g4 = create_new_vertex()
        sat_add_and(g4, h1, g2)
        sat_add_or(g, g3, g4)
    elif operation.startswith('DFF') or operation.startswith('BUFF'):
        a = operation[4:-1]
        h = add_vertex(a)
        sat_add_id(g, h)


def parse_line(line):
    if line.isspace() or line == '':
        return
    if line.startswith('#'):
        return
    if line.startswith('INPUT('):
        add_vertex(line[6:-1], is_input=True)
        return
    if line.startswith('OUTPUT('):
        sat.append([add_vertex(line[7:-1])])
        return
    parse_operation(line)


def write_sat_in_file(output_file):
    f = open(output_file, "w")
    s = 'p cnf {0} {1}\n'
    f.write(s.format(max(abs(max(x, key=abs)) for x in sat), len(sat)))
    for clause in sat:
        f.write(' '.join(map(str, clause)) + ' 0\n')
    f.close()


with open(input_file, 'r') as f:
    for line in f:
        parse_line(line[:-1])

write_sat_in_file('formula.cnf')
print(max(input_vertexes) + 1)
