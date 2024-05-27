
import os
from skopt import gp_minimize
from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args
import subprocess

# Define base configuration
corpus = 'sgd'
mode = 'train'
epochs = 100
gpu = '0,1'  # default GPU setting
nclass = 37
batch_size_val = 2 # don't change this number
emb_batch = 0

# Prepare directory for results
results_dir = f'results_{corpus}'
os.makedirs(results_dir, exist_ok=True)

# Define the search space
space = [
    Integer(1, 2, name='nfinetune'),
    Integer(40, 300, name='chunk_size'),
    Real(1e-5, 5e-4, "log-uniform", name='lr'),
    Real(0.3, 0.7, name='dropout'),
    Categorical(['none', 'emb_cls', 'emb'], name='speaker_info'),
    Categorical(['none', 'emb_cls', 'emb'], name='topic_info')
]

# Objective function to minimize
@use_named_args(space)
def objective(**params):
    global index
    index += 1
    chunk_size = params['chunk_size']
    lr = params['lr']
    dropout = params['dropout']
    nfinetune = params['nfinetune']
    speaker_info = params['speaker_info']
    topic_info = params['topic_info']

    # Construct the output file name
    file_name = f"{results_dir}/{corpus}_{index}.txt"
    
    # Prepare command
    command = f"python -u engine.py --corpus={corpus} --mode={mode} --gpu={gpu} " \
              f"--batch_size_val={batch_size_val} --epochs={epochs} --lr={lr} --chunk_size={chunk_size} " \
              f"--dropout={dropout} --nfinetune={nfinetune} --speaker_info={speaker_info} " \
              f"--topic_info={topic_info} --nclass={nclass} --emb_batch={emb_batch} " \
              f"> {file_name}"

    with open(file_name, 'a') as f:
        f.write("\nAdditional information: ")
        f.write(f"Chunk size: {chunk_size}, Learning rate: {lr}, Dropout: {dropout}, Speaker info: {speaker_info}, Topic info: {topic_info}\n")

    # Execute command
    print(command)
    os.system(command)

    # Here, you should parse the output file or return a value directly from the engine.py script
    # For the sake of this example, we'll assume a dummy metric (e.g., accuracy)
    # In practice, you should extract the relevant metric from the output file
    dummy_metric = 1.0  # replace this with actual metric extraction logic

    return -dummy_metric  # we return negative because gp_minimize minimizes the objective

index = 0
# Run Bayesian Optimization
res = gp_minimize(objective, space, n_calls=50, random_state=42)

# Print best parameters and their corresponding score
print("Best score=%.4f" % res.fun)
print("Best parameters:")
print(res.x)