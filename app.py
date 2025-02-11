from flask import Flask, render_template
from portfolio_tracker import calculate_portfolio

app = Flask(__name__)

@app.route('/')
def index():
    portfolio_data = calculate_portfolio()
    return render_template('index.html', data=portfolio_data)

if __name__ == '__main__':
    app.run(debug=True) 