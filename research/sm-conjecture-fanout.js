// sm-conjecture-fanout.js — the script BODY for the `workflow` tool.
//
// This is the reusable "research fan-out" for the constraint-first SM conjecture.
// It fans out N independent angles to N agents in parallel, each returning a
// structured verdict, and aggregates them for a compare-notes synthesis.
//
// To run it: call the `workflow` tool with
//   meta = { name: "sm-conjecture-fanout",
//            description: "Five-way parallel research on whether the SM's 19
//                          parameters are unpredicable in any UV completion" }
// and this file's contents as the `script` parameter.
//
// To adapt it to a NEW research question: replace `directions` (the label + a
// self-contained prompt per angle) and, if needed, tighten the `schema`. The
// `parallel(...)` fan-out and the aggregation stay unchanged.
//
// NOTE: `agent`, `parallel`, and `schema` are workflow-tool hooks — they exist
// only inside the workflow runtime, not in plain Node.

const directions = [
  {
    label: "GUT unification",
    prompt: "You are one of five researchers analyzing a single physics question for a synthesis. Context (take as given, do not re-derive): we proved the string flux landscape's only exact structure is its constraint (the D3 tadpole), and we CONJECTURE that the Standard Model's ~19 free parameters (3 gauge couplings, 9 masses, 4 CKM, 2 Higgs, 1 theta_QCD) are 'unpredicable in any UV completion' — i.e. no theory-of-everything can derive them, because there is no invariant for them to be a function of. YOUR ANGLE: grand unification. Research and report: (a) does SU(5)/SO(10) grand unification RELATE or PREDICT any of the 19 parameters — gauge coupling unification, Yukawa/mass relations like b-tau unification? (b) are these genuine predictions or post-hoc fits / label choices? (c) if a GUT predicts a relation among the parameters, does that FALSIFY the 'unpredicable' conjecture? Use web search to check current status. Return ONLY a JSON object with fields: direction, claim (1-3 sentences), evidence (specific facts with source URLs), confidence (low/medium/high), falsifies_conjecture (true/false/unknown), open_questions, next_step."
  },
  {
    label: "String constructions",
    prompt: "You are one of five researchers analyzing a single physics question for a synthesis. Context (take as given): we proved the string flux landscape's only exact structure is its constraint (the D3 tadpole), and we CONJECTURE the SM's ~19 free parameters are 'unpredicable in any UV completion'. YOUR ANGLE: string compactifications. Research and report: in KNOWN string constructions (heterotic Calabi-Yau, F-theory GUTs, intersecting D-brane models), do any of the 19 parameters get PREDICTED or RELATED by geometry, flux, or bundle data? Are Yukawa couplings computed from geometry, gauge couplings set by moduli vevs? Survey what string theory actually CONSTRAINS vs leaves free. Use web search for concrete examples. Return ONLY a JSON object with fields: direction, claim, evidence (with source URLs), confidence (low/medium/high), falsifies_conjecture (true/false/unknown), open_questions, next_step."
  },
  {
    label: "Invariant-theory analog",
    prompt: "You are one of five researchers analyzing a single physics question for a synthesis. Context (take as given): the flux-sector uniqueness theorem was provable because flux has a duality group Sp(b3) and Weyl's First Fundamental Theorem gives a COMPLETE invariant classification (everything is a function of the tadpole). We CONJECTURE the SM's ~19 free parameters are 'unpredicable in any UV completion'. YOUR ANGLE: the invariant-theory analog. Research and report: does the SM admit an analogous invariant-theory classification? What is the right GROUP ACTION under which the 19 parameters are invariants (gauge group, flavor, RG flow, conformal structure)? Is there a known First-Fundamental-Theorem-style result proving 'no invariant fixes the parameters'? Use web search for invariant theory of the SM, flavor symmetry, naturalness reformulations. Return ONLY a JSON object with fields: direction, claim, evidence (with source URLs), confidence (low/medium/high), falsifies_conjecture (true/false/unknown), open_questions, next_step."
  },
  {
    label: "Swampland constraints",
    prompt: "You are one of five researchers analyzing a single physics question for a synthesis. Context (take as given): we proved the string flux landscape's only exact structure is its constraint (the D3 tadpole), and we CONJECTURE the SM's ~19 free parameters are 'unpredicable in any UV completion'. YOUR ANGLE: swampland conjectures. Research and report: do the swampland conjectures (Weak Gravity, distance, de Sitter, species) CONSTRAIN or PREDICT any of the 19 parameters? Are there sharp predictions or only order-of-magnitude consistency bounds? Use web search for swampland bounds on SM parameters. Return ONLY a JSON object with fields: direction, claim, evidence (with source URLs), confidence (low/medium/high), falsifies_conjecture (true/false/unknown), open_questions, next_step."
  },
  {
    label: "Lambda angle",
    prompt: "You are one of five researchers analyzing a single physics question for a synthesis. Context (take as given): we classify exact structure into CONSTRAINTS (what consistency forbids), LABELS (topological/geometric choices), and PARAMETERS (free inputs, unpredicable). We CONJECTURE the SM's ~19 free parameters are unpredicable in any UV completion. YOUR ANGLE: the cosmological constant Lambda. Research and report: is Lambda a PARAMETER, a CONSTRAINT, or a LABEL? Is its smallness a prediction (anthropic/selection), a constraint (swampland/de Sitter), or a free parameter? Use web search for the current status. Return ONLY a JSON object with fields: direction, claim, evidence (with source URLs), confidence (low/medium/high), falsifies_conjecture (true/false/unknown — does Lambda's status bear on whether parameters are unpredicable?), open_questions, next_step."
  }
];

const schema = {
  type: "object",
  properties: {
    direction: { type: "string" },
    claim: { type: "string" },
    evidence: { type: "string" },
    confidence: { type: "string", enum: ["low", "medium", "high"] },
    falsifies_conjecture: { type: "string", enum: ["true", "false", "unknown"] },
    open_questions: { type: "string" },
    next_step: { type: "string" }
  },
  required: ["direction", "claim", "evidence", "confidence", "falsifies_conjecture", "open_questions", "next_step"]
};

const results = await parallel(directions.map(d => () =>
  agent(d.prompt, { label: d.label, schema })
    .then(r => r ? { ...r, direction: d.label } : null)
));

return results.map((r, i) => r || {
  direction: directions[i].label, error: "failed", claim: "", evidence: "",
  confidence: "low", falsifies_conjecture: "unknown", open_questions: "", next_step: ""
});
