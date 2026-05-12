from __future__ import annotations
from argparse import Namespace,ArgumentParser
from ..services.flexibility_service import run_flexibility_service


def add_flexibility_parser(parser: ArgumentParser) -> None:
    parser.add_argument("-i", "--input_path", required=True, help="Path to the input cleaned protein structure file in CIF or PDB format.")
    parser.add_argument("-o", "--output_dir", required=True, help="Path to the output directory for saving the JSON report.")
    parser.add_argument("--method",type=str,choices=["ANM", "GNM"],default="ANM",help="Method for RMSF calculation: ANM or GNM (default: ANM).")
    parser.add_argument("--cutoff",type=float,default=15.0,help="Distance cutoff used to determine the residue connection in ProDy (default: 15.0).")
    parser.add_argument("--n_modes",type=int,default=20,help="Number of low-frequency normal modes used for RMSF calculation (default: 20).")

    parser.set_defaults(func=run_flexibility)

def run_flexibility(args: Namespace) -> None:
    run_flexibility_service(input_path=args.input_path,output_dir=args.output_dir,cutoff=args.cutoff,n_modes=args.n_modes,method=args.method)


