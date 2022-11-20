from typing import List, Tuple
import json

import flwr as fl
from flwr.common import Metrics

# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m['accuracy'] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {'accuracy': sum(accuracies) / sum(examples)}

def fit_metrics_aggregation(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    print('==========\nfit_round metrics:')
    for key, value in metrics[0][1].items():
        value_deserialized = json.loads(str(value))
        print(f'\t{key}: {value_deserialized}')
    print('==========')

# Define strategy
strategy = fl.server.strategy.FedAvg(
                min_fit_clients=1,
                min_evaluate_clients=1,
                min_available_clients=1,
                fit_metrics_aggregation_fn=fit_metrics_aggregation,
                evaluate_metrics_aggregation_fn=weighted_average,
           )

# Start Flower server
fl.server.start_server(
    server_address='192.168.2.214:31415',
    config=fl.server.ServerConfig(num_rounds=1),
    strategy=strategy,
)
