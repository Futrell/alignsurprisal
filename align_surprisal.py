""" Problem statement:

We have two sequences X = x_1, ..., x_N and Y = y_1, ..., y_M. Think of them as two different tokenizations of the same string.
Each token of the sequence X comes with a surprisal value.

We want to align X and Y, producing for each token of Y, either:
1. If y corresponds to one token of X, the surprisal value of its corresponding single token in X.
2. If y corresponds to multiple tokens in X, the sum surprisal of its multiple corresponding tokens in X.
3. If multiple y correspond to one token in X, a sentinel value.
4. An irreconcilable sentinel if elements of X cannot be reconciled with elements of Y (for example, X = a bc d, Y = ab cd)
"""
import sys

import pandas as pd
import tokenizations
import rfutils

def align(source_tokens, source_values, target_tokens):
    _, target2source = tokenizations.get_alignments(source_tokens, target_tokens)
    
    # add padding to make it easy to iterate through windows of (y_{t-1}, y_t, y_{t+1})
    target2source.insert(0, [])
    target2source.append([])
    for prev_indices, indices, next_indices in rfutils.sliding(target2source, 3):
        if any(i in next_indices or i in prev_indices for i in indices):
            yield None, "irreconcilable"
        elif len(indices) > 1:
            yield sum(source_values[i] for i in indices), "merged"
        else:
            yield source_values[indices[0]], None

def main(source_filename, source_token_col, source_value_col, target_filename, target_token_col):
    source = pd.read_csv(source_filename)
    source_tokens, source_values = source[source_token_col], source[source_value_col]
    target = pd.read_csv(target_filename)
    target_tokens = target[target_token_col]
    aligned, statuses = zip(*(align(source_tokens, source_values, target_tokens)))
    result = pd.DataFrame({'target_tokens': target_tokens, 'value': aligned, 'status': statuses})
    result.to_csv(sys.stdout)
    
if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
