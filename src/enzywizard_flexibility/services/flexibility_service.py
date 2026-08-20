from __future__ import annotations

import math
from pathlib import Path
from ..utils.logging_utils import Logger
from ..utils.IO_utils import file_exists, get_stem, check_filename_length, load_protein_structure
from ..algorithms.clean_algorithms import check_cleaned_structure
from ..algorithms.flexibility_algorithms import compute_protein_rmsf,generate_flexibility_report
from ..utils.IO_utils import write_json_from_dict_inline_leaf_lists
from ..utils.common_utils import get_optimized_filename


def run_flexibility_service(input_path: str | Path,output_dir: str | Path, cutoff: float = 15.0, n_modes: int = 20, method: str = "ANM") -> bool:
    # ---- logger ----
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger = Logger(output_dir)
    logger.print(f"[INFO] Flexibility processing started: {input_path}")

    # ---- check input ----
    if not math.isfinite(cutoff) or cutoff <= 0:
        logger.print(f"[ERROR] Invalid cutoff: {cutoff}. Must be a finite positive number.")
        return False

    if n_modes <= 0:
        logger.print(f"[ERROR] Invalid n_modes: {n_modes}. Must be a positive integer.")
        return False


    if not file_exists(input_path):
        logger.print(f"[ERROR] Input not found: {input_path}")
        return False

    # ---- get name ----
    name = get_stem(input_path)
    if not check_filename_length(name, logger):
        return False
    logger.print(f"[INFO] Protein name resolved: {name}")

    # ---- load structure ----
    structure = load_protein_structure(input_path, name, logger)
    if structure is None:
        logger.print(f"[ERROR] Failed to load structure: {input_path}")
        return False
    logger.print("[INFO] Structure loaded")

    #---- check structure ----
    if not check_cleaned_structure(structure, logger):
        logger.print("[ERROR] Cleaned structure validation failed")
        return False
    logger.print(f"[INFO] Structure checked")

    # ---- run algorithm ----
    logger.print("[INFO] Protein flexibility calculation started")
    protein_rmsf=compute_protein_rmsf(structure,logger,cutoff=cutoff,n_modes=n_modes,method=method)
    if protein_rmsf is None:
        logger.print("[ERROR] Protein flexibility calculation failed")
        return False

    # ---- generate report ----
    try:
        report = generate_flexibility_report(protein_rmsf=protein_rmsf)
    except Exception as e:
        logger.print(f"[ERROR] Failed to generate flexibility report: {e}")
        return False

    # ---- write output ----
    json_report_path = output_dir / get_optimized_filename(f"flexibility_report_{name}.json")
    try:
        write_json_from_dict_inline_leaf_lists(report, json_report_path)
    except Exception as e:
        logger.print(f"[ERROR] Failed to write report JSON to {json_report_path}: {e}")
        return False
    logger.print(f"[INFO] Report JSON saved: {json_report_path}")

    logger.print("[INFO] Flexibility processing finished")

    return True
