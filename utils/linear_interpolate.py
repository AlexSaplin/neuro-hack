def interpolate_events(event_list, duration: int):
    result = [0.] * duration
    event_list = [(0, 0)] + event_list + [(duration, 0)]
    for idx, x in enumerate(event_list):
        if x[0] == duration:
            break
        for i in range(x[0], event_list[idx + 1][0]):
            result[i] = x[1] + (event_list[idx + 1][1] - x[1]) / (event_list[idx + 1][0] - x[0]) * (i - x[0])
    return result
