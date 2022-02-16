Contributing Guide - Code
===================================

Forking
-------
You will need your own fork to work on the code. Go to the `MyView project page <https://github.com/prithvijitguha/MyView>`_ and hit the ``Fork`` button. You will
want to clone your fork to your machine::

    git clone https://github.com/prithvijitguha/MyView.git MyView-username
    cd MyView-yourname
    git remote add upstream https://github.com/prithvijitguha/MyView.git

Creating a Branch
-----------------

You want your master branch to reflect only production-ready code, so create a
feature branch for making your changes. For example::

    git branch shiny-new-feature
    git checkout shiny-new-feature

The above can be simplified to::

    git checkout -b shiny-new-feature

Creating a development environment
----------------------------------
Create a virtual environment. ::

    python -m venv hms_env

Install all the required dependencies. ::

    pip install -r requirements.txt

Run website locally. ::

    uvicorn main:app --reload


Commiting
----------

After you have made your changes. Let's say we have changed file ``modified_file``.::

    git add modified_file

``pre-commit`` does a set of checks before you commit the code. Please ``pre-commit`` before ``commit``.::

    pre-commit install

This will install a set of hooks and create a pre-commit environment.::

    pre-commit run --files modified_file

Once your file passes the checks you can commit your changes. ::

    git commit -m "modified file modified_file"

Pushing your code
-----------------

Once committed you can push your code. ::

    git push origin shiny-new-feature


Create a Pull Request
---------------------
#. Navigate to your repository on GitHub
#. Click on the ``Pull Request`` button
#. You can then click on ``Commits`` and ``Files Changed`` to make sure everything looks
   okay one last time
#. Write a description of your changes in the ``Preview Discussion`` tab
#. Click ``Send Pull Request``.


