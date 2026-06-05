from flask import Flask

# Create Flask app
app = Flask(__name__)

# Test route (home page)
@app.route('/')
def home():
    return " Movie Mandala backend is Running!"

#Run Server
if __name__ == '__main__':
    app.run(debug=True)