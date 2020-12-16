import threading


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


def Hirschberg(_s, _t, _delta, num_workers=4):
    global s
    global t
    global delta
    global _num_workers
    s = _s
    t = _t
    delta = _delta
    _num_workers = num_workers
    backtracing = []
    dfs(0, 0, len(s), len(t), backtracing)
    return back_trace(s, t, backtracing, delta)


def dfs(x1, y1, x2, y2, result):
    global s
    global t
    global delta
    global _num_workers
    num_workers = _num_workers
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

    # Left part
    f = []
    df = [(0, 0)] # Single cell at (x1, y1)
    off_df = 0
    df2 = []
    off_df2 = 0
    lx, ly = x1, y1
    rx, ry = x1, y1
    if x1 == mid:
        f.append(df[-1])
    for sum_xy in range(x1 + y1 + 1, mid + y2 + 1):
        ly2 = min(ly + 1, y2)
        lx2 = sum_xy - ly2
        rx2 = min(rx + 1, mid)
        ry2 = sum_xy - rx2
        Len = rx2 - lx2 + 1
        _df = []
        off = off_df + (1 if ly + 1 > y2 else 0)
        def worker_f(LiRi, return_dict):
            # res = []
            for i in range(LiRi[0], LiRi[1]):
                tmp = (float('-inf'), -1)
                tmp = max(tmp, (df[off + i - off_df][0] + delta['-'][t[ly2 - i - 1]] if 0 <= off + i - off_df < len(df) and ly2 - i > y1 else float('-inf'), 0))  # from up
                tmp = max(tmp, (df[off + i - 1 - off_df][0] + delta[s[lx2 + i - 1]]['-'] if 0 <= off + i - 1 - off_df < len(df) and lx2 + i > x1 else float('-inf'), 1))  # from left
                tmp = max(tmp, (df2[off + i - 1 - off_df2][0] + delta[s[lx2 + i - 1]][t[ly2 - i - 1]] if len(df2) > off + i - 1 - off_df2 >= 0 and ly2 - i > y1 and lx2 + i > x1 else float('-inf'), 2))  # from up-left
                return_dict[i] = tmp
                # res.append(tmp)
            # return_dict[LiRi[0]] = res
        if num_workers == 1 or Len <= 1000:
            res = [(0, 0)] * Len
            offsets = [(0, Len)]
            worker_f((0, Len), res)
        else:
            chunk_size = (Len + num_workers - 1) // num_workers
            offsets = [(i, min(Len, i + chunk_size)) for i in range(0, Len, chunk_size)]
            res = [(0, 0)] * Len
            pool = []
            for offset in offsets:
                p = threading.Thread(target=worker_f, args=(offset, res))
                p.start()
                pool.append(p)
            for p in pool:
                p.join()
        _df = res
        # for li in offsets:
        #     _df.extend(res[li[0]])
        if rx2 == mid:
            f.append(_df[-1])
        df, df2 = _df, df
        off_df, off_df2 = off, off_df
        lx, ly = lx2, ly2
        rx, ry = rx2, ry2
    assert len(f) == m

    # Right part
    g = []
    dg = [(0, 0)] # Single cell at (x2, y2)
    off_dg = 0
    dg2 = []
    off_dg2 = 0
    lx, ly = x2, y2
    rx, ry = x2, y2
    for sum_xy in range(x2 + y2 - 1, mid + y1 - 1, -1):
        lx2 = max(mid, lx - 1)
        ly2 = sum_xy - lx2
        ry2 = max(ry - 1, y1)
        rx2 = sum_xy - ry2
        Len = rx2 - lx2 + 1
        _dg = []
        off = off_dg + (1 if lx - 1 < mid else 0)
        for i in range(Len):
            tmp = (float('-inf'), -1)
            tmp = max(tmp, (dg[off + i - 1 - off_dg][0] + delta['-'][t[ly2 - i]] if len(dg) > off + i - 1 - off_dg >= 0 and ly2 - i + 1 <= y2 else float('-inf'), 0)) # from up
            tmp = max(tmp, (dg[off + i - off_dg][0] + delta[s[lx2 + i]]['-'] if len(dg) > off + i - off_dg >= 0 and lx2 + i + 1 <= x2 else float('-inf'), 1)) # from left
            tmp = max(tmp, (dg2[off + i - 1 - off_dg2][0] + delta[s[lx2 + i]][t[ly2 - i]] if len(dg2) > off + i - 1 - off_dg2 >= 0 and ly2 - i + 1 <= y2 and lx2 + i + 1 <= x2 else float('-inf'), 2)) # from up-left
            _dg.append(tmp)
        if lx2 == mid:
            g.append(_dg[0])
        dg, dg2 = _dg, dg
        off_dg, off_dg2 = off, off_dg
        lx, ly = lx2, ly2
        rx, ry = rx2, ry2
    g = g[::-1]
    if x2 == mid:
        g.append(dg[0])
    assert len(g) == m
    # print(x1, y1, x2, y2)
    # print(f)
    # print(g)

    best = None
    best_sum = None
    for i in range(m):
        if best_sum is None or best_sum < f[i][0] + g[i][0]:
            best_sum = f[i][0] + g[i][0]
            best = i
    # print(mid, best)
    dfs(x1, y1, mid, best + y1, result)
    if g[best][1] == 0:
        x3 = mid
        y3 = best + 1
    elif g[best][1] == 1:
        x3 = mid + 1
        y3 = best
    else:
        x3 = mid + 1
        y3 = best + 1
    y3 += y1
    dfs(x3, y3, x2, y2, result)
