@app.route("/prod/<ProductID>")
@login_required
def prod(ProductID):
    prod = products.query.get_or_404(ProductID)
    return render_template('prod.html', title=prod.NameOfProduct, prod=prod, now=datetime.utcnow())	