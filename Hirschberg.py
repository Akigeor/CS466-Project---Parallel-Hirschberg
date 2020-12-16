def back_trace(s, t, path, delta):
    x, y = 0, 0
    score = 0
    s1, t1 = '', ''
    for i, j in path[1:]:
        if i == x:
            s1 += '-'
        else:
            s1 += s[i - 1]
        if j == y:
            t1 += '-'
        else:
            t1 += t[j - 1]
        x, y = i, j
        assert s1[-1] != '-' or t1[-1] != '-'
        score += delta[s1[-1]][t1[-1]]
    return score, s1 + '\n' + t1

def Hirschberg(_s, _t, _delta):
    global s
    global t
    global delta
    s = _s
    t = _t
    delta = _delta
    result = []
    _Hirschberg(0, 0, len(s), len(t), result)
    return back_trace(s, t, result, delta)

def _Hirschberg(x1, y1, x2, y2, result):
    global s
    global t
    global delta
    if x2 == x1:
        for i in range(y1, y2 + 1):
            result.append((x1, i))
        return
    if y2 == y1:
        for i in range(x1, x2 + 1):
            result.append((i, y1))
        return

    m = y2 - y1 + 1
    mid = (x1 + x2) // 2

    f = [0]
    for i in range(y1 + 1, y2 + 1):
        f.append(f[-1] + delta['-'][t[i - 1]])
    for i in range(x1 + 1, mid + 1):
        _f = [f[j] + delta[s[i - 1]]['-'] for j in range(m)]
        for j in range(1, m):
            c1 = s[i - 1]
            c2 = t[y1 + j - 1]
            _f[j] = max(_f[j], f[j - 1] + delta[c1][c2])
            _f[j] = max(_f[j], _f[j - 1] + delta['-'][c2])
        f, _f = _f, f

    g = [0]
    for i in range(y2 - 1, y1 - 1, -1):
        g.append(g[-1] + delta['-'][t[i]])
    g = g[::-1]
    for i in range(x2 - 1, mid - 1, -1):
        _g = [g[j] + delta[s[i]]['-'] for j in range(m)]
        for j in range(m - 2, -1, -1):
            c1 = s[i]
            c2 = t[y1 + j]
            _g[j] = max(_g[j], g[j + 1] + delta[c1][c2])
            _g[j] = max(_g[j], _g[j + 1] + delta['-'][c2])
        g, _g = _g, g

    best = None
    best_sum = None
    for i in range(m):
        if best_sum is None or best_sum < f[i] + g[i]:
            best_sum = f[i] + g[i]
            best = i
    # print(mid, best)
    _Hirschberg(x1, y1, mid, best + y1, result)
    if best < m - 1 and g[best] == g[best + 1] + delta['-'][t[best]]:
        x3 = mid
        y3 = best + 1
    elif g[best] == _g[best] + delta[s[mid]]['-']:
        x3 = mid + 1
        y3 = best
    else:
        x3 = mid + 1
        y3 = best + 1
    y3 += y1
    _Hirschberg(x3, y3, x2, y2, result)
    return best_sum