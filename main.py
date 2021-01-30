from collections import defaultdict
from setup import words, alpha, N


class PoolProgress:
    def __init__(self, pool, update_interval=1):
        self.pool = pool
        self.update_interval = update_interval

    def track(self, job):
        task = self.pool._cache[job._job]
        while task._number_left > 0:
            print(f"Tasks remaining = {task._number_left*task._chunksize}")
            time.sleep(self.update_interval)


def infer(*infos):
    if not infos or not infos[0]:
        return [set() for _ in range(N)], []

    forbidden = [set().union(*[fbds[idx] for fbds, promises in infos]) for idx in range(N)]

    promises = [
        (char, [idx for idx in positions if char not in forbidden[idx]])
        for _, promises_single in infos
        for char, positions in promises_single
    ]

    known = [
        (char, positions[0]) 
        for char, positions in promises 
        if len(positions)==1
    ]
    while known:
        for char, idx in known:
            forbidden[idx] = set(a for a in alpha if a != char)
            for other_char, other_positions in promises:
                if idx in other_positions:
                    other_positions.remove(idx)
        
        promises = [(char, positions) for char, positions in promises if len(positions) > 0]
        known = [(char, positions[0]) for char, positions in promises if len(positions)==1]
    
    return forbidden, promises


def info(correct, guess):

    indices = list(range(len(correct)))

    correct_positions = [
        idx 
        for idx, (char_correct, char_guess) in enumerate(zip(correct, guess))
        if char_correct == char_guess
    ]

    incorrect_positions = [
        idx 
        for idx, (char_correct, char_guess) in enumerate(zip(correct, guess))
        if char_correct != char_guess
    ]

    forbidden = [set() for _ in guess]
    promises = []
    
    different_positions_values_guess   = [guess[idx]   for idx in incorrect_positions]
    different_positions_values_correct = [correct[idx] for idx in incorrect_positions]

    for idx, (char_correct, char_guess) in enumerate(zip(correct, guess)):
        if idx in correct_positions:
            forbidden[idx] = set(a for a in alpha if a != char_correct)
        else:
            forbidden[idx].add(char_guess)
            if char_guess in different_positions_values_correct:
                different_positions_values_correct.remove(char_guess)

                promised_positions = [
                    idx_other
                    for idx_other in incorrect_positions 
                    if guess[idx_other] != char_guess
                ]
                
                promises.append((char_guess, promised_positions))

    return forbidden, promises

def info_many(correct, guesses):
    return infer([info(correct, guess) for guess in guesses])

def print_fbd(forbidden):
    if len(forbidden) <= len(alpha)//2:
        return f'Forbid {sorted(forbidden)}.'
    return f'Require {[a for a in alpha if a not in forbidden]}'

def is_valid(word, info):
    forbidden, promises = info
    if any(letter in forbidden[idx] for idx, letter in enumerate(word)):
        return False

    return all(
        char in [word[idx] for idx in positions]
        for char, positions in promises
    )

def possible_guesses(info):
    """Return the number of possible correct words that match are possible with the information received from our guesses.
    """
    return sum(is_valid(word, info) for word in words)


def accuracy(guesses):
    """Return the likelihood of guessing the correct word after submitting the list of guesses.
    """
    s = 0
    for correct_word in words:
        likelihood = 1/possible_guesses(info_many(correct_word, guesses))
        s += likelihood
        if (idx + 1) % 100 == 0:
            print(f'{idx+1:4}/{num_words} completed, score {s/(idx+1)*100:6.2f} percent.')
    return s/num_words
    
def find_best_addition(guesses):
    prev_infos = {correct_word: info_many(correct_word, guesses) for correct_word in words}
    scores = defaultdict(float) # Higher is better
    for guess in words:
        for correct, prev_info in prev_infos.items():
            new_info = infer(prev_info, info(correct, guess))
            scores[guess] += 1/possible_guesses(new_info)
        print(f'guesses = [{guess}] leads to a score of [{scores[guess]}]')

    return max(scores.items(), key = lambda x: x[1])
    
def find_best_word():
    scores = defaultdict(float)
    for guess in words[:2]:
        score = sum(1/possible_guesses(info(correct, guess)) for correct in words)
        scores[guess] = score
        print(f'guesses = [{guess}] leads to a score of {score:4.2f}.')
    return max(scores.items(), key = lambda x: x[1])

if __name__ == '__main__':
    print(find_best_word())
    # find_best_addition([])

    # g = max(words, key = lambda w: accuracy([w]))
    # print(g, accuracy[g])

    # # correct = 'lminn'
    # # guess   = 'limin'
    
    # # fbd, prom = info(correct, guess)
    # # print('Fordid')
    # # for f in fbd:
    # #     print(sorted(f))
    # # print('Promises')
    # # for p in prom:
    # #     print(p)

    # for w in words:
    #     if w[0:2] == 'ae' and w[3:5] == 'is':
    #         print(w)
    # print('done!')

    # correct = 'aegis'
    # guesses = ['tears', 'think', 'there', 'their', 'theme']
    # print(accuracy(guesses))
    # for guess in guesses:
    #     forbidden, promises = info(correct, guess)
    #     print(f'Guess = {guess}')
    
    #     print('\tFordid')
    #     for f in forbidden:
    #         print(f'\t\t{print_fbd(f)}')
    #     print('\tPromises')
    #     for p in promises:
    #         print(f'\t\t{p}')
    
    # info = info_many(correct, guesses)
    # forbidden, promises = info
    # print('\tFordid')
    # for f in forbidden:
    #     print(f'\t\t{print_fbd(f)}')
    # print('\tPromises')
    # for p in promises:
    #     print(f'\t\t{p}')

    # print(is_valid(correct, info))
    # # for w in words:
    # #     try:
    # #         v = is_valid(w, info)
    # #         # print(f'{w} {v}')
    # #     except IndexError as exc:
    # #         print(exc)
    # #         print(f'failed on {repr(w)}')
    # #         print(info)