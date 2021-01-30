from setup import N, words

def response(guess, correct):
    guess = list(guess)
    correct = list(correct)
    known = []
    misplaced = []
    for idx, (char_guess, char_correct) in enumerate(zip(guess, correct)):
        if char_guess == char_correct:
            known.append(idx)
            guess[idx] = None
            correct[idx] = None
    
    for idx in range(N):
        if (char_guess := guess[idx]) is not None and char_guess in correct:
            misplaced.append(idx)
            correct[idx] = None
    
    return (tuple(known), tuple(misplaced))

def score(guess):
    return len(set(response(guess, correct) for correct in words))

if __name__ == '__main__':
    print(max({w:score(w) for w in words}, key = lambda x: x[1]))
    
    
