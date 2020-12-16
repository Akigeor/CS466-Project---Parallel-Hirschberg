
keys = ['A', 'C', 'T', 'G', '-']
delta = {}
for i in range(len(keys)):
    delta[keys[i]] = {k: v for (k, v) in zip(keys, [1 if keys[i] == keys[j] else -1 for j in range(len(keys))])}

def rand_input(l, alphabet):
    s = ''
    for i in range(l):
        s += alphabet[random.randint(0, len(alphabet) - 2)]
    return s

from tqdm import tqdm
import random
import argparse

import ParallelHirschberg
import ParallelHirschberg_failed
import NeedlemanWunsch
import Hirschberg

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', required=False, type=str, default='stress')
    parser.add_argument('--num_workers', required=False, type=int, default=2)
    parser.add_argument('--input', required=False, type=str, default='input.txt')
    parser.add_argument('--length', required=False, type=int, default=200)
    args = parser.parse_args()
    task = args.task
    num_workers = args.num_workers
    if task == 'stress': # To check correctness
        random.seed(0)
        test_cases = 10000
        for it in tqdm(range(test_cases), total=test_cases):
            s = rand_input(random.randint(1, args.length), keys)
            t = rand_input(random.randint(1, args.length), keys)
            ans = NeedlemanWunsch.global_align(s, t, delta) # Needleman-Wunsch as ground truth
            out1 = ParallelHirschberg.Hirschberg(s, t, delta, num_workers=num_workers) # Parallel Hirschberg Approach 2
            out2 = ParallelHirschberg_failed.Hirschberg(s, t, delta, num_workers=num_workers) # Parallel Hirschberg Approach 1 (failed)
            out3 = Hirschberg.Hirschberg(s, t, delta) # Plain Hirschberg
            assert ans[0] == out1[0] == out2[0] == out3[0]
    elif task == 'generate_input':
        test_cases = 10
        random.seed(0)
        with open(args.input, 'w') as fout:
            for it in range(test_cases):
                s = rand_input(random.randint(args.length, args.length), keys)
                t = rand_input(random.randint(args.length, args.length), keys)
                fout.write(f'{s} {t}\n')
    else:
        with open(args.input) as fin:
            for line in tqdm(fin):
                s, t = line.strip().split(' ')
                if task == 'run_phb_failed':
                    ParallelHirschberg_failed.Hirschberg(s, t, delta, num_workers=num_workers)
                elif task == 'run_phb':
                    ParallelHirschberg.Hirschberg(s, t, delta, num_workers=num_workers)
                elif task == 'run_hb':
                    Hirschberg.Hirschberg(s, t, delta)
                elif task == 'run_nw':
                    NeedlemanWunsch.global_align(s, t, delta)
                else:
                    raise ValueError()
