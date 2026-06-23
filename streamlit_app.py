from __future__ import annotations

from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parent

LABS = {
    "Lab0": "warmup",
    "Lab1": "rule-based systems",
    "Lab2": "search",
    "Lab3": "games",
    "Lab4": "constraint satisfaction",
    "Lab5": "nearest neighbors and decision trees",
    "Lab6": "neural networks",
    "Lab7": "support vector machines",
    "Lab8": "bayesian inference",
    "Lab9": "boosting",
}


def lab_files(lab: str) -> list[Path]:
    folder = ROOT / lab
    if not folder.exists():
        return []
    return sorted(path for path in folder.glob("*.py") if path.is_file())


st.set_page_config(page_title="MIT 6.034 lab archive", layout="wide")
st.title("mit 6.034 lab archive")
st.caption("read-only browser for archived fall 2020 artificial-intelligence coursework")

st.info(
    "This app does not run the old course grader or call any MIT service. It indexes "
    "the committed lab folders and shows local verification commands for readers."
)

rows = []
for lab, topic in LABS.items():
    files = lab_files(lab)
    rows.append(
        {
            "lab": lab,
            "topic": topic,
            "python_files": len(files),
            "main_file": f"{lab}/lab{lab.removeprefix('Lab')}.py",
            "tester": f"{lab}/tester.py" if (ROOT / lab / "tester.py").exists() else "",
        }
    )

st.dataframe(rows, width="stretch", hide_index=True)

selected_lab = st.selectbox("lab", list(LABS))
files = lab_files(selected_lab)
left, right = st.columns([1, 2])

with left:
    st.subheader("files")
    for path in files:
        st.write(f"`{path.relative_to(ROOT).as_posix()}`")
    tester = ROOT / selected_lab / "tester.py"
    if tester.exists():
        st.subheader("local check")
        st.code(f"cd {selected_lab}\npython tester.py", language="bash")

with right:
    st.subheader("preview")
    preview_file = st.selectbox("file", files, format_func=lambda p: p.name) if files else None
    if preview_file:
        text = preview_file.read_text(encoding="utf-8", errors="replace")
        st.code(text[:6000], language="python")

st.subheader("archive note")
st.write(
    "The repository is preserved as coursework. If you are currently taking a "
    "similar class, do not use this as a solution source."
)
