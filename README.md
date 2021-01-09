# TwitterNLP

Chrome Extension that detects whether or not one of the trending topics are being received as positive or negative. The extension would analyze a combination of recent and popular tweets based on the trending topic to classify as either "Positive" or "Negative" and translate that to a percentage. The extension would change the color of the topic on twitter to a shade of either red or green depending on how positive or negative the tweet itself was. 

The NLP model was developed using a Multinomial Naive Bayes classifier (SKLearn), reaching a validation accuracy of roughly 80%. The Chrome Extension was developed using Java script and Python. Preprocessed data using, NLTK pandas, numpy and matplotlib (for visualization). Used dataset with over 1.6 million tweets found on Kaggle to train the model.  
