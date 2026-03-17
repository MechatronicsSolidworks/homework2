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

# ─────────────────────────────────────────────────────────────────────────────
# Part b) Draw root locus
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Part b)  Root Locus — Three Compensator Cases", fontsize=14, fontweight="bold")

for ax, (label, OL, T_total) in zip(axes, results):
    plt.sca(ax)

    # Compute root locus
    rlist, klist = control.root_locus(OL, plot=False)

    # Plot branches
    for branch in rlist.T:
        ax.plot(branch.real, branch.imag, 'b', linewidth=1.2)

    # Plot OL poles and zeros
    ol_poles = control.poles(OL)
    ol_zeros = control.zeros(OL)
    ax.plot(ol_poles.real, ol_poles.imag, 'rx', markersize=10, markeredgewidth=2, label="OL poles")
    if len(ol_zeros) > 0:
        ax.plot(ol_zeros.real, ol_zeros.imag, 'go', markersize=8, markeredgewidth=2, fillstyle='none', label="OL zeros")

    # Set axes limits to focus on the area of interest (fixes the scaling issue)
    ax.set_xlim([-50, 10])
    ax.set_ylim([-30, 30])

    # Formatting
    ax.axhline(0, color='k', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='k', linewidth=0.5, linestyle='--')
    ax.set_title(label, fontsize=11, fontweight='bold')
    ax.set_xlabel("Real Axis")
    ax.set_ylabel("Imaginary Axis")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.35)

plt.tight_layout()
plt.savefig("root_locus_fixed.png", dpi=150)
plt.show()