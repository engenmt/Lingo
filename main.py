from setup import words

def response(guess, correct):
    """Return the information received upon guessing the word `guess` into the word `correct`."""
    guess = list(guess)
    correct = list(correct)
    known = []
    misplaced = []
    
    for idx in range(5):
        if guess[idx] == correct[idx]:
            known.append(idx)
            guess[idx] = None
            correct[idx] = None
    
    for idx in range(5):
        if (char_guess := guess[idx]) is not None and char_guess in correct:
            misplaced.append(idx)
            correct[correct.index(char_guess)] = None
    
    return (tuple(known), tuple(misplaced))


def score(*guesses):
    """Return the score of a sequence of guesses. The score is proportional to how good the guesses are.

    Consider all correct words. Each correct word gives information (1) the first letter and
    (2) the sequence of responses based on the guessed words. There is an equivalence relation
    on the set of correct words, where two words are equivalent with respect to the guesses if
    their information returned is identical. The probability that you guess correctly given 
    a sequence of guesses is proportional to the number of equivalence classes, so this function
    returns the number of equivalence classes.
    """
    return len(set(
        sum((response(guess, correct) for guess in guesses), (correct[0],)) for correct in words
    ))


def best_addition(*guesses):
    """Given a sequence of guesses, return the best guessed word to add on."""
    return max(words, key = lambda w: score(w, *guesses))


if __name__ == '__main__':
    
    g = ('clipt', 'khoum', 'warns', 'gybed')
    print(g, score(*g))
