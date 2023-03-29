[Back to README.md](../README.md)

# Git Workflow

- [Git-Workflow documentation on atlassian.com](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)


## The branching

### develop branch
We have one main-Branch. This is the branch that will be published on the production server. That one, that is available to the public. <br>
But we don't want to work on this branch, because its easy to mess things up. 

So, there are other branches. Each one has a specific task. 

- **develop**: is derived from _main_. (Only one branch). collects the feature branches for roll out. 
- **feature**: they are derived from _develop_. (for each feature of the project, one branch)
- **hotfix**: they are derived from _main_. (if there is a bug on the production server, this is a small bugfix)
- **release**: created before merging develop into _main_. (one at a time)

<img src="./img/main-develop.svg" alt="main and develop branch" width="600px" style="margin: 20px 0 30px 0">


### feature branches 
Each new feature we include (new model, new view) gets its own feature. We have to discuss how we design one feature. Is it really just one view, or does it include more functions/classes? 

Here is an example workflow. Remember: You create new branches of your local repositories. So there could be changes to  remote _develop_ that are not synchronized with your machine. 
- **So always pull, before you create a new branch!**
- **And always make sure that you are actually on the correct branch, before you start working. ;)**

```console
# pull everytime, before you create a new branch!
git checkout develop
git pull
# create the new branch
git checkout -b feature-xy
```


When the work on one feature branch is finished and its tested, if the pull request is accepted, the feature branch is merged into _develop_. After that, it is deleted, because all its history (all commits) is merged into _develop_. <br>
**Feature branches are always created from the latest _develop_ branch.**

<img src="./img/feature-branches.svg" alt="main and develop branch" width="600px" style="margin: 20px 0 30px 0">

```console
# pull everytime, before you merge! 
git checkout develop
git pull
# while you are checkout on develop, merge feature-xy
git merge feature-xy

# after solving possible pull requests 
# and checking if everything is ok, delete feature branch
git branch -D feature-xy
```

## Release branches

Once the develop branch reaches a certain state, we can decide to roll out the integrated features. This can be done by creating a branch of develop and calling it something like ***release/0.1.0***. After this is done, nothing can be added to the upcoming release, except from bugfixes. Because we took a snapshot of _develop_ whe can, from there on, start working on it again. The release branch gets merged into _main_ if there are no bugs and afterwards, it is deleted. 

```console
git checkout develop
git pull

# create release branch. Number e.g 0.1.0 is the version number
git checkout -b release/0.1.0

# after everything is done merge into main
git checkout main
git pull
git merge release/0.1.0

# if changes were made to the release branch, merge back to develop, too
git checkout develop
git merge release/0.1.0

# then delete release branch
git branch -D release/0.1.0
```

<img src="./img/release-branches.svg" alt="main and develop branch" width="600px" style="margin: 20px 0 30px 0">


## Hotfix branches

Hotfix branches fix problems on a running production server. 
Hotfix branches are the only ones, once the project started, which are created from _main_.

```console
git checkout main
git pull
# now create the hotfix branch
git checkout -b hotfix-xy
```

After solving the bug merge into _main_ AND _develop_. Because we never pull from _main_. _main_ is no WIP branch. It gets only updated by _hotfix-xy_ and _release/xy_ or _develop_. 

```console
git checkout main
git merge hotfix-xy
git checkout develop
git merge hotfix-xy
# then delete the hotfix branch
git branch -D hotfix-xy
```