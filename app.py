from flask import Flask, render_template, request, redirect
import pandas as pd
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

FILE = "expenses.csv"

if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Amount", "Category"])
    df.to_csv(FILE, index=False)


@app.route("/")
def home():
    df = pd.read_csv(FILE)

    total = df["Amount"].sum()

    records = df.to_dict(orient="records")

    category_data = df.groupby("Category")["Amount"].sum()

    if not category_data.empty:
        category_data.plot.pie(autopct='%1.1f%%')
        plt.ylabel("")
        plt.savefig("static/pie.png")
        plt.close()

    return render_template("index.html", total=total, records=records)


@app.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    category = request.form["category"]

    df = pd.read_csv(FILE)
    df.loc[len(df)] = [amount, category]
    df.to_csv(FILE, index=False)

    return redirect("/")

@app.route("/delete/<int:index>")
def delete(index):
    df = pd.read_csv(FILE)
    df = df.drop(index).reset_index(drop=True)
    df.to_csv(FILE, index=False)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)