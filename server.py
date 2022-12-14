from typing import List, Tuple
from statistics import mean
import json
import os
import sys

import flwr as fl
from flwr.common import Metrics

# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m['accuracy'] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {'accuracy': sum(accuracies) / sum(examples)}

def post_fit(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    m = metrics[0][1]
    power_consumption = json.loads(str(m['power_consumption']))
    runtime = round(float(m['runtime']))
    frequency = str(m['frequency'])
    batch_size = str(m['batch_size'])
    mean_consumption = round(mean(power_consumption), 2)
    path = f'plotdata/{batch_size}.csv'
    with open(path, 'a') as f:
        if os.stat(path).st_size == 0:
            f.write('runtime,mean_consumption,frequency\n')
        f.write(f'{runtime},{mean_consumption},{frequency}\n')

# Define strategy
strategy = fl.server.strategy.FedAvg(
                min_fit_clients=1,
                min_evaluate_clients=1,
                min_available_clients=1,
                fit_metrics_aggregation_fn=post_fit,
                evaluate_metrics_aggregation_fn=weighted_average,
           )

# Start Flower server
fl.server.start_server(
    server_address=sys.argv[1],
    config=fl.server.ServerConfig(num_rounds=1),
    strategy=strategy,
)
