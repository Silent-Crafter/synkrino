from flask import Flask, request, redirect, url_for, render_template
from syn import scrape, headers

print(headers)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
def search():

    data = request.form.get("product")

    name = ["porsche", "audi", "supra", "nissan gtr", ""]

    cards = ""
    card = """
        <div class="w3-quarter w3-margin-top">
          <div class="w3-card-2">
            <div class="w3-container w3-blue">
                <p>{name}</p>
            </div>
            <div class="w3-container w3-grey">
                <p>{price}</p>
            </div>
          </div>
        </div>
    """

    amz_titles, amz_price = scrape(data)

    for titles, prices in zip(amz_titles, amz_price):
        cards += card.format(name=titles, price=prices)

    return render_template('search.html', card=cards)

if __name__ == '__main__':
    app.run()
