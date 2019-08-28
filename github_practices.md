Github Tips & Tricks
---

## 1. Syn a forked repo with the upstream repo

- On local repo, add remote repository (side by side remote ```origin```) link to upstream repo. Guide: https://help.github.com/en/articles/configuring-a-remote-for-a-fork 
- Fetch upstream repo to local repo & merge code/scripts with remote ```origin```. Then, push the changes to forked repo. Guide: https://help.github.com/en/articles/syncing-a-fork

List current remote repository:

```bash
git remote -v
```

Add upstream repository:

```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git
```

Fetch upstream:

```bash
git fetch upstream
```

Merge and push

```bash
git merge upstream/master
git push origin master
```


## 2. Online Markdown Editor for GitHub

- Link: https://jbt.github.io/markdown-editor/
