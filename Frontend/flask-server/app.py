from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Image Storage"

# Recent Keys API
@app.route("/recentKeys")
def recentKeys():
    # generate key data
    return {"date":["2022-02-02", 
                    "2022-02-03", 
                    "2022-02-04", 
                    "2022-02-05",
                    "2022-02-06"],
                  "value": ["image1", 
                          "image2", 
                          "image3", 
                          "image4",
                          "image5"]}


@app.route("/allKeys")
def allKeys():
    # generate key data
    return {"date": ["2022-02-02", 
                     "2022-02-03", 
                     "2022-02-04", 
                     "2022-02-05",
                     "2022-02-06",
                     "2022-02-07", 
                     "2022-02-08", 
                     "2022-02-09", 
                     "2022-02-10",
                     "2022-02-11"],
                "value": ["image1", 
                        "image2", 
                        "image3", 
                        "image4",
                        "image5",
                        "image6", 
                        "image7", 
                        "image8", 
                        "image9",
                        "image10"]}

if __name__ == "__main__":
    app.run(port=5000, debug=True)