# pro2_modulprojekt_sanchezpaez

This is the repository for the PRO2 SoSe22 module project.

Installation and functionality description
=======================

1. Intro
-------

This directory contains an implementation of the BK Tree. BK Trees are often used to perform spell checks based on Levenshtein distance and autocorrect functions.

The program has three main parts, called from `main()`. It first takes the name of the word list from the command line, reads the list and builds a BK tree (`make_bktree_from_file()`), which is by default based on  the Levenshtein distance calculation. An example of the Levenshtein distance calculation is printed. Flags to use another string metric (Damerau-Levenshtein) tu build the tree, to load a pre-saved tree, or to visualise the built tree are also available. At the end of this first phase, the status of the tree is printed out, indicating number of leaves and height.

The second phase (`make_graph_from_tree()`) is optional and can be selected by the user. When the list is of manageable size, the BK tree will be plotted.

Finally, the program goes on interactive mode (`interactive_mode_search_word()`) to allow the user to enter a word query, for which they will also need to specify the desired distance threshold. That means, for a word query 'car' and an edit distance of 1, words like 'cat', 'can' or 'bat', for example, would be matched. The user can exit the program by hitting 'enter'.


The directory contains:

* `main.py`
* classes (folder)
* `vocabulary.py`
* tests (folder)
* `requirements.txt`
* `demo_words.txt`
* `README.md`(this file)
* .gitignore


2. Installation and use
-------

1) Clone the repository.

2) Using your terminal navigate through your computer to find the directory where you cloned the repository. Then from Terminal (look for 'Terminal' on Spotlight), or CMD for Windows,  set your working directory to that of your folder (for example: cd Desktop/pro2_modulprojekt_sanchezpaez-main).

3) Required packages:

* matplotlib==3.5.1
* networkx==2.8.4
* nltk==3.7
* numpy==1.21.5
* tqdm==4.64.0
* pydot==1.4.2
* graphviz==0.20.1


If you don't have pip installed follow the installing instructions here: https://pip.pypa.io/en/stable/installation/

Run pip install -r requirements.txt or pip3 install -r requirements.txt. The Python version you need is 3.9 or above.

Make sure graphviz is correctly installed before executing the program, or else it will fail. How to do so may depend on you OS. Have a look here: https://pypi.org/project/graphviz/. Creating a virtual environment to run the program is an option.


4) You should be able to run the script now. Check first how you can run python on your computer (it can be 'python' or 'python3'). 

For a mini-demo go to the command line and type the following:

```
python main.py demo_words.txt
```

You can use flags to:

* Build the tree using Damerau_Levenshtein distance:

```
python main.py demo_words.txt -dl
```


* Load a pre-saved tree (note: you should have run the program first to be generate that tree):

```
python main.py demo_words.txt -t
```

* Visualise the plotted tree:

```
python main.py demo_words.txt -v
```

To use the nltk wordlist instead type this on the command line:

```
python main.py words_nltk.txt
```
Again, the same flags are available.
Note that when using large word lists, the visualisation part is not recommnended, for it is imposible to represent a large tree on a normal-sized screen.

![bk_tree](https://gitup.uni-potsdam.de/sanchezpaez/pro2_modulprojekt_sanchezpaez/uploads/2431ed447285b18a8e3e6e0b2ee61b62/bk_tree.png)



5) To run the tests:

All tests are in the `tests.py` file, and are organised in classes corresponding to the main classes in the program, including exception classes. They can be run all at once, individually or by class directly from Pycharm.


3. Contact information
-------

If you have any questions or problems during they installation process, feel free to email sandrasanchezp@hotmail.com

