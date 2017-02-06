# e-conomics-hiring-assignments-solutions
My solution to the hiring assignment presented in: https://github.com/e-conomic/hiring-assigments/tree/master/autosuggest/bankrec-assignment

## Setup
Make sure you've set your locale.

    export LC_ALL=en_US.UTF-8
    export LANG=en_US.UTF-8

Set up your virtual environment and install the relevant packages.

    virtualenv -q --no-site-packages -p python2.7 .venv
    ./.venv/bin/pip install pip==9.0.1 setuptools==18.2
    ./.venv/bin/pip install -r requirements.txt

Activate the environment and start Jupyter notebook.

    source .venv/bin/activate
    PYTHONPATH=src jupyter-notebook

When done, deactivate the virtual environment.

    deactivate