import os
import matplotlib.pyplot as plt
import numpy as np

# Automatically install 'control' library if not found
try:
    import control
except ImportError:
    os.system('pip install control')
    import control

# Your remaining code follows here...

# ─────────────────────────────────────────────────────────────────────────────
# Define plant blocks
# ─────────────────────────────────────────────────────────────────────────────
# G1 = 100 / (s + 20)
G1 = control.TransferFunction([100], [1, 20])

# G2 = 10 / (s * (s + 10))
G2 = control.TransferFunction([10], [1, 10, 0])

# ─────────────────────────────────────────────────────────────────────────────
# Define the three compensator cases
# ─────────────────────────────────────────────────────────────────────────────
Gc_cases = [
    ("Gc(s) = s",           control.TransferFunction([1, 0], [1])),         # Derivative
    ("Gc(s) = s^2",         control.TransferFunction([1, 0, 0], [1])),      # Double Derivative
    ("Gc(s) = s^2/(s+20)",  control.TransferFunction([1, 0, 0], [1, 20])), # Second-order Lead
]

# ─────────────────────────────────────────────────────────────────────────────
# Compute total closed-loop transfer function for each case
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 65)
print("  Part a)  Total (closed-loop) Transfer Functions")
print("=" * 65)

results = []   

for label, Gc in Gc_cases:
    # Inner feedback loop: T_inner = G2 / (1 + Gc * G2)
    T_inner = control.feedback(G2, Gc)

    # Outer open-loop: OL = G1 * T_inner
    OL = G1 * T_inner

    # Total closed-loop: T_total = OL / (1 + OL)
    T_total = control.feedback(OL, 1)

    # Simplify system (eliminate near pole-zero cancellations)
    T_total = control.minreal(T_total, tol=1e-6)
    results.append((label, OL, T_total))

    # Print results
    print(f"\n  ┌─ Case: {label}")
    print(f"  │  Total closed-loop T(s):")
    for line in str(T_total).splitlines():
        print(f"  │    {line}")
    poles = np.round(control.poles(T_total), 4)
    print(f"  │  Closed-loop poles : {poles}")
