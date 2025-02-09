from django.shortcuts import render
from django.http import HttpResponse
from collections import deque
import time

# 定义目标状态和移动方向
TARGET_4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
TARGET_5 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 0]
MOVES = [(-1, 0, "下"), (1, 0, "上"), (0, -1, "右"), (0, 1, "左")]

# 将一维索引转换为二维坐标
def index_to_position(index, size):
    return index // size, index % size

# 将二维坐标转换为一维索引
def position_to_index(x, y, size):
    return x * size + y

# 检查当前位置是否越界
def is_valid(x, y, size):
    return 0 <= x < size and 0 <= y < size

# BFS 寻找最短路径并记录每一步的数字和方向
def bfs(start_state, target_state, size, print_steps=False, max_time=10):
    start_time = time.time()
    start_tuple = tuple(start_state)
    queue = deque([(start_state, start_state.index(0), 0, [])])
    visited = set([start_tuple])

    while queue:
        if time.time() - start_time > max_time:
            return -1, []  # 超过最大处理时间，认为无解
        
        current_state, empty_pos, steps, move_history = queue.popleft()
        if current_state == target_state:
            return steps, move_history
        
        empty_x, empty_y = index_to_position(empty_pos, size)
        for dx, dy, direction in MOVES:
            new_x, new_y = empty_x + dx, empty_y + dy
            if is_valid(new_x, new_y, size):
                new_empty_pos = position_to_index(new_x, new_y, size)
                new_state = current_state[:]
                new_state[empty_pos], new_state[new_empty_pos] = new_state[new_empty_pos], new_state[empty_pos]
                new_state_tuple = tuple(new_state)
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    new_move_history = move_history + [(new_state[empty_pos], direction)]
                    queue.append((new_state, new_empty_pos, steps + 1, new_move_history))
    
    return -1, []   # 如果没有解，返回 -1 和空的移动历史

# 打印当前的拼图布局
def format_puzzle(state, size):
    return '<br>'.join([' '.join(map(str, state[i:i+size])) for i in range(0, len(state), size)])

# Django 视图函数
def solve_puzzle(request):
    if request.method == 'POST':
        try:
            initial_state = list(map(int, request.POST.get('initial_state').split()))
            puzzle_size = request.POST.get('puzzle_size')
            if puzzle_size is None:
                raise ValueError
            puzzle_size = int(puzzle_size)
            if puzzle_size == 4:
                target_state = TARGET_4
            elif puzzle_size == 5:
                target_state = TARGET_5
            else:
                raise ValueError
            if len(initial_state) != puzzle_size * puzzle_size or set(initial_state) != set(range(puzzle_size * puzzle_size)):
                raise ValueError
        except ValueError:
            return HttpResponse("<p>输入无效，请输入正确数量的数字（0-15或0-24），用空格分隔。</p>")
        
        print_each_step = 'print_each_step' in request.POST
        steps, move_history = bfs(initial_state, target_state, puzzle_size, print_steps=print_each_step)
        
        if steps != -1:
            response = f"""
                <p>解决方案的步数：{steps}</p>
                <p>初始状态：</p>
                <p>{format_puzzle(initial_state, puzzle_size)}</p>
                <p>最终状态：</p>
                <p>{format_puzzle(target_state, puzzle_size)}</p>
                <p>移动过程：</p>
            """
            current_state = initial_state[:]
            for i, (number, direction) in enumerate(move_history):
                if print_each_step:
                    current_state = move_number(current_state, number)
                    response += f"""
                        <p>步骤 {i + 1}: 移动数字 {number} {direction}</p>
                        <p>{format_puzzle(current_state, puzzle_size)}</p>
                    """
        else:
            response = "<p>无法解决该问题，可能是无解布局或处理时间过长。</p>"
        
        return HttpResponse(response)
    else:
        return render(request, 'funny_game/solve_puzzle.html')

# 根据数字移动更新当前布局
def move_number(state, number):
    empty_pos = state.index(0)
    number_pos = state.index(number)
    state[empty_pos], state[number_pos] = number, 0
    return state
