This is to recommend books according to books already liked. As data source we used the book-crossing data set
(http://www2.informatik.uni-freiburg.de/~cziegler/BX/).

To run this program you need to download pandas and numpy libs.

There were some problems with reading the data from books.csv, so at first one has to run books_cleaner.py

The core of this program is divided into 2 parts:

- similarity_estimator.py

- books_recommender.py

and they must be run respectively.

In BX-CSV-Dump one finds all data which are used in this program. 

The books according to which we recommend are located in files tolkien_lotr.csv and frank_herbert_dune.csv

The results can be seen as a list of top 100 recommended books.
