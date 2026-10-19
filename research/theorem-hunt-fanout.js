// theorem-hunt-fanout.js — the script BODY for the `workflow` tool (third fan-out).
//
// Six mathematical domains, each asked: what theorems (like Darboux) independently
// strengthen the constraint-first result ("only constraint + global topology survive")?
//
// Run with the `workflow` tool, meta = { name: "theorem-hunt-fanout", description: "..." },
// this file as `script`. To adapt: replace `directions` and tighten `schema`.
// `agent`, `parallel`, `schema` exist only inside the workflow runtime.

const directions = [
  { label: "Gromov non-squeezing / rigidity", prompt: "You are one of six researchers hunting for theorems that strengthen a physics result. Context (take as given): we proved the string flux landscape's only exact structure is its constraint (the D3 tadpole, via Weyl's FFT — Sp's only invariant), and we added Darboux's theorem (a symplectic form has NO local invariants) as a second, differential foundation. Together: no local fingerprint (Darboux) + no algebraic fingerprint (FFT) => the only surviving structure is global topology + the constraint. YOUR ANGLE: global symplectic topology / rigidity. Find the theorems that fill the POSITIVE side — what global invariants DO survive, making 'global topology' precise (Gromov's non-squeezing, symplectic capacities, Eliashberg-Gromov C^0 rigidity, Arnold conjecture). For each: exact statement, and how it sharpens 'the surviving structure is global topology' into a named theorem. Use web search. Return ONLY a JSON object with fields: direction, theorems_found (string), how_it_strengthens (string, 1-3 sentences), which_half (one of: local, global, algebraic, topological, counting, other), evidence (string, source URLs), confidence (low/medium/high), next_step (string)." },
  { label: "Atiyah-Singer index theorem", prompt: "You are one of six researchers hunting for theorems that strengthen a physics result. Context (take as given): we classify exact structure as constraints + labels (topology), with the SM's gauge group and N_gen=3 as 'labels' (topological data). YOUR ANGLE: index theory. Find the theorems that make 'labels are topological' rigorous: Atiyah-Singer index theorem (N_gen = index of the Dirac operator = |chi|/2), anomaly cancellation as the family index theorem. For each: exact statement, and how it turns 'labels = topological' from observation into theorem. Use web search. Return ONLY a JSON object with fields: direction, theorems_found (string), how_it_strengthens (string, 1-3 sentences), which_half (one of: local, global, algebraic, topological, counting, other), evidence (string, source URLs), confidence (low/medium/high), next_step (string)." },
  { label: "Morse theory / Milnor", prompt: "You are one of six researchers hunting for theorems that strengthen a physics result. Context (take as given): we claim 'no exact polynomial duality-invariant selector exists' — no local or algebraic exact fingerprint exists. YOUR ANGLE: Morse theory. Find the theorems relating the NUMBER/STRUCTURE of critical points (flux vacua) to global topology: Morse inequalities (m_k >= b_k), Milnor's Morse theory, Morse-Bott, Witten index, Ashok-Denef-Douglas index theorem. How does this sharpen or bound the 'search' claim — is the vacuum count itself a topological invariant, or only bounded by it? Use web search. Return ONLY a JSON object with fields: direction, theorems_found (string), how_it_strengthens (string, 1-3 sentences), which_half (one of: local, global, algebraic, topological, counting, other), evidence (string, source URLs), confidence (low/medium/high), next_step (string)." },
  { label: "Invariant theory (Molien/Hilbert)", prompt: "You are one of six researchers hunting for theorems that strengthen a physics result. Context (take as given): we proved the flux sector's only exact structure is the tadpole via Weyl's FFT, and computed the SM's 19 parameters as the orbit-space dimension of SU(3)^5 via Hilbert series. YOUR ANGLE: invariant theory. Find the general theorems that make the invariant-ring / orbit-space counting rigorous: Molien-Weyl formula, Hilbert-Serre theorem, Hilbert's finiteness theorem (reductive groups). For each: exact statement, and how it turns '19 = orbit-space dimension' and 'the tadpole generates C[N] (a polynomial ring in one generator)' into theorems. Use web search. Return ONLY a JSON object with fields: direction, theorems_found (string), how_it_strengthens (string, 1-3 sentences), which_half (one of: local, global, algebraic, topological, counting, other), evidence (string, source URLs), confidence (low/medium/high), next_step (string)." },
  { label: "K-theory / Bott periodicity", prompt: "You are one of six researchers hunting for theorems that strengthen a physics result. Context (take as given): we classify exact structure as constraints + labels, and listed D-brane charges as a 'constraint'. YOUR ANGLE: K-theory. Find the theorems making 'D-brane charges are constraints' rigorous: Witten's D-brane K-theory classification, Bott periodicity, Freed-Witten anomaly / twisted K-theory. How does this sharpen 'constraints = what the theory forbids' into a theorem — are D-brane charges a TOPOLOGICAL label (K(X) class), and is the tadpole 'total charge = 0 in K(X)'? Use web search. Return ONLY a JSON object with fields: direction, theorems_found (string), how_it_strengthens (string, 1-3 sentences), which_half (one of: local, global, algebraic, topological, counting, other), evidence (string, source URLs), confidence (low/medium/high), next_step (string)." },
  { label: "Symplectic reduction / moment maps", prompt: "You are one of six researchers hunting for theorems that strengthen a physics result. Context (take as given): the surviving structure after Darboux + FFT is global. YOUR ANGLE: symplectic reduction. Find the theorems about the GLOBAL structure of symplectic quotients: Marsden-Weinstein reduction, Atiyah-Guillemin-Sternberg convexity, Delzant classification, Duistermaat-Heckman localization, Kirwan surjectivity. How do these make 'the vacuum space is a symplectic quotient whose invariants are global' precise? Use web search. Return ONLY a JSON object with fields: direction, theorems_found (string), how_it_strengthens (string, 1-3 sentences), which_half (one of: local, global, algebraic, topological, counting, other), evidence (string, source URLs), confidence (low/medium/high), next_step (string)." }
];

const schema = {
  type: "object",
  properties: {
    direction: { type: "string" },
    theorems_found: { type: "string" },
    how_it_strengthens: { type: "string" },
    which_half: { type: "string", enum: ["local", "global", "algebraic", "topological", "counting", "other"] },
    evidence: { type: "string" },
    confidence: { type: "string", enum: ["low", "medium", "high"] },
    next_step: { type: "string" }
  },
  required: ["direction", "theorems_found", "how_it_strengthens", "which_half", "evidence", "confidence", "next_step"]
};

const results = await parallel(directions.map(d => () =>
  agent(d.prompt, { label: d.label, schema })
    .then(r => r ? { ...r, direction: d.label } : null)
));

return results.map((r, i) => r || {
  direction: directions[i].label, error: "failed", theorems_found: "", how_it_strengthens: "",
  which_half: "other", evidence: "", confidence: "low", next_step: ""
});
