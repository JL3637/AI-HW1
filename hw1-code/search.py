# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Shang-Tse Chen (stchen@csie.ntu.edu.tw) on 03/03/2022

"""
This is the main entry point for HW1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)

import queue
import heapq
import time

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    q = queue.Queue()
    visited = set()
    bfspath = {}
    objs = maze.getObjectives()
    state = (maze.getStart(), tuple(objs))
    visited.add(state)
    q.put(state)
    while not q.empty():
        state = q.get()
        if state[1] == ():
            break
        c, r = state[0]
        for i in maze.getNeighbors(c, r):
            tmp_objs = list(state[1])
            if i in tmp_objs:
                tmp_objs.remove(i)
            s = (i, tuple(tmp_objs))
            if s not in visited:
                visited.add(s)
                q.put(s)
                bfspath[s] = state
    path = []
    while state != (maze.getStart(), tuple(objs)):
        path.append(state[0])
        state = bfspath[state]
    path.append(maze.getStart())
    path.reverse()
    print(maze.isValidPath(path))

    return path

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    state_queue = []
    heapq.heapify(state_queue)
    visited = set()
    obj = maze.getObjectives()[0]
    start = maze.getStart()
    a = (manhattan_distance(start, obj), 0, start)
    visited.add(start)
    heapq.heappush(state_queue, a)
    astarpath = {}
    while state_queue:
        state = heapq.heappop(state_queue)
        if state[2] == obj:
            break
        for i in maze.getNeighbors(state[2][0], state[2][1]):
            if i not in visited:
                visited.add(i)
                s = (manhattan_distance(i, obj) + state[1] + 1, state[1] + 1, i)
                heapq.heappush(state_queue, s)
                astarpath[s] = state
    path = []
    while state != (manhattan_distance(start, obj), 0, start):
        path.append(state[2])
        state = astarpath[state]
    path.append(start)
    path.reverse()

    return path

def heuristic_corner(a, b_list):
    tmp = b_list.copy()
    if len(tmp) == 0:
        return 0
    b_min = min(tmp, key=lambda b: manhattan_distance(a, b))
    tmp.remove(b_min)
    return manhattan_distance(a, b_min) + heuristic_corner(b_min, tmp)

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    state_queue = []
    heapq.heapify(state_queue)
    visited = set()
    objs = maze.getObjectives()
    start = maze.getStart()
    a = (heuristic_corner(start, objs), 0, start, tuple(objs))
    visited.add((a[2], a[3]))
    heapq.heappush(state_queue, a)
    astarpath = {}
    while state_queue:
        state = heapq.heappop(state_queue)
        if state[3] == ():
            break
        for i in maze.getNeighbors(state[2][0], state[2][1]):
            tmp_objs = list(state[3])
            if i in tmp_objs:
                tmp_objs.remove(i)
            s = (heuristic_corner(i, tmp_objs) + state[1] + 1, state[1] + 1, i, tuple(tmp_objs))
            if (s[2], s[3]) not in visited:
                visited.add((s[2], s[3]))
                heapq.heappush(state_queue, s)
                astarpath[s] = state
    path = []
    while state != (heuristic_corner(start, objs), 0, start, tuple(objs)):
        path.append(state[2])
        state = astarpath[state]
    path.append(start)
    path.reverse()
    # print(path)
    print(maze.isValidPath(path))

    return path

def heuristic_multi(a, b_list):
    if len(b_list) == 0:
        return 0
    b_min = min(b_list, key=lambda b: manhattan_distance(a, b))
    b_max = max(b_list, key=lambda b: manhattan_distance(b_min, b))
    return manhattan_distance(a, b_min) + manhattan_distance(b_min, b_max)


def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    state_queue = []
    heapq.heapify(state_queue)
    visited = set()
    objs = maze.getObjectives()
    start = maze.getStart()
    a = (heuristic_multi(start, objs), 0, start, tuple(objs))
    visited.add((a[2], a[3]))
    heapq.heappush(state_queue, a)
    astarpath = {}
    while state_queue:
        state = heapq.heappop(state_queue)
        if state[3] == ():
            break
        for i in maze.getNeighbors(state[2][0], state[2][1]):
            tmp_objs = list(state[3])
            if i in tmp_objs:
                tmp_objs.remove(i)
            s = (heuristic_multi(i, tmp_objs) + state[1] + 1, state[1] + 1, i, tuple(tmp_objs))
            if (s[2], s[3]) not in visited:
                visited.add((s[2], s[3]))
                heapq.heappush(state_queue, s)
                astarpath[s] = state
    path = []
    while state != (heuristic_multi(start, objs), 0, start, tuple(objs)):
        path.append(state[2])
        state = astarpath[state]
    path.append(start)
    path.reverse()
    # print(path)
    print(maze.isValidPath(path))

    return path

def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    objs = maze.getObjectives()
    objs_r = objs.copy()
    start = maze.getStart()
    cur = start
    path = [cur]
    while objs:
        neighbors = maze.getNeighbors(cur[0], cur[1])
        intersect = [i for i in neighbors if i in objs]
        if intersect:
            cur = intersect[0]
            path.append(cur)
            objs.remove(cur)
        else:
            closest_dot = min(objs, key=lambda x: manhattan_distance(cur, x))
            maze.setObjectives([closest_dot])
            maze.setStart(cur)
            sub_path = astar(maze)
            path += sub_path[1:]
            cur = sub_path[-1]
            objs.remove(cur)
    maze.setStart(start)
    maze.setObjectives(objs_r)
    print(maze.isValidPath(path))
    return path
