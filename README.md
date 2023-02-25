# Align surprisal

Reconciles surprisal values from an LM, which might have a weird tokenization, with tokens found in some other corpus such as an RT corpus.

We have two sequences X = x_1, ..., x_N and Y = y_1, ..., y_M. Think of them as two different tokenizations of the same string. Each token of the sequence X comes with a surprisal value.

We want to align X and Y, producing for each token of Y, either:
1. If y corresponds to one token of X, the surprisal value of its corresponding single token in X.
2. If y corresponds to multiple tokens in X, the sum surprisal of its multiple corresponding tokens in X.
3. If multiple y correspond to one token in X, a sentinel value.
4. An irreconcilable sentinel if elements of X cannot be reconciled with elements of Y (for example,  X = a bc d, Y = ab cd)

## Example usage

The file rt1000.csv contains 1000 tokens' worth of data from the Dundee corpus, and the file lm1000.csv contains surprisal values for these tokens from GPT-3, under GPT-3's tokenization.

```{python}
python lm1000.csv token logprob rt1000.csv WORD > aligned.csv
```

## Dependencies

`tokenizations`
`pandas`
`rfutils`: https://github.com/Futrell/rfutils

