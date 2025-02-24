from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

def solve_puzzle(request):
    if request.method == 'GET':
        return render(request, 'funny_game/solve_puzzle.html')
    elif request.method == 'POST':
        initial_state = request.POST.get('initial_state')
        puzzle_size = int(request.POST.get('puzzle_size', 4))
        print_each_step = request.POST.get('print_each_step') == 'on'
        
        # 这里添加解题逻辑
        result = f"收到求解请求：\n初始状态：{initial_state}\n阶数：{puzzle_size}\n是否显示步骤：{print_each_step}"
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'result': result})
        return HttpResponse(result)
