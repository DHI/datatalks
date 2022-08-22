# Data Talk 9: How to make your Python code modular and re-usable

*Jesper Sandvig Mariegaard, August 25.*

Are your notebooks/scripts becoming too long? Would you like to extract functionality into functions, modules, and packages that can be re-used and shared? Then this data talk is for you. A long notebook will be refactored and functionality will be extracted into a separate module that can be imported. It will also be demonstrated how to make your own package and how to debug with VS Code.

## Why?

Why would you want to improve your messy notebooks/scripts? 

* Easier to understand for yourself later
* Easier to understand for others (better collaboration)
* Extract common functionality and avoid re-doing the same basic processing every time
* From experiments to production

## Modular programming

Modular programming refers to the process of breaking a large, unwieldy programming task into separate, smaller, more manageable subtasks or **modules**. Individual modules can then be cobbled together like building blocks to create a larger application.

There are several advantages to modularizing code in a large application:

**Simplicity**: Rather than focusing on the entire problem at hand, a module typically focuses on one relatively small portion of the problem. If you’re working on a single module, you’ll have a smaller problem domain to wrap your head around. This makes development easier and less error-prone.

**Maintainability**: Modules are typically designed so that they enforce logical boundaries between different problem domains. If modules are written in a way that minimizes interdependency, there is decreased likelihood that modifications to a single module will have an impact on other parts of the program. (You may even be able to make changes to a module without having any knowledge of the application outside that module.) This makes it more viable for a team of many programmers to work collaboratively on a large application.

**Reusability**: Functionality defined in a single module can be easily reused (through an appropriately defined interface) by other parts of the application. This eliminates the need to duplicate code.

**Scoping**: Modules typically define a separate **namespace**, which helps avoid collisions between identifiers in different areas of a program. (One of the tenets in the Zen of Python is Namespaces are one honking great idea—let’s do more of those!)

**Functions**, **modules** and **packages** are all constructs in Python that promote code modularization.

## From messy notebook to library

* Step 0: [v0_messy_notebook.ipynb](v0_messy_notebook.ipynb)
* Step 1: [v1_notebook_with_loops_and_variables.ipynb](v1_notebook_with_loops_and_variables.ipynb)
* Step 2: [v2_notebook_with_functions.ipynb](v2_notebook_with_functions.ipynb)
* Step 3: [v3_notebook_using_module.ipynb](v3_notebook_using_module.ipynb)
* Step 4: [v4_notebook_using_module_other_folder.ipynb](v4_notebook_using_module_other_folder.ipynb)
* Step 5: [v5_notebook_using_package.ipynb](v5_notebook_using_package.ipynb)

## General advice

Below goes for *both* notebooks and scripts:

* Keep your notebook short 
* Give your notebook a descriptive and searchable name (possibly with a number indicating workflow order)
* Keep all import statements at the top of the notebook
* Organize your notebook in sections with headlines and text
* Avoid using absolute paths (if necessary then define a variable with the folder path at top of your notebook)
* Variables should be lower case (use underscore for long names)
* Use keyword arguments when calling function
* Replace magic numbers with constants
* Don't copy-paste lots of code (make a loop instead)
* Functions... 
    * should **do one thing only** 
    * should be small
    * should have few arguments
    * should have **no side effects**
    * should have a **docstring** 
    

## Modules and packages

* Module = a Python .py file (namespace)
* Package = a Python module which can contain submodules or recursively, subpackages. (Technically, a package is a Python module with an `__path__` attribute.)

### Where does Python look for modules? 

The import order is:

* Built-in python modules. You can see the list in the variable `sys.modules`.
* The `sys.path` entries.
* The installation-dependent default locations.

The `sys.path` contains: 

* The first entry is the FULL PATH TO THE DIRECTORY of the file which python (or current working directory if run in interactive mode)
* The other entries in `sys.path` are populated from the `PYTHONPATH` environment variable. Basically your global pip folders where your third-party python packages are installed. 

You can append to `sys.path` if you have a specific folder you would like to import modules from. But... consider if it would be better to create a package instead and install with pip. 


### What is the `__init__.py` for?

In a Python package, the file `__init__.py` can be empty, as long as it exists. It indicates that the directory should be regarded as a package. Of course, `__init__.py` can also set the appropriate content. 

If you have `setup.py` in your project and you use `find_packages()` within it, it is necessary to have an `__init__.py` file in every directory for packages to be automatically found.


## Useful resources 

* [Python modules and packages](https://realpython.com/python-modules-packages/)
* [Absolute vs relative imports](https://realpython.com/absolute-vs-relative-python-imports/)
* [Tutorial-convert-ml-experiment-to-production](https://docs.microsoft.com/en-us/azure/machine-learning/tutorial-convert-ml-experiment-to-production)
* [Clean code cheat sheet](https://cheatography.com/costemaxime/cheat-sheets/summary-of-clean-code-by-robert-c-martin/pdf/)