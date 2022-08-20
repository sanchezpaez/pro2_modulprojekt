# pro2_modulprojekt_sanchezpaez

This is the repository for the PRO2 SoSe22 module project.

Installation and functionality description
=======================

1. Intro
-------

This directory contains an implementation of the BK Tree.

The program has three main parts, called from `main()`. It first takes the name of the word list from the command line, reads the list and builds a BK tree (`make_bktree_from_file()`), which is based on  the Levenshtein distance calculation. An example of the Levenshtein distance calculation is printed by default. Flags to show other string metrics (Damerau-Levenshtein or Hamming) are also available. At the end of this first phase, the status of the tree is printed out, indicating number of leaves and height.

The second phase (`make_graph_from_tree()`) is optional and depends on the number of leaves. When the list is of manageable size, the BK tree is transformed into a graph, which will be plotted.

Finally, the program goes on interactive mode (`interactive_mode_search_word()`) to allow the user to enter a word query, for which they will also need to specify the desired distance threshold. That means, for a word query 'car' and an edit distance of 1, words like 'cat', 'can' or 'bat', for example, would be matched.


The directory contains:

* `main.py`
* `file.py`
* `bk_tree.py`
* `graph.py`
* `exception.py`
* `vocabulary.py`
* `tests.py`
* `requirements.txt`
* `demo_words.txt`
* `words_nltk.txt`
* `words_2.pkl`
* `README.md`(this file)


2. Installation
-------

1) Clone the repository.

2) Using your terminal navigate through your computer to find the directory were you cloned the repository. Then from Terminal (look for 'Terminal' on Spotlight), or CMD for Windows,  set your working directory to that of your folder (for example: cd Desktop/pro2_modulprojekt_sanchezpaez).

3) Required packages:

* matplotlib==3.5.1
* networkx==2.8.4
* nltk==3.7
* numpy==1.21.5
* tqdm==4.64.0

If you don't have pip installed follow the installing instructions here: https://pip.pypa.io/en/stable/installation/

Run pip install -r requirements.txt (Python 2), or pip3 install -r requirements.txt (Python 3)


4) You should be able to run the script now. Check first how you can run python on your computer (it can be 'python' or 'python3').

For a mini-demo go to the command line and type the following:

```
python main.py demo_words.txt
```

You can use flags to show other string metrics, e.g. Damerau_Levenshtein distance Hamming distance:

```
python main.py demo_words.txt -dl -h
```

![Captura_de_pantalla_2022-08-20_a_las_19.24.08](https://gitup.uni-potsdam.de/sanchezpaez/pro2_modulprojekt_sanchezpaez/uploads/0fa1813d9724814170745f4f8e7eae3c/Captura_de_pantalla_2022-08-20_a_las_19.24.08.png)


For an extended demo you can use the nltk wordlist by typing this on the command line:

```
python main.py words_nltk.txt
```
Again, the same flags are available for other string metrics.
Note that when using large word lists, the visualisation part is not available, for it is imposible to represent a large tree on a normal-sized screen.

![bk_tree](https://gitup.uni-potsdam.de/sanchezpaez/pro2_modulprojekt_sanchezpaez/uploads/2431ed447285b18a8e3e6e0b2ee61b62/bk_tree.png)



In posterior calls of `main()`, it is possible to use the param loaded_tree (`loaded_tree=True`) to skip the `build_tree()` stage and load a pre_saved tree structure.


5) To run the tests:

All tests are in the `tests.py` file, and are organised in classes corresponding to the main classes in the program, including exception classes. They can be run all at once, individually or by class directly from Pycharm.


3. Contact information
-------

If you have any questions or problems during they installation process, feel free to email sandrasanchezp@hotmail.com

