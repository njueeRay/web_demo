from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from collections import deque
import time
import heapq  # 使用优先队列优化A*算法

# 定义目标状态和移动方向
def get_target_state(size):
    return list(range(1, size * size)) + [0]

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

# 计算曼哈顿距离启发式
def manhattan_distance(state, target, size):
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:  # 不计算空格的距离
            current_pos = index_to_position(i, size)
            target_pos = index_to_position(target.index(state[i]), size)
            distance += abs(current_pos[0] - target_pos[0]) + abs(current_pos[1] - target_pos[1])
    return distance

class PuzzleState:
    def __init__(self, f_score, g_score, state, empty_pos, move_history):
        self.f_score = f_score
        self.g_score = g_score
        self.state = state
        self.empty_pos = empty_pos
        self.move_history = move_history

    def __lt__(self, other):
        return self.f_score < other.f_score

# A* 搜索算法（使用优先队列优化）
def astar_search(start_state, target_state, size, print_steps=False, max_time=30):
    start_time = time.time()
    start_tuple = tuple(start_state)
    
    # 使用优先队列
    h_score = manhattan_distance(start_state, target_state, size)
    start_node = PuzzleState(h_score, 0, start_state, start_state.index(0), [])
    open_set = [start_node]
    heapq.heapify(open_set)
    closed_set = {start_tuple}
    
    while open_set:
        if time.time() - start_time > max_time:
            return -1, []  # 超时返回
            
        current = heapq.heappop(open_set)
        
        if current.state == target_state:
            return current.g_score, current.move_history
            
        empty_x, empty_y = index_to_position(current.empty_pos, size)
        
        # 尝试所有可能的移动
        for dx, dy, direction in MOVES:
            new_x, new_y = empty_x + dx, empty_y + dy
            if is_valid(new_x, new_y, size):
                new_empty_pos = position_to_index(new_x, new_y, size)
                new_state = current.state[:]
                new_state[current.empty_pos], new_state[new_empty_pos] = new_state[new_empty_pos], new_state[current.empty_pos]
                new_state_tuple = tuple(new_state)
                
                if new_state_tuple not in closed_set:
                    closed_set.add(new_state_tuple)
                    new_g_score = current.g_score + 1
                    new_h_score = manhattan_distance(new_state, target_state, size)
                    new_move_history = current.move_history + [(new_state[current.empty_pos], direction)]
                    
                    new_node = PuzzleState(
                        new_g_score + new_h_score,
                        new_g_score,
                        new_state,
                        new_empty_pos,
                        new_move_history
                    )
                    heapq.heappush(open_set, new_node)
    
    return -1, []  # 无解返回

# 打印当前的拼图布局
def format_puzzle(state, size):
    return '<br>'.join([' '.join(map(str, state[i:i+size])) for i in range(0, len(state), size)])

# Django 视图函数
def solve_puzzle(request):
    if request.method == 'POST':
        try:
            initial_state = list(map(int, request.POST.get('initial_state').split()))
            puzzle_size = int(request.POST.get('puzzle_size', 3))
            if puzzle_size not in [3, 4, 5]:
                raise ValueError("只支持3阶、4阶和5阶华容道")
            
            target_state = get_target_state(puzzle_size)
            
            if len(initial_state) != puzzle_size * puzzle_size:
                raise ValueError(f"{puzzle_size}阶华容道需要{puzzle_size * puzzle_size}个数字")
            
            if set(initial_state) != set(range(puzzle_size * puzzle_size)):
                raise ValueError("输入的数字必须是0到N-1的所有数字")
                
        except ValueError as e:
            return HttpResponse(f"<p>输入错误：{str(e)}</p>")
        
        print_each_step = request.POST.get('print_each_step') == 'on'
        
        # 为3阶设置更短的超时时间
        max_time = 10 if puzzle_size == 3 else 30
        steps, move_history = astar_search(initial_state, target_state, puzzle_size, 
                                         print_steps=print_each_step, max_time=max_time)
        
        if steps != -1:
            if print_each_step:
                # 返回所有步骤的数据，但前端只显示当前步骤
                all_steps = []
                current_state = initial_state[:]
                for i, (number, direction) in enumerate(move_history, 1):
                    empty_pos = current_state.index(0)
                    number_pos = current_state.index(number)
                    current_state[empty_pos], current_state[number_pos] = number, 0
                    step_data = {
                        'step': i,
                        'number': number,
                        'direction': direction,
                        'state': current_state[:]
                    }
                    all_steps.append(step_data)
                
                response = {
                    'total_steps': steps,
                    'initial_state': initial_state,
                    'target_state': target_state,
                    'size': puzzle_size,
                    'steps': all_steps
                }
                return JsonResponse(response)
            else:
                # 只返回步骤文字说明
                moves = [f"步骤 {i+1}: 移动数字 {num} {dir}" for i, (num, dir) in enumerate(move_history)]
                response = f"""
                    <p>解决方案的步数：{steps}</p>
                    <p>初始状态：</p>
                    <p>{format_puzzle(initial_state, puzzle_size)}</p>
                    <p>目标状态：</p>
                    <p>{format_puzzle(target_state, puzzle_size)}</p>
                    <p>移动过程：</p>
                    <p>{'<br>'.join(moves)}</p>
                """
                return HttpResponse(response)
        else:
            response = "<p>无法在指定时间内找到解决方案，请尝试其他布局。</p>"
            return HttpResponse(response)
        
    return render(request, 'funny_game/solve_puzzle.html')
