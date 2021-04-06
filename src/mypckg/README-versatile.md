# Versatile

This repository stores common functions parallel to multiple projects or code that can serve as template for new products.

In Git you can add a submodule to a repository. This is basically a repository embedded in your main repository. [more info](https://gist.github.com/gitaarik/8735255)

## How to use
### Adding a submodule for the first time in a new repo**
example:
`git submodule add git@github.com:url_to/awesome_submodule.git path_to_awesome_submodule`
versatile:
`git submodule add git@gitlab.com:url_to//versatile.git versatile`

**Updating for the first time a submodule already existing on a repo**
* in your project parent directory run: `git submodule update --init `
or `git submodule update --init versatile`

**Keeping your submodules up-to-date**
  1. If you are inside your project folder doing `git pull` wont update `versatile` manually do: `git submodule update --recursive --remote` instead.
  2. However, if you are inside `versatile` you can also do `git pull` to update it. (Note, if u are inside this folder you can also change versatile repo and push your modifications, plz in this case notice the responsible/author of the file you are editing )

* Note: you will probably get a permission error. i recommend you to configure gitçab ssh keys, you can use the one under versatile/shell_scripts/ssh-renamemeto.ssh. To do this follow the README inside this folder

### Changing content of a submodule
Use a submodule has a normal repo:
* you can clone the submodule and work in it as a normal repo
  - in this case you have to add, commit and push your modification
  - then you have to go to your repo that included the submodule and:
    - `cd` into the submodule folder and `pull`
    - i think there is another way but not sure yet
* you can edit the submodule inside another project
  - just cd to the submodule main folder and work normally as another git repo

## Useful info: ()
https://chrisjean.com/git-submodules-adding-using-removing-and-updating/

## Modules
if you want add a brief description if you are adding a module to `versatile`

### Popular
* Web:
  - Requests: https://pypi.org/project/requests/​
  - Django: https://pypi.org/project/Django/​
  - Flask: https://pypi.org/project/Flask/​
  - Twisted: https://twistedmatrix.com/trac/​
  - BeautifulSoup: https://pypi.org/project/beautifulsoup4/​
  - Selenium: https://selenium-python.readthedocs.io/
* Data science:
  - Numpy: https://numpy.org/​
  - Pandas: https://pandas.pydata.org/​
  - Matplotlib: https://matplotlib.org/​
  - Nltk: https://www.nltk.org/​
  - Opencv: https://opencv-python-tutroals.readth...
* Machine Learning:
  - Tensorflow: https://www.tensorflow.org/​
  - Keras: https://keras.io/​
  - PyTorch: https://pytorch.org/​
  - Sci-kit Learn: https://scikit-learn.org/stable/
* GUI:
  - Kivy: https://kivy.org/#home​
  - PyQt5: https://pypi.org/project/PyQt5/​
  - Tkinter: https://wiki.python.org/moin/TkInter

## Usefull Tutorials:
 * https://www.pyimagesearch.com/2018/03/12/python-argparse-command-line-arguments/

## troubleshoot

* 1
HEAD detached at origin/master
nothing to commit, working tree clean

do:  git checkout master
      git pull
