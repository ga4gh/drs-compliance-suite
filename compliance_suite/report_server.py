from flask import Flask, render_template
import os
import json

web_dir_path = os.path.join(os.path.dirname(__file__), 'web')
app = Flask(__name__,template_folder=web_dir_path+'/templates', static_folder=web_dir_path+'/static')

@app.route("/")
def index():
    with open((web_dir_path +"/temp_report.json"), "r") as f:
        report = json.load(f)
    return render_template("index.html", report=report)

def start_mock_server(port):
    # serves the output report as html webpage at http://127.0.0.1:<port>/
    app.run(port=port,debug=True)