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
