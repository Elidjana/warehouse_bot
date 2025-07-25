from django.shortcuts import render
from django.http import JsonResponse
from robot.logic.simulator import WarehouseSimulator

simulator = WarehouseSimulator()


def index(request):
    return render(request, 'robot/index.html')


def start_sim(request):
    color = request.GET.get("color")
    simulator.reset(color)
    return JsonResponse({"status": "started", "color": color})


def step(request):
    pos, state = simulator.step()
    return JsonResponse({"pos": pos, "state": state})
