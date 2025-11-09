from flask import Flask, render_template, request, send_file, redirect, url_for, session
from ga_optimization import genetic_algorithm, simulate_plan, optimize_hyperparameters, evolutionary_hyperparameter_optimization
from yp import PRODUCTION_PLAN, draw_gantt_chart, gantt_data

app = Flask(__name__)
app.secret_key = 'yogurt-optimizer-secret-key-change-in-production'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/optimize", methods=["POST"])
def optimize():
    mode = request.form.get('mode', 'standard')
    
    best_config = None
    
    if mode == 'random':
        # Random search hyperparameter optimization
        num_trials = int(request.form.get('random_trials', 10))
        best_config = optimize_hyperparameters(num_trials)
        best_plan, best_time = genetic_algorithm(
            population_size=best_config['population_size'],
            generations=best_config['generations'],
            mutation_rate=best_config['mutation_rate'],
            verbose=False
        )
    elif mode == 'evolutionary':
        # Evolutionary hyperparameter optimization
        meta_pop = int(request.form.get('meta_population', 8))
        meta_gen = int(request.form.get('meta_generations', 4))
        best_config = evolutionary_hyperparameter_optimization(meta_pop, meta_gen)
        best_plan, best_time = genetic_algorithm(
            population_size=best_config['population_size'],
            generations=best_config['generations'],
            mutation_rate=best_config['mutation_rate'],
            verbose=False
        )
    else:
        # Standard mode with custom parameters
        population_size = int(request.form.get('population_size', 30))
        generations = int(request.form.get('generations', 300))
        mutation_rate = float(request.form.get('mutation_rate', 0.2))
        
        best_config = {
            'population_size': population_size,
            'generations': generations,
            'mutation_rate': mutation_rate
        }
        
        best_plan, best_time = genetic_algorithm(
            population_size=population_size,
            generations=generations,
            mutation_rate=mutation_rate,
            verbose=False
        )
    
    simulate_plan(best_plan)
    draw_gantt_chart()

    schedule = []
    for line, start, end, yogurt in gantt_data:
        schedule.append((yogurt, line, round(start, 2), round(end, 2)))

    session['schedule'] = schedule
    session['best_time'] = round(best_time, 2)
    session['config'] = best_config
    session['mode'] = mode
    
    return redirect(url_for('result'))

@app.route("/result")
def result():
    schedule = session.get('schedule', [])
    best_time = session.get('best_time', 0)
    config = session.get('config', {})
    mode = session.get('mode', 'standard')
    
    return render_template("result.html", 
                         schedule=schedule, 
                         best_time=best_time,
                         config=config,
                         mode=mode)

@app.route("/gantt")
def gantt():
    return send_file("gantt_chart.png", mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)