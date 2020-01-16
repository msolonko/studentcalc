# Student Calc

This project tested whether or not it is possible to predict student college acceptances to the nation's most selective colleges using neural networks. Despite college admissions being increasingly holistic, I achieved a ~73% accuracy on Tier 1 colleges and 98%+ on Tier 4 (based on acceptance rate).

The data collected was web-scraped from College Confidential using Beautiful Soup (data from last 5 years). Then, a Keras neural network was trained on the training set of the data and tested on the test set. Temporarily, this tool was up on my website but due to costs of running, I am publishing it here. It is a Flask application. 

The Github repo contains all the student data, the web scraping code, the URLs with the data, the neural network models with the scalers, and the code for the web application. I hope someone finds it useful!
