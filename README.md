# Villagers Tree

A python package to generate a tree visualization of Villagers cards.

## Author:
* Guillaume Cerutti (<guillaume.cerutti@gmail.com>)

## Installation

### Pre-requisite : Install conda

* Open a terminal window and type `conda`. If no error message appear (but a long how-to message) then you have successfully installed `conda`.

* Otherwise, you may choose to install either [the miniconda tool](https://docs.conda.io/en/latest/miniconda.html) or [the anaconda distribution](https://docs.anaconda.com/anaconda/install/) suitable for your OS.

### Download the source repository

#### Using the `git` command line tool

* Open a terminal window and navigate to the directory of your choice using the `cd` command.

* Copy the source repository using `git` by typing:

```
git clone https://github.com/gcerutti/villagers_tree.git
```

### Create a new conda environment

* In the terminal window, go to the directory where you copied the source repository:

```
cd villagers_tree
```

* Create a new environment containing all the script dependencies using the provided YAML file:

```
conda env create -f environment.yml
```

### Activate the conda environment

* To install the python package in the environment you just created, you need to activate it first.

```
conda activate villagers_tree
```

### Install the package

* Install the package contents.

```
python -m pip install -e .
```


## Usage

### Activate the conda environment

* Each time you open a nw terminal window to use the script, you will need to activate the environment you created to access the dependencies

```
conda activate villagers_tree
```

### Run the generation script


* To generate all Villagers cards separately, run the card generation script:

```
generate_villager_cards
```

> **NOTE:** the cards will be generated as separate `.png` files, under the `output/villager_cards` folder. 


