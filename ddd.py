from flask import Flask, request, jsonify, render_template_string
from sqlalchemy import create_engine, Column, Boolean, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class BooleanModel(Base):
    __tablename__ = 'boolean_model'
    id = Column(Integer, primary_key=True)
    flag = Column(Boolean, default=False)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cyberpunk Status Panel</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

            body {
                background: #000;
                color: #0f0;
                font-family: 'Orbitron', sans-serif;
                text-align: center;
                padding-top: 100px;
            }

            h1 {
                font-size: 2.5rem;
                text-shadow: 0 0 10px #0f0, 0 0 20px #0f0, 0 0 30px #00ff00;
            }

            #status {
                font-size: 3rem;
                font-weight: bold;
                display: block;
                margin: 20px auto;
                padding: 10px;
                width: 200px;
                border-radius: 10px;
                transition: all 0.3s ease-in-out;
            }

            .status-on {
                color: #00ff00;
                text-shadow: 0 0 15px #00ff00, 0 0 30px #00ff00;
            }

            .status-off {
                color: #ff0000;
                text-shadow: 0 0 15px #ff0000, 0 0 30px #ff0000;
            }

            button {
                font-size: 1.5rem;
                font-weight: bold;
                padding: 10px 30px;
                margin-top: 20px;
                background: transparent;
                border: 2px solid #0f0;
                color: #0f0;
                border-radius: 8px;
                cursor: pointer;
                text-shadow: 0 0 5px #0f0, 0 0 10px #0f0;
                transition: all 0.3s ease-in-out;
            }

            button:hover {
                background: #0f0;
                color: #000;
                box-shadow: 0 0 15px #00ff00, 0 0 30px #00ff00;
            }
        </style>
        <script>
            function fetchStatus() {
                fetch('/status')
                    .then(response => response.json())
                    .then(data => {
                        let statusElement = document.getElementById('status');
                        if (data.status) {
                            statusElement.innerText = 'ONLINE';
                            statusElement.classList.add('status-on');
                            statusElement.classList.remove('status-off');
                        } else {
                            statusElement.innerText = 'OFFLINE';
                            statusElement.classList.add('status-off');
                            statusElement.classList.remove('status-on');
                        }
                    });
            }

            function changeStatus() {
                fetch('/change_status', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        let statusElement = document.getElementById('status');
                        if (data.status) {
                            statusElement.innerText = 'ONLINE';
                            statusElement.classList.add('status-on');
                            statusElement.classList.remove('status-off');
                        } else {
                            statusElement.innerText = 'OFFLINE';
                            statusElement.classList.add('status-off');
                            statusElement.classList.remove('status-on');
                        }
                    });
            }

            window.onload = fetchStatus;
        </script>
    </head>
    <body>
        <h1>Myhome Status Panel</h1>
        <span id="status">Loading...</span>
        <button onclick="changeStatus()">Toggle Status</button>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/status', methods=['GET'])
def get_status():
    status_record = session.query(BooleanModel).first()
    return jsonify({"status": status_record.flag if status_record else False})

@app.route('/change_status', methods=['POST'])
def change_status():
    status_record = session.query(BooleanModel).first()
    if status_record:
        status_record.flag = not status_record.flag
    else:
        status_record = BooleanModel(flag=True)
        session.add(status_record)

    session.commit()
    return jsonify({"status": status_record.flag})

if __name__ == '__main__':
    import sys
    try:
        app.run(debug=True)
    except SystemExit:
        sys.exit(0)
