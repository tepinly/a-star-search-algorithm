import operator

tree = {}
coords = {}
costs = {}
xMin = 0
yMin = 0

# Generate the map
def map(x, y):
    val = 0
    for i in range(x):
        for j in range(y):
            coords.update({str(val): [i, j]})
            val += 1
    createTree(x, y)
    draw(x, y)
    addCosts()

# Create the costs, it's a aconstant value but too lazy to hardcode it
def addCosts(obstacles=[]):
    for k, i in coords.items():
        costs.update({k: 1})

# Draw the map
def draw(x, y, path = []):
    print('\n ', end = '')
    for j in range(y):
        for i in range(x):
            print('-' if keyOfValue(i, j) in path else keyOfValue(i, j), end = '  ')
        print('\n\n ', end = '')

# Connect all neighboring nodes to current one
def connect(x, y):
    neighbors = []
    if keyOfValue(x+1, y+1): neighbors.append(keyOfValue(x+1, y+1))
    if keyOfValue(x+1, y): neighbors.append(keyOfValue(x+1, y))
    if keyOfValue(x, y+1): neighbors.append(keyOfValue(x, y+1))
    if keyOfValue(x-1, y-1): neighbors.append(keyOfValue(x-1, y-1))
    if keyOfValue(x-1, y): neighbors.append(keyOfValue(x-1, y))
    if keyOfValue(x, y-1): neighbors.append(keyOfValue(x, y-1))
    if keyOfValue(x+1, y-1): neighbors.append(keyOfValue(x+1, y-1))
    if keyOfValue(x-1, y+1): neighbors.append(keyOfValue(x-1, y+1))
    return neighbors

# Create the node connection tree
def createTree(x , y):
    for i in range(x):
        for j in range(y):
            temp = connect(i, j)
            tree.update({keyOfValue(i, j): temp})

# Get the key of the coordinate value
def keyOfValue(x, y):
    try:
        list(coords.keys())[list(coords.values()).index([x, y])]
    except:
        return False
    else:
        return list(coords.keys())[list(coords.values()).index([x, y])]

# Check if the value will be of a didagonal node
def isDiagonal(node, explored, c):
    if c < 3 and explored[-1] != (keyOfValue(xMax, yMax) or keyOfValue(xMax, yMin) or keyOfValue(xMin, yMax) or keyOfValue(xMin, yMin)): return True
    if explored[-1] == keyOfValue(xMax, yMax) and keyOfValue(xMax-1, yMax-1) \
    or explored[-1] == keyOfValue(xMax-1, yMax-1) and node == keyOfValue(xMax, yMax) \
    or explored[-1] == keyOfValue(xMin, yMin) and node == keyOfValue(xMin+1, yMin+1) \
    or explored[-1] == keyOfValue(xMin+1, yMin+1) and node == keyOfValue(xMin, yMin) \
    or explored[-1] == keyOfValue(xMin, yMax) and node == keyOfValue(xMin+1, yMax-1) \
    or explored[-1] == keyOfValue(xMin+1, yMax-1) and node == keyOfValue(xMin, yMax) \
    or explored[-1] == keyOfValue(xMax, yMin) and node == keyOfValue(xMax-1, yMin+1) \
    or explored[-1] == keyOfValue(xMax-1, yMin+1) and node == keyOfValue(xMin, yMax): return True
    return False

# Get the value of key
def getVal(node, explored, target):
    if explored == []: return 0
    
    x = costs[node]
    for i in explored:
        x += costs[i]

    c = 0
    for i in tree[node]:
        for j in tree[explored[-1]]:
            if i == j: c += 1
    diagonal = isDiagonal(node, explored, c)

    dx = abs(coords[node][0] - coords[target][0])
    dy = abs(coords[node][1] - coords[target][1])
    return (x * (dx + dy)) + (((x/2 - x) * min(dx, dy)) if diagonal else 0)

    return x

# Sort queue depending on costs
def sortCost(neighbors, explored, target, h = False):
    temp = {}
    for i in range(len(neighbors)):
        for k, j in costs.items():
            if neighbors[i] == k:
                temp.update({k: getVal(k, explored, target)})

    return list(dict(sorted(temp.items(), key = operator.itemgetter(1))).keys())

# Form the path
def aStar(tree, start, target, explored = [], queue = []):
    if queue == []: queue = [start]
    
    while queue:
        node = queue.pop(0)
        explored.append(node)
        if node == target: return True

        neighbors = tree[node]
        neighbors = sortCost(neighbors, explored, target)
        final = []

        for i in neighbors:
            if i not in explored: 
                final.append(i)
                queue.append(i)

        for n in range(len(final)):
            if aStar(tree, final[n], target, explored, sortCost(queue, explored, target)): return explored
            aStar(tree, final[n], target, explored, sortCost(queue, explored, target))

xMax = int(input('\n Max X: '))
yMax = int(input(' Max Y: '))
map(xMax, yMax)

start = input('Starting block: ')
target = input(' Target block: ')
path = aStar(tree, start, target)
draw(xMax, yMax, path)
print('', ' -> '.join(path))