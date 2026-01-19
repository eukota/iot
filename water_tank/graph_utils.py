SPARK_CHARS = u"▁▂▃▄▅▆▇█"


def sparkline(values):
    if not values:
        return ""
    min_val = min(values)
    max_val = max(values)
    if max_val == min_val:
        index = len(SPARK_CHARS) // 2
        return SPARK_CHARS[index] * len(values)

    scale = float(len(SPARK_CHARS) - 1) / (max_val - min_val)
    pieces = []
    for val in values:
        idx = int(round((val - min_val) * scale))
        if idx < 0:
            idx = 0
        if idx >= len(SPARK_CHARS):
            idx = len(SPARK_CHARS) - 1
        pieces.append(SPARK_CHARS[idx])
    return "".join(pieces)
