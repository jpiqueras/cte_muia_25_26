
import re
import numpy as np

def read_fx_t(filepath):
    """
    Read ESATAN output file and extract FX and T values into numpy arrays.
    Skips nodes 99998 and 99999, but keeps others like 100 and 200.
    
    Parameters
    ----------
    filepath : str
        Path to the ESATAN output text file.
    
    Returns
    -------
    fx_array : np.ndarray
        Array of FX values.
    t_array : np.ndarray
        Array of T values.
    """
    
    # Regex: capture NODE, FX, T, QI
    pattern = re.compile(
        r'^\s*(\d+)\s+([+-]?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?)\s+([+-]?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?)\s+([+-]?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?)'
    )

    fx_vals = []
    t_vals = []

    with open(filepath, "r") as f:
        for line in f:
            m = pattern.match(line)
            if m:
                node = int(m.group(1))
                if node in (99998, 99999):
                    continue  # skip special nodes
                fx = float(m.group(2))
                t = float(m.group(3))
                fx_vals.append(fx)
                t_vals.append(t)

    return np.array(fx_vals), np.array(t_vals)

