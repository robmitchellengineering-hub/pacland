"""The hTheta pairing sweep (rented-CPU job): lock the trace→Bessel vs heat-kernel separation across
β and lattice size. Usage: python3 scripts/hthe_pairing_sweep.py [--beta 1.0,1.5,2.0,2.5,3.0] [--N 6,8]"""
import argparse
from pacland import mass_gap_falsifiers as m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--beta", default="1.0,1.5,2.0,2.5,3.0")
    ap.add_argument("--N", default="6,8")
    ap.add_argument("--configs", type=int, default=20)
    ap.add_argument("--sweeps", type=int, default=12)
    args = ap.parse_args()
    betas = [float(b) for b in args.beta.split(",")]
    Ns = [int(n) for n in args.N.split(",")]
    print("beta,N,survives,evidence")
    for beta in betas:
        for N in Ns:
            ok, ev = m.verify_hthe_pairing(beta=beta, N=N, n_configs=args.configs, n_sweeps=args.sweeps)
            print(f"{beta},{N},{ok},{ev[:200]}")

if __name__ == "__main__":
    main()
