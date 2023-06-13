from flask import Flask, request, redirect, url_for, render_template
from syn import scrape, headers
from time import sleep

print(headers)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
def search():

    data = request.form.get("product")

    cards = ""

    results = ""

    row = """
    <div class="w3-container" style="margin-top:20px;">
      <div class="w3-row-padding w3-padding-32 w3-center">
        {cols}
      </div>
    </div>
    """

    card = """
        <div class="w3-quarter w3-margin-top" style="padding-left: 32px; padding-right: 32px">
          <div class="w3-card-2 w3-hover-shadow">
            <a href="{l}" style="text-decoration: none">
              <div class="w3-display-container w3-lightgrey prod-image-container">
                  <img src="{i}" height="100%" class="w3-display-middle prod-image"/>
              </div>
              <div class="w3-container w3-blue prod-name">
                  <p>{n}</p>
              </div>
              <div class="w3-container w3-grey prod-price">
                  <p>{p}</p>
              </div>
              <div class="w3-container w3-red prod-service">
                  <p>{s}</p>
              </div>
            </a>
          </div>
        </div>

    """

    amz_titles, amz_price, amz_links, amz_images, flp_titles, flp_price, flp_links, flp_images = scrape(data)

    amazon = list(zip(amz_titles, amz_price, amz_links, amz_images))
    flipkart = list(zip(flp_titles, flp_price, flp_links, flp_images))

    amz_counter = 0
    flp_counter = 0

    col_counter = 0

    while amz_counter < len(amazon) or flp_counter < len(flipkart):
        try: at, ap, al, ai = amazon[amz_counter]
        except IndexError: at = ap = al = ""
        
        try: ft, fp, fl, fi = flipkart[flp_counter]
        except IndexError: ft = fp = fl = ""

        if at and ap and al: 
            cards += card.format(n=at, p=ap, l=al, i=ai, s="amazon")
            col_counter += 1
        amz_counter += 1

        if ft and fp and fl: 
            cards += card.format(n=ft, p=fp, l=fl, i=fi, s="flipkart")
            col_counter += 1
        flp_counter += 1

        if col_counter == 4:
            results += row.format(cols=cards)
            col_counter = 0
            cards = ""

    return render_template('search.html', card=results)

if __name__ == '__main__':
    app.run()
