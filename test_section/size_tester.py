size_val = 440
resp_options = [{"len": 546}, {"len": 577}, {"len": 362}, {"len": 439}, {"len": 556}]


def closest_to_range(values, lower=(size_val - 0), upper=(size_val + 100)):
    closest_value = min(values, key=lambda x: min(abs(x - lower), abs(x - upper)))
    return closest_value


if resp_options:
    val_list = []
    for r in resp_options:
        val_list.append(r["len"])
    best_val = closest_to_range(values=val_list)
    print(best_val)
