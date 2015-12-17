## Ranking Stack Overflow Answers
*Carter Tiernan, Matt McNally*



### Directory Structure
----
1. **code**
   - This directory contains all the source code for the project and its split into two directories code/dist and code/src.

2. **code/dist**
    - This is the distribution files of our project, when they are run the tests we preformed and described in our report will be run.

3. **code/src**
   - This is where other source code written in earlier stages of development, or extra analysis not used in our project is stored.


### Files
---
#### code/dist
1. **data_analyzer.py**
   - This class functions to parse our dataset after it has been extracted from Posts.xlm (the original dataset). It populates our test and
  training sets with all the features that needed within our system but are not present within Posts.xml.
2. **db_tools.py**
   - This class acts as an API to connect to our database that holds the test and training data. It allows for connections to be made to
  the database as well initializes the tables if the database does not exists. It also has the functionality to add columns to the tables
  so new features can be added to the system.
3. **sentiment_tools.py**
   - This class preforms sentiment analysis on question and answer text using the library TextBlob. It returns two values, the text's
  subjective sentiment and objective sentiment scores.
4. **small_data_dumper.py**
   - This class parses Posts.xml (the original dataset) and extracts the questions and answers that will be analyzed, as well as any features
  used within the system that are present within Posts. It puts this data into a SQLite database for quick and easy information retrieval.
5. **stochastic_gradient_descent.py**
   - This class preforms the classification and calculates confidence scores of answers being a questions accepted answer. It does so using
  Scikit Learns Stochastic Gradient Descent Classifier.
6. **text_parser.py**
   - This text handles all text manipulation done within our system. Such manipulation includes the removal of html tags, extra white space
  and code from the bodies of questions and answers.

### Setting up the System
----
1. Install Python
   - https://www.python.org/downloads/
2. Install SQLite3
   - This is native to OSX
3. Install textblob
   - pip install textblob
4. Download the Stack Exchange Datadump
    - https://archive.org/details/stackexchange
5. Extract the Posts zip

### Running the System
----
1. Run small_data_dumper.py
2. Run data_analyzer.py
3. Run stochastic_gradient_descent.py
