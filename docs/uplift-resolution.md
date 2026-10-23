# Resolving the uplift — is "small positive Λ via uplift" valid?

Status: **draft under test** (two adversarial literature passes in flight, 2026-10-23).
The question is the single most contested step in the CC story: the KKLT anti-D3 uplift.

## The question

The CC distribution arc ended on: the flux discretuum is *locally flat* near zero (measured /
pinned), but the "small positive Λ" requires the **uplift** `Λ = −3|W₀|²/(8σ³) + D/σ³`, and the
anti-D3 uplift is **contested**. This doc resolves whether that uplift — or a controlled
alternative — actually survives, which decides whether "small Λ via uplift" is (a) valid,
(b) broken, or (c) unsettled.

## The attack side (no-gos / instabilities, as catalogued)

- Kachru–Pearson–Verlinde hep-th/0112197 — the anti-D3 "puffs up" into an NS5 (metastability).
- Moritz–Retolaza–Westphal arXiv:1707.08678 — anti-D3 singularity / no-go.
- Bena–Blåbäck–Graña–Lüst arXiv:2103.03250 — "Algorithmically solving the Tadpole Problem."
- Córdova–de Luca–Tomasiello arXiv:1812.04147 — backreaction.
- Dall'Agata–Emelin–Farakos–Morittu arXiv:2203.12636 — goldstino-condensation instability.
- Hebecker–Schreyer–Venken arXiv:2208.02826 — curvature corrections to KPV; no parametric control.

## The defense side — every no-go answered, concrete candidates exist (pass A verdict)

The debate has **shifted**: it is no longer "does a metastable dS minimum exist" but "is the
leading-order minimum *controlled* under higher-order corrections". Concrete explicit candidates
now exist and satisfy the tadpole:

- Crinò–Quevedo–Valandro 1906.05224 — explicit LVS dS vacua satisfying the tadpole.
- Demirtas–Kim–McAllister–Moritz[–Rios-Tascon] 2009.01275 / 2107.09064 — exponentially small W₀,
  answering the "Tadpole Problem" (2103.03250 is *example-specific, not a theorem*).
- **Schachner 2406.13751 / 2505.00149 (2025)** — full explicit CY orientifold, complete flux
  superpotential, string-tree Kähler potential to all orders in α′, one anti-D3, all moduli
  stabilized at leading order in α′ and g_s → metastable dS.

Each specific no-go has a specific answer: the goldstino "tachyon" (2203.12636) is traced to an
inconsistent low-energy superfield description (Kallosh–Linde–Wrase–Yamada 2206.04210); the KPV
polarization is the smooth resolution of the MRW singularity at leading order. **No fatal flaw has
yet been demonstrated in these candidates** — but "control" has not been demonstrated either.

## Alternatives and the dS swampland — every uplift fails the 10D control test (pass B verdict)

A 2022–2026 "control problem" wave has now hit **every** uplift mechanism:

| mechanism | 4D dS? | 10D controlled? | verdict |
|---|---|---|---|
| anti-D3 (KKLT) | yes | **no** | inherits the singularity/backreaction issues |
| D-term (BKQ hep-th/0309187) | yes | **no** | secretly an F-term (BDKVP 0405246) — not independent |
| LVS + anti-D3 (hep-th/0502058) | yes | **no** | controlled AdS, **not** dS (Junghans 2201.03572) |
| F-term / nilpotent goldstino (1507.07556) | yes | **no** | 4D-controlled, 10D control fails (HLSS 2512.17995) |
| T-brane (1512.04558) | yes | **no** | volume bound + warping never suppressed (Junghans 2609.35985) |
| classical dS / O-planes (2403.07065) | yes (tree) | contested | strongest counter-example (Andriot), backreaction disputed |

**dS swampland status:** the refined conjecture (1806.08362) is **not proven** (no derivation), is
**contradicted at the 4D level** by explicit dS SUGRA vacua, but is **strongly supported at the 10D
level** — the control problem has now hit every mechanism. DESI BAO (2404.03002, 2025) favors
time-varying dark energy (quintessence), shifting sentiment. De facto: **no controlled dS exists in
the weakly-coupled/weakly-curved regime** — still not a theorem, but no longer an open-ended hope.

## Bottom line — the uplift is unresolved, and that is the honest answer

The anti-D3/KPV uplift is **not broken and not controlled** — the debate has shifted from
*existence* to *control of corrections*. Concrete candidates now exist and satisfy the tadpole
(Crinò–Quevedo–Valandro 1906.05224; Demirtas et al. 2009.01275/2107.09064; Schachner 2406.13751 →
2505.00149), and each no-go has a specific answer — but **no side has won**; "controlled-ness" is
the live, well-posed open question, and it reduces to a **finite list of computable corrections**
(the α′² NS5 action, a backreacted 10d solution, the goldstino sector, all-orders stability) —
**not a conceptual wall**. So:

- **"small positive Λ via a controlled uplift" is (c) UNRESOLVED** — *conditional on control of
  corrections*, not a theorem (≈80% confidence the field state is "unsettled"; within that, the
  leading-order candidates are more likely consistent than not, but unproven);
- the **alternative uplifts** (D-term BKQ hep-th/0309187, LVS hep-th/0502058, F-term) each inherit
  or trade the same control question, and none is established as controlled;
- the **"anthropic selection"** on top is an **unresolved measure problem**, not a derivation.

**What this does to the CC story:** the "why this vacuum" arc ends, honestly, with *no selection
anywhere we can reach* — no exact selector (proven), no flux statistical selection (measured), and
no *established* cosmological selection (the uplift that would supply small Λ is unresolved). The
second pass sharpens the last point: with every uplift mechanism now hit by the 10D control
problem, the field is **trending hard toward "forbidden in the controllable regime"** — ~0.70 that
no controlled dS exists, ~0.30 that one survives — but there is still **no no-go theorem**. So the
small observed Λ is, at best, the anthropic tail of a locally-flat discretuum *gated by a mechanism
that every candidate fails to control*. That is the current, honest state: not a peak, not a proof,
and now leaning against the gate holding — with one decisive open question (is the control problem
generic?) and one closing move (a rigorous no-go, or a single controlled counter-example).

<!-- PASS A + PASS B verdicts (current 2024-2025 timeline + alternatives table) fold in here if they land -->

## Sources

KKLT hep-th/0301240 · LVS hep-th/0502058 · KPV hep-th/0112197 · BKQ hep-th/0309187 ·
Moritz–Retolaza–Westphal 1707.08678 · Córdova–de Luca–Tomasiello 1812.04147 ·
Dall'Agata–Emelin–Farakos–Morittu 2203.12636 · Hebecker–Schreyer–Venken 2208.02826 ·
Bena–Blåbäck–Graña–Lüst 2103.03250 · Obied–Ooguri–Spodyneiko–Vafa 1806.08362 ·
Garg–Krishnan 1807.05193 · Ooguri–Palti–Shiu–Vafa 1810.05506.
