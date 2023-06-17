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

    cols = ""

    results = ""

    row = """
    <div class="w3-row w3-grayscale" style="margin-bottom: 20px;">
      {cols}
    </div>
    """

    item = """
    <div class="w3-col l3 s6" style="padding: 2px">
      <div class="w3-container">
        <div class="w3-display-container">
          <img src="{i}">
          <div class="w3-display-middle w3-display-hover">
            <a href="{l}" class="w3-button w3-black" target="_blank">Buy now <i class="fa fa-shopping-cart"></i></a>
          </div>
        </div>
        <p>{n}<br><b>{p}</b><br><span class="w3-small w3-text-grey">{s}</span></p>
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
            cols += item.format(n=at, p=ap, l=al, i=ai, s="amazon")
            col_counter += 1
        amz_counter += 1

        if ft and fp and fl: 
            cols += item.format(n=ft, p=fp, l=fl, i=fi, s="flipkart")
            col_counter += 1
        flp_counter += 1

        if col_counter == 4:
            results += row.format(cols=cols)
            col_counter = 0
            cols = ""

    return render_template('search.html', card=results)

if __name__ == '__main__':
    app.run()
