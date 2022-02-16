Contributing Guide - Documentation
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

    python -m venv myview_env

activate virtual environment.

Windows: ::

    myview_env/scripts/activate


Linux: ::

    source venv/bin/activate


Install all the required dependencies. ::

    pip install -r requirements.txt


Building the documentation
---------------------------

while cd'd into ``MyView``, type the following command to build the documentation.::

    sphinx-build -b html docs/source/ docs/build/html

Let's break down that command:
    - ``sphinx-build``: Command to use python package
    - ``-b``: build flag
    - ``html``: build format(what format your files need to be generated in)
    - ``docs/source``: source destination(rst files)
    - ``docs/build/html``: final destination of html files

Make your changes
------------------

Documentation source material is stored in ``docs/source/`` directory of the repo
Make your changes to the rst files.
If you're adding a new page make sure to add the page name to ``index.rst``

For eg. if new page is ``new_page.rst``

in ``index.rst``, under ``toctree``
    - ``contributing_guide_code``
    - ``contributing_guide_docs``
    - ``new_page``



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




