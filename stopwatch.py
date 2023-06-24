import timeit

timers = {}

DEBUG = True

def start(name):
    if not DEBUG:
        return
    if name not in timers:
        timers[name] = {
            "started": 0,
            "total": 0,
            "running": False
        }

    assert not timers[name]["running"], "Stopwatch already started for: " + name

    timers[name]["running"] = True
    timers[name]["started"] = timeit.default_timer()

def stop(name):
    if not DEBUG:
        return
    assert name in timers, "Stopwatch does not exist: " + name
    assert timers[name]["running"], "Stopwatch not started for: " + name

    timers[name]["running"] = False
    timers[name]["total"]+= (timeit.default_timer() - timers[name]["started"])

def show():
    if not DEBUG:
        return
    for name in timers.keys():
        print(f"{name:<30}{timers[name]['total']:9.1f} secs")