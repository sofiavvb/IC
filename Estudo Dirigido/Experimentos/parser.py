#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = [
#   "rich",
# ]
# ///

import csv
import json
import re
import sys
from pathlib import Path
from rich.console import Console

out = Console()

def parse_gurobi_log(file_path):
    """
    Parses Gurobi stdout.log for metrics.
    """
    metrics = {
        "best_bound": None,
        "best_objective": None,
        "gap": None,
        "nodes": 0,
        "simplex_iterations": 0,
        "root_time": None,
        "root_bound": None,
        "root_heu": None,
        "root_iterations": None,
        "status": "Timeout",
    }

    if not file_path.exists():
        return metrics

    # Regex patterns
    root_relax_pattern = re.compile(r"Root relaxation: objective ([+\-0-9.eE]+), (\d+) iterations, ([0-9\.]+) seconds")
    heuristic_pattern = re.compile(r"Found heuristic solution: objective ([+\-0-9.eE]+)")
    summary_explored_pattern = re.compile(r"Explored (\d+) nodes \((\d+) simplex iterations\) in ([0-9\.]+) seconds")
    final_bounds_pattern = re.compile(r"Best objective ([+\-0-9.eE]+), best bound ([+\-0-9.eE]+), gap ([0-9\.]+)%")

    root_section_passed = False
    last_heuristic_obj = None

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            
            # --- Root Node Parsing ---
            if not root_section_passed:
                h_match = heuristic_pattern.search(line)
                if h_match:
                    last_heuristic_obj = float(h_match.group(1))
            
            root_match = root_relax_pattern.search(line)
            if root_match:
                metrics["root_bound"] = float(root_match.group(1))
                metrics["root_iterations"] = int(root_match.group(2))
                metrics["root_time"] = float(root_match.group(3))
                metrics["root_heu"] = last_heuristic_obj
                root_section_passed = True
                continue

            # --- Final Summary Parsing (Success Case) ---
            expl_match = summary_explored_pattern.search(line)
            if expl_match:
                metrics["nodes"] = int(expl_match.group(1))
                metrics["simplex_iterations"] = int(expl_match.group(2))
                metrics["status"] = "Finished"
                continue

            bounds_match = final_bounds_pattern.search(line)
            if bounds_match:
                metrics["best_objective"] = float(bounds_match.group(1))
                metrics["best_bound"] = float(bounds_match.group(2))
                metrics["gap"] = float(bounds_match.group(3))
                continue

            # --- Table Row Parsing (Timeout/Running Case) ---
            if metrics["status"] == "Timeout" and line.endswith("s"):
                clean_line = re.sub(r"^[H\*]\s+", "", line)
                parts = clean_line.split()
                
                if len(parts) >= 8:
                    try:
                        metrics["nodes"] = int(parts[0])
                        gap_str = parts[-3].replace('%', '')
                        metrics["gap"] = float(gap_str) if gap_str != '-' else None
                        metrics["best_bound"] = float(parts[-4])
                        metrics["best_objective"] = float(parts[-5])
                    except (ValueError, IndexError):
                        pass

    return metrics

def parse_meta_file(file_path):
    """
    Parses meta.json for metadata.
    """
    data = {
        "instance_name": "Unknown",
        "wall_time_seconds": None,
        "depth": None
    }
    
    try:
        with open(file_path, "r") as f:
            meta = json.load(f)
            
        data["instance_name"] = meta.get("instance_name", "Unknown")
        data["wall_time_seconds"] = meta.get("wall_time_seconds", None)
        
        command = meta.get("command", "")
        depth_match = re.search(r"--depth\s+(\d+)", command)
        if depth_match:
            data["depth"] = int(depth_match.group(1))
        else:
            build_name = meta.get("build_name", "")
            build_match = re.search(r"depth[-_](\d+)", build_name)
            if build_match:
                 data["depth"] = int(build_match.group(1))

    except (FileNotFoundError, json.JSONDecodeError):
        pass
        
    return data

def process_single_folder(target_dir):
    """
    Processes a specific directory containing one stdout.log and meta.json.
    Writes res.csv inside that directory.
    """
    target_path = Path(target_dir)
    log_path = target_path / "stdout.log"
    meta_path = target_path / "meta.json"
    output_csv = target_path / "res.csv"

    if not log_path.exists() or not meta_path.exists():
        out.print(f"[red]Skipping {target_dir}: Missing stdout.log or meta.json[/red]")
        return

    # 1. Parse Data
    gurobi_data = parse_gurobi_log(log_path)
    meta_data = parse_meta_file(meta_path)
    
    # 2. Flatten Data
    row = {}
    row["Instance"] = meta_data["instance_name"]
    row["Time"] = meta_data["wall_time_seconds"]
    
    row["Best Bound"] = gurobi_data["best_bound"]
    row["Best Objective"] = gurobi_data["best_objective"]
    row["Gap"] = gurobi_data["gap"]
    
    row["Nodes"] = gurobi_data["nodes"]
    row["Simplex Iterations"] = gurobi_data["simplex_iterations"]
    row["Depth"] = meta_data["depth"]
    
    row["Root Time"] = gurobi_data["root_time"]
    row["Root Bound"] = gurobi_data["root_bound"]
    row["Root Obj"] = gurobi_data["root_heu"]
    row["Root Iterations"] = gurobi_data["root_iterations"]
    
    # 3. Write CSV
    fieldnames = list(row.keys())
    
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)
        
    out.print(f"[green]Parsed {target_dir} -> res.csv[/green]")

# --- Main Execution ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./parser.py <target_folder_path>")
        sys.exit(1)
        
    target_directory = sys.argv[1]
    process_single_folder(target_directory)