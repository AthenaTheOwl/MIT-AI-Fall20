<!-- ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ -->

# N° 08 · MIT · 6.034 · fall 2020

> *coursework, kept for posterity.*

problem sets from MIT's introductory artificial intelligence course, fall 2020 (`6.034` / `MIT-AI-Fall20`). archived as-is. the code runs; the labs were graded.

`python` · 2020 · **status: archived**

<!-- ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ -->

## the labs

```
Lab 0   warmup
Lab 1   rule-based systems
Lab 2   search
Lab 3   games
Lab 4   constraint satisfaction
Lab 5   k-nearest neighbors / decision trees
Lab 6   neural networks
Lab 7   support vector machines
Lab 8   bayesian inference
Lab 9   boosting
```

each lab is its own folder. course-provided scaffolding plus implementation. no rewrites, no cleanup — preserved as the artifact of what the class actually was.

## why it's here

a personal time capsule. the algorithms inside are foundational: search, CSP, k-NN, neural nets, SVMs, bayes nets, boosting. the version of you that wrote this code didn't know what it didn't know yet. that's the value.

## security notice

`Lab0/key.py` and `Lab1/key.py` previously contained hardcoded credentials for the MIT 6.034 fall 2020 automated grader (`ai6034.mit.edu/labs/xmlrpc/`). those credentials were valid only for that course offering, were revoked, and the server they pointed at is no longer relevant. the files have been removed from `master`.

if you forked this repo: pull the latest `master`. if you ever need to run the grader scaffolding against a 6.034 server, supply your own `key.py` locally — it's now in `.gitignore` so it won't be committed.

the leak was caught in a 2026-05 audit. git history still contains the old credentials and will be rewritten in a follow-up pass; until then, treat the old values as known-compromised and assume any future reuse is a fresh exposure.

## colophon

MIT 6.034, fall 2020. coursework respects MIT academic policy — if you are currently taking 6.034, do not reference solutions here.

*built downstairs.* — [the basement, room 7](https://github.com/AthenaTheOwl)
