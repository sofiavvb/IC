# run_all_experiments.py
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

DATASET_DIR = "datasets/categorical/"
OUTPUT_DIR = "experiments/"
DEPTHS = [2, 3, 4, 5]
TIME_LIMIT = 600  
MAX_WORKERS = 20

def run_single_experiment(depth, dataset_path):
    dataset_name = os.path.basename(dataset_path)
    logdir = os.path.join(OUTPUT_DIR, f"depth_{depth}")
    os.makedirs(logdir, exist_ok=True)

    cmd = [
        "python", "experiment_runner.py",
        "--depth", str(depth),
        "--dataset", dataset_path,
        "--logdir", logdir
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIME_LIMIT)
        status = "finished"
    except subprocess.TimeoutExpired as e:
        # Kill process if timeout reached
        status = "timeout"
        result = e  # to capture partial stdout/stderr

    return {
        "depth": depth,
        "dataset": dataset_name,
        "status": status,
        "stdout": getattr(result, "stdout", ""),
        "stderr": getattr(result, "stderr", ""),
        "returncode": getattr(result, "returncode", None),
    }

def main():
    datasets = [
        os.path.join(DATASET_DIR, f)
        for f in os.listdir(DATASET_DIR)
        if f.endswith(".csv")
    ]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(run_single_experiment, d, path)
                   for d in DEPTHS for path in datasets]

        for future in as_completed(futures):
            result = future.result()
            print(f"[{result['status']}] depth={result['depth']} dataset={result['dataset']}")
            results.append(result)

if __name__ == "__main__":
    main()
