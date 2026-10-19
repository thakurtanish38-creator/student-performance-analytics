# Session 5 Summary: Git and GitHub

**Date:** 19 October 2026
**Project:** Student Performance Analytics

---

## 1. Goal

Save the project with version history using Git, make it reproducible with `requirements.txt`, write a README, and put it online on GitHub.

## 2. What we built

| Item | What it is |
|---|---|
| `.git/` (hidden folder) | Git's record of the project's history. Created by `git init`. |
| `.gitignore` | A list of things Git must never save or upload |
| `requirements.txt` | The libraries the project needs, with exact versions |
| `README.md` | The front page of the project on GitHub |
| `docs/` | Session notes and `findings.md` |
| GitHub repository | `https://github.com/thakurtanish38-creator/student-performance-analytics` |

## 3. Key words

| Word | Plain meaning |
|---|---|
| **Git** | A tool on your computer that keeps snapshots of your project, so you can go back to any earlier one |
| **GitHub** | A website that stores your Git project online, and works as a portfolio |
| **Repository (repo)** | One project's folder, tracked by Git |
| **Commit** | A named snapshot of the project |
| **Staging area** | The "box" where you pack changes before sealing them as a commit |
| **Branch** | A line of snapshots. Ours is called `main`. |
| **Remote** | An online copy of the repository. `origin` is the nickname for our GitHub one. |
| **Push** | Upload your snapshots to the remote |
| **Hash** | The short unique ID of a commit (like `40d7de0`) |
| **Untracked / modified** | Untracked: Git sees the file but doesn't track it yet. Modified: a tracked file was edited. |

## 4. Commands we used

| Command | What it does |
|---|---|
| `git config --global user.name` / `user.email` | Reads or sets the name and email stamped on your commits |
| `git rev-parse --show-toplevel` | Shows which folder Git treats as the top of the repository |
| `git status` | Shows what changed and what is in the staging box |
| `git init -b main` | Starts tracking the current folder, with the main branch called `main` |
| `git add .` / `git add <file>` | Packs everything (or one file) into the staging box |
| `git commit -m "message"` | Seals the box into a snapshot with a label |
| `git log --oneline` | Shows the history, one line per commit |
| `git commit --amend --reset-author --no-edit` | Redoes the latest commit with the current name and email (safe only before pushing) |
| `git remote add origin <address>` | Links the project to the online repository |
| `git remote -v` | Lists the remotes |
| `git push -u origin main` | Uploads `main` to GitHub the first time and links the two |
| `git push` | Uploads new commits afterwards |

**The everyday routine:** check (`git status`), pack (`git add`), seal (`git commit -m`), upload (`git push`).

## 5. Code walkthrough

### .gitignore

```
# Virtual environment (big, and can be rebuilt)
.venv/

# Python cache files
__pycache__/
*.pyc

# Secrets and private data (for later in the project)
.env
*.db
*.sqlite3

# Editor and operating-system clutter
.vscode/
Thumbs.db
.DS_Store
```

- Lines starting with `#` are comments for humans.
- `.venv/` is the virtual environment. It is huge and anyone can rebuild it from `requirements.txt`.
- `__pycache__/` and `*.pyc` are temporary files Python creates. The `*` is a wildcard meaning "anything".
- `.env` is the standard name for a file holding secrets, such as passwords. We list it now so it can never be uploaded by accident.
- `*.db` and `*.sqlite3` are database files. Later, users' real academic records will live in one, and they must never be uploaded.
- The last group is editor and Windows clutter.
- `data/` is deliberately **not** ignored: the dataset licence (CC BY 4.0) allows sharing with credit, and keeping it lets anyone run the project.

### requirements.txt

```
python -m pip freeze | Out-File -Encoding utf8 requirements.txt
```

- `python -m pip freeze` lists every installed library with its exact version, such as `pandas==3.0.6`.
- `|` is a **pipe**: it passes the output of the left command into the right one.
- `Out-File -Encoding utf8 requirements.txt` saves it as a file. We avoid `>` because on Windows PowerShell it can save in a text format other tools cannot read well.
- Many lines are **dependencies**: helper libraries that pandas, matplotlib and Streamlit need, installed automatically.
- Anyone can rebuild the setup with `pip install -r requirements.txt`. This is what makes the project reproducible.

### README.md

- Written in **Markdown**: `#` makes a heading, `-` makes a bullet, and backticks mark code.
- Sections: Status (honest about what is done and what is only planned), What the analysis found, Project structure, How to run it, Dataset and credit, Limitations, Author.
- The dataset credit is required by the CC BY 4.0 licence:
  Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T

## 6. Key ideas (write these in your own words)

- What is the difference between Git and GitHub?
- What is a commit, and why is it a two-step process (`add` then `commit`)?
- Why do we have a `.gitignore`, and what must never be uploaded?
- What does `requirements.txt` do, and why does it matter?
- What is a README for, and why must it be honest about what is finished?
- Why is it safe to rewrite a commit before pushing, but risky after?

## 7. Errors and fixes

| Problem | Cause | Fix |
|---|---|---|
| Git was tracking the **outer** folder, not the project folder | A repository had been created one level too high (probably by VS Code) | Confirmed it had no remote and no commits, deleted its `.git` folder, then ran `git init -b main` inside the project folder |
| A stray `student-merge.R` file in the outer folder | Dropped there by mistake when copying files | Deleted it |
| `New-Item` error for `.gitignore` | The file already existed, because it had been created in VS Code | No fix needed. Windows refuses to create the same file twice. |
| VS Code showed the outer folder in the Explorer | The wrong folder had been opened | **File → Open Folder...** and chose the inner project folder |

Lessons: read the path before a command, check which folder is open, and look at `git rev-parse --show-toplevel` when Git behaves strangely.

## 8. Interview lines

**Git:** "I used Git for version control and pushed the project to GitHub, with a `.gitignore` that keeps out the virtual environment, secrets and database files, and a `requirements.txt` so the setup can be reproduced."

**Debugging:** "Git was tracking a parent folder by mistake. I diagnosed it with `git rev-parse --show-toplevel`, confirmed the repository was empty and had no remote, removed it, and re-initialised it in the correct folder."

## 9. Questions I still have

(Write anything that is still fuzzy here.)

-

## 10. Next session

Session 6: Streamlit basics. We write a first page, run it in the browser, add text, a table and a chart, and learn how Streamlit reruns the script when you click something.

---

*Dataset: Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T. Licensed CC BY 4.0.*
