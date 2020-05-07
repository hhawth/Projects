import math

class searchAlgo:

    def __init__(self, start, finish, maze):
        self.start = start
        self.finish = finish
        self.maze = maze

    def up(self, z):
        try:
            value = [z[0]-1, z[1]]
            return value
        except:
            value = [0,0]
            return value

    def down(self, z):
        try:
            value = [z[0]+1, z[1]]
            return value
        except:
            value = [0,0]
            return value

    def right(self, z):
        try:
            value = [z[0], z[1]+1]
            return value
        except:
            value = [0,0]
            return value

    def left(self, z):
        try:
            value = [z[0], z[1]-1]
            return value
        except:
            value = [0,0]
            return value

    def showMaze(self, path):
        copy_maze = self.maze
        for step in path:
            if self.maze[step[0]][step[1]] == "S" or self.maze[step[0]][step[1]] == "E":
                continue
            copy_maze[step[0]][step[1]] = "*"
        print("BFS path in maze:")
        for line in copy_maze:
            print(line)
        return


class breadth_first_search(searchAlgo):

    def __init__(self, start, finish, maze):
        searchAlgo.__init__(self, start, finish, maze)

    def search(self):
        visited = [self.start]
        queue = [self.start]
        previous_queue = 0
        while queue:
            s = queue.pop()
            a, b, c, d = self.up(s),self.right(s),self.down(s),self.left(s)
            directions = [a, b, c, d]
            for n in directions:
                if s in queue:
                    continue
                if n not in visited and self.maze[n[0]][n[1]] != "#":
                    visited.append(n)
                    stuff = s,n
                    queue.extend(stuff)
                    if n == self.finish:
                        print("BFS path:",queue)
                        return self.showMaze(queue)


class a_star(searchAlgo):

    def __init__(self, start, finish, maze):
        searchAlgo.__init__(self, start, finish, maze)

    def search(self):
        visited = [self.start]
        start_node = self.start
        end_node = self.finish
        queue = [self.start]

        def cal_distance_to_finish(current_node, end_node):
            # use Pythagorean Theorem to estiamte
            return math.sqrt(abs((current_node[0]+current_node[1])-(end_node[0]+end_node[1])))

        def takeSecond(elem):
            value = elem[1]
            return value

        priority_queue = []
        while queue:
            s = queue.pop()
            a, b, c, d = self.up(s),self.right(s),self.down(s),self.left(s)
            directions = [a, b, c, d]
            possible_paths = []
            for n in directions:
                if n not in visited and self.maze[n[0]][n[1]] != "#":
                    visited.append(n)
                    distance_from_start = abs((n[0]+n[1])-(start_node[0]+start_node[1]))
                    distance_from_end = cal_distance_to_finish(n, self.finish)
                    total_cost = distance_from_start + distance_from_end
                    node = [n, total_cost]
                    priority_queue.append(node)
                if n == self.finish:
                    print("a* path:",queue)
                    return self.showMaze(queue)
            priority_queue.sort(key=takeSecond, reverse=True)
            last_item_inpriority_queue = priority_queue.pop()
            add_queue = s, last_item_inpriority_queue[0]
            print(add_queue)
            queue.extend(add_queue)






def load ():
    mazemap = []
    def split(line):
        return [char for char in line]
    with open("maze.txt", "r") as f:
        for line in f:
            x = line.splitlines()
            mazemap.append(split(x[0]))
    return mazemap

def run():
    mazemap = load()
    start = [1,1]
    finish = [8,18]
    x = breadth_first_search(start, finish, mazemap)
    x.search()
    # x = a_star(start, finish, mazemap)
    # x.search()
