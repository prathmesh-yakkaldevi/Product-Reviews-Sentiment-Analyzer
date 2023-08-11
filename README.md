<br/>
<p align="center">
  <h1 align="center">Product Reviews Sentiment Analyzer</h1>

  <p align="center">
    <a href="https://flipkartreview1.azurewebsites.net/">View Demo</a>
    .
    <a href="https://github.com/prathmesh-yakkaldevi/Product-Reviews-Sentiment-Analyzer/issues">Report Bug</a>
    .
    <a href="https://github.com/prathmesh-yakkaldevi/Product-Reviews-Sentiment-Analyzer/issues">Request Feature</a>
    <br>
A web application for analyzing the sentiment of product reviews from Flipkart.
  </p>
</p>

https://github.com/prathmesh-yakkaldevi/Product-Reviews-Sentiment-Analyzer/assets/62748359/3df4880e-3edc-45d3-b630-704e37d611c7

## Note
Promised features are located in the "update" branch. The "main" branch, which is solely used for hosting, will remain untouched by any merging from the update branch.

## Features

- Extracts and analyzes product reviews from Flipkart using BeautifulSoup (bs4) and NLTK.
- Performs sentiment analysis on the extracted reviews to determine positive, negative, or neutral sentiments.
- Generates a word cloud visualization to display the most frequent words in the reviews.
- Provides an intuitive user interface for inputting Flipkart product links.
- Deployed on Flask web framework for easy accessibility.





## Installation

1. Clone the repository:
```
git clone https://github.com/prathmesh-yakkaldevi/Product-Reviews-Sentiment-Analyzer.git
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Run the Flask application:
```
python app.py
```
## How to use
1. Open your web browser and navigate to `http://localhost:5000`.

2. Enter the Flipkart product link in the provided input field.
```
https://www.flipkart.com/durafit-mustang-6-hp-peak-dc-motorized-treadmill-free-installation-assistance/p/itm4a01f9221f62b?pid=TRDGDZH63HEM5QPZ&lid=LSTTRDGDZH63HEM5QPZ2CUFCP&marketplace=FLIPKART&store=qoc&srno=b_1_2&otracker=browse&fm=organic&iid=en_WPClllrUWvGhjEncaqY0ReQlsBwygoZlAbc9V9qGEFnCVUWnNWM7uHDEoNFpVq515YrvAymjlO9z4Nza-FHhBw%3D%3D&ppt=browse&ppn=browse&ssid=5pyb4ng0q80000001689239287764
```

3. Click the "Analyze" button to initiate the sentiment analysis process.

4. View the sentiment analysis results and the word cloud visualization.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.
