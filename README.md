[![DOI](https://zenodo.org/badge/1219036051.svg)](https://doi.org/10.5281/zenodo.19709746)
# EnzyWizard-Flexibility


EnzyWizard-Flexibility is a command-line tool for estimating protein flexibility
from a cleaned protein structure and generating a detailed JSON report.
It computes per-residue root mean square fluctuation (RMSF) values using elastic
network models implemented in ProDy, including the Anisotropic Network Model (ANM)
and Gaussian Network Model (GNM). These models capture intrinsic protein dynamics
based on the topology of the structure and provide insight into residue mobility
and collective motions.


# Documentation index:

- example usage
- input parameters
- output files
- output report schema
- Process
- common errors and solutions
- dependencies
- references



# example usage:

The examples below use placeholder paths such as `path/to/input.cif` and
`path/to/output_dir/`; replace them with your own cleaned input structure file
and output directory.

Calculate residue RMSF values from a cleaned CIF file with default settings.
The default method is ANM, with a residue connection cutoff of 15.0 and 20
low-frequency modes.

```
enzywizard-flexibility -i path/to/input.cif -o path/to/output_dir/
```

Calculate residue RMSF values from a cleaned PDB file with default settings.

```
enzywizard-flexibility -i path/to/input.pdb -o path/to/output_dir/
```

Use GNM instead of ANM. GNM reports isotropic residue mobility and is useful when
only residue-level fluctuation magnitude is needed. ANM is the default and uses
an anisotropic elastic network model before the RMSF values are reported.

```
enzywizard-flexibility -i path/to/input.cif -o path/to/output_dir/ --method GNM
```

Use a smaller cutoff to build a sparser elastic network. This can emphasize more
local residue connections and may change RMSF values, especially in flexible or
weakly connected regions.

```
enzywizard-flexibility -i path/to/input.cif -o path/to/output_cutoff_10/ --cutoff 10.0
```

Use a larger cutoff to build a denser elastic network. This can include more
long-range residue connections and may smooth or reduce apparent local
fluctuations, but it can also increase computation time for larger proteins.

```
enzywizard-flexibility -i path/to/input.cif -o path/to/output_cutoff_20/ --cutoff 20.0
```

Use fewer low-frequency modes for a faster, more global-motion-focused report.
The requested number of modes is capped internally by the maximum available
number of modes for the selected model and protein size.

```
enzywizard-flexibility -i path/to/input.cif -o path/to/output_modes_5/ --n_modes 5
```

Use more low-frequency modes to include more motion components in the RMSF
calculation. This may change residue RMSF values and can increase runtime for
larger proteins.

```
enzywizard-flexibility -i path/to/input.cif -o path/to/output_modes_50/ --n_modes 50
```

Run the same cleaned structure with two model settings and save the reports into
separate output directories. Comparing the reports is useful for checking how
sensitive the flexibility profile is to the elastic network model and connection
cutoff.

```
enzywizard-flexibility -i path/to/input.cif -o path/to/output_anm_cutoff_15/ --method ANM --cutoff 15.0 --n_modes 20
enzywizard-flexibility -i path/to/input.cif -o path/to/output_gnm_cutoff_10/ --method GNM --cutoff 10.0 --n_modes 20
```



# input parameters:

-i, --input_path
Required.
Path to the input cleaned protein structure file.
Supported file extensions: .cif, .pdb.

-o, --output_dir
Required.
Path to the output directory for saving the JSON report.
The output directory is created automatically if it does not exist.

--method
Optional.
Method for RMSF calculation.
Supported values:
- ANM: Anisotropic Network Model
- GNM: Gaussian Network Model
Default: ANM.

--cutoff
Optional.
Distance cutoff for building the residue connection in ProDy.
Residues whose CA atoms are within this cutoff are considered connected.
This parameter controls the connectivity density of the elastic network.
Default: 15.0.
Must be a finite positive number.
A smaller cutoff gives a sparser network and may emphasize more local residue
connections. A larger cutoff gives a denser network, can include more long-range
connections, and may increase runtime for larger proteins.

--n_modes
Optional.
Number of low-frequency normal modes used for RMSF calculation.
These modes represent collective motions of the protein.
Default: 20.
Must be a positive integer.
The requested number of modes is capped internally by the maximum available
number of modes for the selected model and protein size.
Using fewer modes usually runs faster and focuses more on the largest-scale
global motions. Using more modes includes more motion components and may
increase runtime for larger proteins.


# output files:

The program outputs the following files into the output directory:

`{name}` is derived from the input file name without its extension.

1. A JSON report
   - flexibility_report_{name}.json
     - JSON report containing residue-level protein flexibility values.

2. A log file
   - log.txt
     - Processing log containing informational messages and errors.


# output report schema:

The JSON report contains the following fields:

- "report_type"
  - Data type: string
  - Expected value: "enzywizard_flexibility"
  - Description: The field "report_type" indicates the type of report ("report": http://purl.obolibrary.org/obo/IAO_0000088) generated by the EnzyWizard-Flexibility software.

- "protein_flexibility"
  - Data type: array
  - Description: The field "protein_flexibility" indicates protein flexibility ("protein flexibility": http://edamontology.org/operation_0244) calculated from the protein structure ("protein structure": http://edamontology.org/data_1537) and represented by residue root mean square fluctuation values ("root mean square fluctuation": https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html).

  Each item in "protein_flexibility" is an object containing:

  - "residue_index"
    - Data type: integer
    - Description: The field "residue_index" indicates the index ("index": http://purl.obolibrary.org/obo/NCIT_C25390) of the residue ("residue": http://purl.obolibrary.org/obo/GENO_0000782).

  - "residue_name"
    - Data type: string
    - Allowed values: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y.
    - Description: The field "residue_name" indicates the name of the residue ("residue": http://purl.obolibrary.org/obo/GENO_0000782), using one-letter code ("one-letter code": https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent.

  - "residue_root_mean_square_fluctuation"
    - Data type: number
    - Description: The field "residue_root_mean_square_fluctuation" indicates the root mean square fluctuation ("root mean square fluctuation": https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the residue ("residue": http://purl.obolibrary.org/obo/GENO_0000782). Unit: angstroms (Å) ("angstrom": http://qudt.org/vocab/unit/ANGSTROM).


# Process:

This command processes the input cleaned protein structure as follows:

1. Load the input structure
   - Read the cleaned CIF or PDB file using Biopython (Bio.PDB).
   - Resolve the protein name from the input filename.

2. Validate basic input conditions
   - Check that the input file exists.
   - Validate that the input structure satisfies the cleaned-structure requirement.

3. Extract structural information
   - Extract the single chain from the cleaned structure.
   - Retrieve all residues in chain order.
   - Extract CA atom coordinates for each residue.
   - Ensure sufficient residues are available for protein flexibility calculation.

4. Build elastic network model
   - Construct an elastic network model using ProDy based on the selected method:

     ANM (Anisotropic Network Model):
     - Builds a Hessian matrix from the CA-based elastic network.
     - Solves low-frequency normal modes.
     - Computes square fluctuations from these modes.
     - Converts square fluctuations into RMSF values.
     - Captures directional (anisotropic) motions of residues.

     GNM (Gaussian Network Model):
     - Builds a Kirchhoff matrix from the CA-based elastic network.
     - Solves low-frequency normal modes.
     - Computes square fluctuations from these modes.
     - Converts square fluctuations into RMSF values.
     - Captures isotropic residue mobility without directional information.

5. Calculate RMSF values
   - Convert square fluctuations into RMSF values by taking square roots.
   - Ensure consistency between residue count and RMSF results.

6. Assemble residue-level results
   - For each residue, record:
     - residue_index
     - residue_name
     - residue_root_mean_square_fluctuation

7. Save outputs
   - Generate and save a JSON report containing protein flexibility values.


# common errors and solutions:

- "Invalid cutoff"
  - Cause: The value passed to `--cutoff` is zero, negative, NaN, or infinite.
  - Solution: Use a finite positive number, such as `10.0`, `15.0`, or `20.0`.

- "Invalid n_modes"
  - Cause: The value passed to `--n_modes` is zero or negative.
  - Solution: Use a positive integer, such as `5`, `20`, or `50`.

- "argument --method: invalid choice"
  - Cause: The value passed to `--method` is not one of the supported RMSF methods.
  - Solution: Use `--method ANM` or `--method GNM`.

- "Input not found"
  - Cause: The path passed to `-i` or `--input_path` does not exist or is not a file.
  - Solution: Check the input file path and make sure it points to an existing cleaned CIF or PDB file.

- "Filename too long"
  - Cause: The input file name without extension is longer than the supported filename limit.
  - Solution: Rename the input file to a shorter name and run the command again.

- "Unsupported format"
  - Cause: The input file extension is not `.cif` or `.pdb`.
  - Solution: Use a supported cleaned structure file format.

- "Exception in loading structure"
  - Cause: Biopython could not parse the input file as a usable structure.
  - Solution: Check that the file is valid, non-empty, non-corrupted, and matches its file extension.

- "Structure must contain exactly one model. Please run 'enzywizard clean' first."
  - Cause: The input structure contains multiple models or no usable model.
  - Solution: Run the structure through `enzywizard-clean` first and use the cleaned output file.

- "Structure must contain exactly one chain. Please run 'enzywizard clean' first."
  - Cause: The input structure contains multiple chains or no usable chain.
  - Solution: Run the structure through `enzywizard-clean` first so it is converted to a single cleaned chain.

- "Cleaned structure must use chain ID 'A'. Please run 'enzywizard clean' first."
  - Cause: The input file is not in the cleaned single-chain format expected by EnzyWizard-Flexibility.
  - Solution: Use a cleaned output file generated by `enzywizard-clean`.

- "Residue numbering is not continuous"
  - Cause: The cleaned structure has missing or non-continuous residue numbering.
  - Solution: Run `enzywizard-clean` again and use its cleaned CIF or PDB output.

- "Missing backbone atom"
  - Cause: A required backbone atom is missing from a residue.
  - Solution: Clean and repair the structure with `enzywizard-clean` before running Flexibility.

- "At least 3 residues with CA atoms are required for RMSF calculation."
  - Cause: The cleaned structure has fewer than three residues with usable CA coordinates, so ProDy cannot build a meaningful elastic network for RMSF calculation.
  - Solution: Use a larger valid protein structure or check whether the input structure was truncated before cleaning.

- "Non-finite CA coordinates detected."
  - Cause: One or more CA coordinates are NaN or infinite.
  - Solution: Check the input structure for invalid coordinates and regenerate the cleaned input.

- "Failed to calculate RMSF by ProDy"
  - Cause: ProDy failed while building the elastic network or solving normal modes, often because of unsuitable coordinates, an extreme cutoff value, or an environment issue.
  - Solution: Review the detailed ProDy error in `log.txt`, check the cleaned structure, and try a standard cutoff such as `15.0`.

- "Non-finite RMSF values detected."
  - Cause: The RMSF calculation produced NaN or infinite values.
  - Solution: Check the cleaned input coordinates and rerun with standard parameters, such as `--method ANM --cutoff 15.0 --n_modes 20`.

- "Failed to write report JSON to"
  - Cause: The report could not be written to the output directory because of a filesystem, permission, or path problem.
  - Solution: Check that the `-o` output directory path is writable and that there is enough disk space.

- Cleaned structure validation failed
  - Cause: The input is not a cleaned single-chain protein structure, or it still contains heterogens, insertion codes, non-standard residues, missing atoms, unexpected atoms, invalid occupancies, or non-continuous numbering.
  - Solution: Review earlier messages in `log.txt`, run `enzywizard-clean`, and use the cleaned CIF or PDB output.

- Protein flexibility calculation failed
  - Cause: Residue extraction, CA coordinate extraction, ProDy model construction, normal-mode calculation, or RMSF assembly failed.
  - Solution: Review the specific error above this summary in `log.txt`, then check the cleaned structure and parameter values.

- Failed to generate flexibility report
  - Cause: The calculated RMSF values could not be converted into the report structure.
  - Solution: Review earlier calculation errors in `log.txt` and rerun after fixing the upstream problem.

- Output files are missing
  - Cause: The command failed before writing all outputs, or the output directory is not the directory passed to `-o`.
  - Solution: Check `log.txt`, confirm the `-o` output directory, and rerun after fixing earlier errors.

- Output file names are different from expected
  - Cause: Output names use `{name}`, which is derived from the input file name without its extension.
  - Solution: Check the input file name and look for files named `flexibility_report_{name}.json` and `log.txt`.


# dependencies:

- Biopython
- ProDy
- NumPy


# references:

- ProDy:
  https://prody.csb.pitt.edu/

- ProDy documentation:
  https://prody.csb.pitt.edu/manual/

- Elastic Network Models:
  Bahar et al., "Direct evaluation of thermal fluctuations in proteins using a single-parameter harmonic potential", Folding & Design (1997)
