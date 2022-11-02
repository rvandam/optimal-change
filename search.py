def find_fewest_coins(coins, target):
    # flag impossible requests
    if target < 0:
        raise ValueError("target can't be negative")
    if 0 < target < min(coins):
        raise ValueError("can't make target with given coins")
    
    # the greedy algorithm is much faster
    # and cannot be wrong with only 1 or 2 coin results
    # since you can't beat a 1 coin result
    # and a 2 coin result can only be beat by a 1 coin result, which the greedy algorithm would find
    # so always try it first so we can avoid the more expensive algorithm
    try:
        greedy = find_fewest_coins_greedy(coins, target)
        if greedy and len(greedy) < 3:
            return greedy
    except ValueError:
        pass # ignore and try with non-greedy algorithm

    return find_fewest_coins_optimal(coins, target)

def find_fewest_coins_optimal(coins, target):
    # otherwise we go with the slower but always optimal algorithm
    # build up best solutions one cent at a time
    # until we get to the target
    bests = [[]]
    for t in range(1, target+1):
        best = []
        for coin in coins:
            if t == coin:
                # perfect match, just one coin
                best.append([coin])
            elif t < coin:
                # coin too big to contribute, use previous best
                best.append(best[-1] if len(best) else [])
            else:
                # test if adding coin makes a shorter list than the best so far
                # None means no solution (such as t=1 when min(coins) = 2)
                without_coin = best[-1] if len(best) else None
                with_coin = bests[-coin] + [coin] if bests[-coin] else None
                shortest = min((x for x in (with_coin, without_coin) if x), key=len) if with_coin or without_coin else None
                best.append(shortest)
        bests.append(best[-1] if len(best) and best[-1] and sum(best[-1]) == t else [])

    # only used by coin set search
    if target == 99:
        return (max(len(x) for x in bests), sum(len(x) for x in bests))

    if sum(bests[-1]) != target:
        raise ValueError("can't make target with given coins")
                
    return sorted(bests[-1])

def find_fewest_coins_greedy(coins, target):
    results = []
    for coin in coins[::-1]:
        while target >= coin:
            results.append(coin)
            target -= coin
    if target:
        raise ValueError("can't make target with given coins")
    return sorted(results)

# surprisingly odd results:
# best 2 coin set with score (18, 900) is [1, 10]
# best 3 coin set with score (9, 516) is [1, 7, 23]
# best 4 coin set with score (6, 389) is [1, 5, 18, 25]
# best 5 coin set with score (5, 331) is [1, 3, 11, 27, 34] # ?optimal or just ran out of time?
# scores are (largest coin count, sum of all coin counts)
# so for all numbers 1-99, which set generates the least change
# TODO: this brute force approach is very inefficient and redundant
# this could probably be a lot faster if we moved part of the search into the dynamic
# build part because for any given list, we already always calculate all the strict subsets
# so we could just do a 6 coin search and get all subsets for free
def search_coin_sets():
    # what's the best set of coins of size 2, 3, 4, etc
    min_score = [(100000, 100000)] * 7
    min_coins = [[] for _ in range(7)]
    # ranges are set by trial and error to try to avoid timeouts
    # but bad ranges could result in suboptimal results
    for i in range(2, 50):
        coins = [1, i]
        _check(coins, min_score, min_coins)
        for j in range(i+1, 50):
            coins = [1, i, j]
            _check(coins, min_score, min_coins)
            for k in range(j+1, 50):
                coins = [1, i, j, k]
                _check(coins, min_score, min_coins)
                for l in range(k+1, 50):
                    coins = [1, i, j, k, l]
                    _check(coins, min_score, min_coins)
                    for m in range(l+1, 50):
                        coins = [1, i, j, k, l, m]
                        _check(coins, min_score, min_coins)

    for x in range(2, 7):
        print(f"best {x} coin set with score {min_score[x]} is {min_coins[x]}")
    
def _check(coins, min_score, min_coins):
    n = len(coins)
    try:
        score = find_fewest_coins_optimal(coins, 99)
        #print(coins, score)
        if score < min_score[n]:
            print("new max=", coins, score)
            min_score[n] = score
            min_coins[n] = coins
    except Exception as e:
        raise e

if __name__ == "__main__":
    search_coin_sets()
