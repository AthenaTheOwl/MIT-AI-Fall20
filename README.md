# MIT AI Fall 2020 coursework archive

Ten folders from 6.034: search, games, CSP, k-NN, neural nets, SVMs, Bayes nets, boosting. The labs were graded; the archive is kept as coursework, with old grader files removed from HEAD.

## What this repo is

This is a preserved coursework archive for MIT 6.034. It is useful as a map of the classical AI toolkit before the current model era took over the room.

The folders cover:

- rule systems and search
- game search
- constraint satisfaction
- nearest neighbors
- neural networks
- support vector machines
- Bayesian networks
- boosting
- short quizzes and lab scaffolds

## Run locally

The labs were written for the course environment. Use a local Python environment and run each lab from its own folder.

Run the checked-in tester for an individual lab:

```bash
cd Lab2
python tester.py
```

## Security note

Old grader credential files are not part of the current HEAD. Treat any historic course-grader credentials as expired and unusable, and do not add new `key.py` files to the repo.

## Live demo

This repo has a small Streamlit index for browsing the archive.

<!-- live-url -->

Streamlit entrypoint:

```text
streamlit_app.py
```

Local run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## Why keep it

The repo shows the older stack of AI ideas in executable form. Search still searches. CSPs still prune. Bayes nets still make hidden assumptions visible. That makes the archive a useful reference point beside the newer agent and eval repos.

## License

Course materials remain subject to their original course terms.
