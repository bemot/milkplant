from flask import Flask, render_template, request, send_file, redirect, url_for, session
from ga_optimization import genetic_algorithm, simulate_plan
from yp import PRODUCTION_PLAN, draw_gantt_chart, gantt_data

app = Flask(__name__)
app.secret_key = 'yogurt-optimizer-secret-key-change-in-production'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/optimize", methods=["POST"])
def optimize():
    best_plan, best_time = genetic_algorithm()
    simulate_plan(best_plan)
    draw_gantt_chart()

    schedule = []
    for line, start, end, yogurt in gantt_data:
        schedule.append((yogurt, line, round(start, 2), round(end, 2)))

    session['schedule'] = schedule
    session['best_time'] = round(best_time, 2)
    
    return redirect(url_for('result'))

@app.route("/result")
def result():
    best_plan, best_time = genetic_algorithm()
    simulate_plan(best_plan)
    draw_gantt_chart()

    schedule = []
    for line, start, end, yogurt in gantt_data:
        schedule.append((yogurt, line, round(start, 2), round(end, 2)))
    
    return render_template("result.html", schedule=schedule, best_time=round(best_time, 2))

@app.route("/gantt")
def gantt():
    return send_file("gantt_chart.png", mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)