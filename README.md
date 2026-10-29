# Tokenization in NLP: Lab Notes

Notes on character, word and sentence tokenization: when to use each method, their weaknesses, and how to handle tricky cases (contractions, social media, Arabic, text without spaces).

## Table of Contents

1. [Character-level tokenization](#1-character-level-tokenization)
2. [Word tokenization: `split()` vs `word_tokenize` vs `TweetTokenizer`](#2-word-tokenization)
3. [What counts as a word?](#3-what-counts-as-a-word)
4. [Sentence tokenization](#4-sentence-tokenization)
5. [Tokenizing text without spaces (Maximum Matching)](#5-tokenizing-text-without-spaces-maximum-matching)
6. [Arabic: specific challenges](#6-arabic-specific-challenges)
7. [Text normalization and cleaning](#7-text-normalization-and-cleaning)
8. [Quick decision guide](#8-quick-decision-guide)

---

## 1. Character-level tokenization

### `.isalpha()`

`.isalpha()` returns `True` if the character is a letter.

| Character | Result |
|-----------|--------|
| `"n"` | `True` |
| `"i"` | `True` |
| `" "` | `False` |
| `"!"` | `False` |
| `"5"` | `False` |

Therefore, a function that filters with `.isalpha()` **ignores spaces, punctuation, and digits**.

### When is character-level tokenization useful?

| Use case | Why it works |
|----------|--------------|
| (a) Spelling correction, typos, unknown words | Even if a word was never seen, its letters were |
| (b) Language identification | Each language has its own letter frequencies |
| (c) OCR and handwriting recognition | Input is naturally character by character |
| (d) Languages with huge vocabularies or no spaces | Avoids needing a giant word list |
| (e) Small character-level models, and as the base for sub-word methods | Small vocabulary |

**Drawback:** sequences become very long, and single characters carry little meaning.

---

## 2. Word tokenization

### Is punctuation a separate token for `word_tokenize`?

**Yes.** Commas, periods, exclamation marks, parentheses and ellipses all become their own tokens.

### Weaknesses of `split()`

1. Punctuation stays glued to words: `Well,` and `odd)!` are counted as different tokens from `Well` and `odd`, which **inflates the vocabulary**.
2. Brackets and ellipses are not separated.
3. Contractions (`that's`) are not split.
4. Several symbols stuck together (`)!`) form one weird token.

### When is `split()` preferable?

When speed and simplicity matter and the text is already clean, for example:

- log files or CSV-like lines with clear separators
- text that was already tokenized (tokens separated by single spaces)
- quick prototypes
- very large data where a linguistic tokenizer would be too slow

It also needs **no library**.

### Comparison of the three tokenizers

| Feature | `split()` | `word_tokenize` | `TweetTokenizer` |
|---------|-----------|-----------------|------------------|
| Needs a library | No | Yes (NLTK) | Yes (NLTK) |
| Speed | Fastest | Slower | Slower |
| Separates punctuation | No (glued to words) | Yes | Yes |
| Keeps contractions whole (`can't`) | Yes (no splitting at all) | No (splits `ca` + `n't`) | Yes |
| Keeps hashtags, mentions, URLs | Yes (but glued to punctuation) | No (shreds them) | Yes |
| Keeps emoticons (`:)`) | Yes (but glued to punctuation) | No (shreds them) | Yes |
| Best for | Clean, pre-tokenized text, logs, prototypes | Clean newspaper-style English | Social media, informal text |

### Social media: use `TweetTokenizer`

`TweetTokenizer` was designed for this kind of text. It:

- keeps hashtags (`#NLP`), mentions (`@prof_ahmed`), URLs and emoticons (`:)`) as single tokens
- keeps contractions (`can't`) whole
- still separates real punctuation (`!`)

`word_tokenize` is trained on clean newspaper-style English and shreds hashtags, URLs and emoticons, which carry a lot of meaning on social media (**a smiley is a strong sentiment signal**). `split()` keeps those items but glues punctuation to words (`gooood!!`).

Useful options:

```python
from nltk.tokenize import TweetTokenizer

tok = TweetTokenizer(
    reduce_len=True,      # "gooood" -> "goood"
    strip_handles=True,   # removes @mentions
    preserve_case=False,  # lowercases everything
)
```

| Option | Effect |
|--------|--------|
| `reduce_len=True` | Shortens repeated letters (`gooood` becomes `goood`) |
| `strip_handles=True` | Removes `@mentions` |
| `preserve_case=False` | Lowercases everything |

### Keeping `isn't` as a single token

**Recommendation:** `TweetTokenizer`, or a regex, for any task that needs `isn't` as a single token. It keeps the contraction together and still separates punctuation.

```python
import re

pattern = r"\w+(?:'\w+)?|[^\w\s]"
re.findall(pattern, "It isn't odd!")
```

How the regex reads:

| Part | Meaning |
|------|---------|
| `\w+` | a word |
| `(?:'\w+)?` | optionally followed by an apostrophe and more letters |
| `\|` | OR |
| `[^\w\s]` | any single symbol (punctuation) |

---

## 3. What counts as a word?

Three cases that make the definition hard:

- **Contractions:** shortened forms of words using an apostrophe, e.g. `don't` = `do not`.
- **Multi-word proper nouns:** names made of several words, e.g. `New York City`, `Albert Einstein`.
- **Hyphenated compounds:** words joined by hyphens, e.g. `well-known`, `part-time`.

### Why is defining a "word" hard?

Is `don't` one word or two? Is `New York` one word or two? Is `state-of-the-art` one word or four? Writing conventions (spaces, apostrophes, hyphens) do not always match the linguistic notion of a word.

### The trade-off every tokenizer must make

| Strategy | Example | Advantages | Disadvantages |
|----------|---------|------------|---------------|
| **Split more** | `do` + `n't`, `state` + `of` + `the` + `art` | Smaller vocabulary, exposes the negation | Loses the idea of a single unit |
| **Split less** | `isn't`, `New York` | Units stay meaningful | Bigger vocabulary with many rare tokens |

There is **no universal best choice**: it depends on the application.

---

## 4. Sentence tokenization

### Why is it genuinely hard?

Because the **period is ambiguous**. It is used for:

| Usage | Example |
|-------|---------|
| Sentence end | `He left.` |
| Abbreviations | `Dr.`, `etc.` |
| Decimals | `1.5` |
| Initials | `J. K. Rowling` |
| Websites | `univ.dz` |
| Ellipses | `...` |

Sentences can also end without any punctuation (titles, tweets, lists) or hide inside quotation marks. A simple split on periods cannot resolve all these cases, so we need **rules or statistics**.

### A heuristic to avoid being fooled by abbreviations

Keep a list of known abbreviations (`Dr.`, `Mr.`, `Mrs.`, `a.m.`, `p.m.`, etc.). When a period follows one of them, do **not** end the sentence, unless the next word looks like the start of a new sentence (capital letter and a common sentence starter such as `He`, `She`, `The`).

Other cheap rules:

- A period between two digits (`1.5`) is never a boundary.
- A period followed by a lowercase letter is not a boundary.

> NLTK's **Punkt** tokenizer learns such abbreviations from large amounts of text.

---

## 5. Tokenizing text without spaces (Maximum Matching)

The same greedy method works on English text written without spaces, and shows its main weakness: **ambiguity**.

```python
en_dict = {"the", "theta", "table", "tab", "le", "natural", "language", "processing"}
print(max_match("naturallanguageprocessing", en_dict))
print(max_match("thetable", en_dict))
```

Output:

```
['natural', 'language', 'processing']
['theta', 'b', 'le']
```

The second result is **wrong**: greedy matching picked `theta` instead of `the` + `table`.

Real tools (**jieba** for Chinese, **MeCab** for Japanese) improve this with word-frequency statistics or machine-learning models that compare alternative cuts and choose the most probable one.

---

## 6. Arabic: specific challenges

| | Challenge | Consequence |
|---|-----------|-------------|
| (a) | **Clitics:** conjunctions, articles and prepositions are glued to the word | One written word may contain 3 or 4 units |
| (b) | **Rich morphology:** one root gives many forms | Large vocabulary |
| (c) | **Optional vowel marks (diacritics):** the same word can be written with or without them | Spelling variants |
| (d) | **Letters change shape by position, text is written right to left** | Affects processing and display |

---

## 7. Text normalization and cleaning

### Lowercasing: a situation where it causes a mistake

In Named Entity Recognition (finding names of people, companies, places), **capital letters are a key clue**. After lowercasing, different entities look identical:

| Original | Meaning | Lowercased | Collides with |
|----------|---------|------------|---------------|
| `Apple` | company | `apple` | the fruit |
| `Bill` | a person | `bill` | an invoice |
| `Turkey` | country | `turkey` | the bird |

As a result, the system may fail to tag the company, or may tag a fruit as an organization.

### Non-breaking space (`\u00a0`) and zero-width space (`\u200b`)

In Python 3, `\s` on normal text strings **already includes `\u00a0`**, so no change is needed.

If your version or flags (`re.ASCII`) do not handle it, either:

```python
text = text.replace("\u00a0", " ")   # pre-process

import re
re.split(r"[\s\u00a0]+", text)       # or use an explicit character class
```

**Careful:** the zero-width space `\u200b` is **NOT** matched by `\s`. It is invisible but stays in the text, so it must be removed separately:

```python
text = text.replace("\u200b", "")
```

| Character | Name | Matched by `\s` in Python 3? | Fix |
|-----------|------|------------------------------|-----|
| `\u00a0` | Non-breaking space | Yes (unless `re.ASCII`) | `replace("\u00a0", " ")` or `[\s\u00a0]+` if needed |
| `\u200b` | Zero-width space | **No** | Remove it separately |

### Discussion: numbers (replace or keep?)

| Replace numbers with a placeholder when... | Keep numbers as they are when... |
|--------------------------------------------|----------------------------------|
| The exact value does not matter for the task (topic or spam classification): `12 points`, `20 hours` all look alike. | Exact values carry the meaning: financial documents (amounts, interest rates), medical texts (a dose of `5 mg` vs `50 mg`), legal texts (article 15, a deadline of 30 days), scientific results. |
| It reduces the vocabulary, since each number would otherwise be a different rare word. | A downstream step needs to compute with them or compare them. |
| Numbers are very diverse (phone numbers, IDs) and would flood the vocabulary. | |

### Is removing `!!!` and repeated letters a good idea for sentiment analysis?

**No, it is not a good idea.**

For sentiment analysis, `!!!` and `SOOOO good` express **intensity**: `soooo good` is more positive than `good`. Removing them throws away signal.

Better approach:

- Keep the exclamation marks.
- Collapse repeated letters to **at most two** (`soo`) instead of deleting the idea of emphasis. This keeps a trace of the elongation while merging the endless variants (`soooo`, `sooooo`).

```python
import re

text = "soooooo good!!!"
re.sub(r"(\w)\1{2,}", r"\1\1", text)   # 'soo good!!!'
```

If the task were **topic classification** (what is this text about?), removing them would be harmless.

| Task | Remove `!!!` and repeated letters? |
|------|------------------------------------|
| Sentiment analysis | No: keep `!!!`, collapse repeats to two letters |
| Topic classification | Yes: harmless |

---

## 8. Quick decision guide

| Situation | Recommended tool |
|-----------|------------------|
| Clean, already-separated text, logs, CSV lines, quick prototype | `split()` |
| Clean newspaper-style English | `word_tokenize` |
| Tweets, hashtags, mentions, emoticons, URLs | `TweetTokenizer` |
| Need `isn't` as a single token with punctuation separated | `TweetTokenizer` or the regex `\w+(?:'\w+)?\|[^\w\s]` |
| Sentence splitting with abbreviations | Punkt (`sent_tokenize`) or abbreviation-list rules |
| Text without spaces (Chinese, Japanese) | `jieba`, `MeCab` (better than greedy Maximum Matching) |
| Typos, unknown words, OCR, language identification | Character-level tokenization |
| NER (names of people, companies, places) | Do **not** lowercase: capitals are a key clue |
| Sentiment analysis | Keep `!!!`, collapse repeated letters to two (`soooo` to `soo`) |
| Topic or spam classification | Replace numbers with a placeholder, noise removal is harmless |
| Financial, medical, legal, scientific text | Keep numbers as they are |
| Invisible characters in scraped text | Remove `\u200b` separately; `\s` already covers `\u00a0` |