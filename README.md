* about  imports [site](https://alex.dzyoba.com/blog/python-import/)


* using virtual enviroments:

Here’s how to install virtualenv  and virtualenvwrapper , both of which will live in your system site-packages  and manage each project’s virtual environment site-packages:

pip install opencvShell [site](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/)

pip install virtualenv virtualenvwrapper

add some lines to your ~/.bashrc  profile.

# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh

then
source ~/.bashrc


Create an environment with mkvirtualenv  ` mkvirtualenv NAME -p python3`
Activate an environment (or switch to a different one) with `workon` .
Deactivate an environment with `deactivate` .
Remove an environment with `rmvirtualenv` .
