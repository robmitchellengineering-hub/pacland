// floor-fanout.js — the script BODY for the `workflow` tool (second research fan-out).
//
// Five independent angles on: "what is the minimum number of free parameters any
// consistent UV completion of the SM can reach?" (the 'floor' question that the first
// fan-out's refinement named).
//
// Run it with the `workflow` tool, meta = { name: "sm-floor-fanout", description: "..." },
// and this file as `script`. To adapt: replace `directions` and tighten `schema`.
// `agent`, `parallel`, `schema` exist only inside the workflow runtime.

const directions = [
  { label: "GUT ladder", prompt: "You are one of five researchers attacking a single physics question for a synthesis. Context (take as given): we proved the flux sector's minimum free-parameter count ('floor') is 1 (the D3 tadpole is the unique invariant). For the SM the 19 parameters are the orbit-space dimension of the flavor/reparametrization group — the independent flavor invariants. The question under attack: WHAT IS THE MINIMUM number of free parameters any consistent ultraviolet completion of the SM can reach — is there a lower bound? YOUR ANGLE: the grand-unification ladder. Enumerate SU(5), SO(10), E6, Pati-Salam, trinification and determine how many free parameters each leaves (how far the orbit-space dimension drops below 19). Is there a lowest? Does the ladder suggest a floor, or just shuffle parameters (SUSY adding ~105 soft terms)? Use web search. Return ONLY a JSON object with fields: direction, claim (1-3 sentences), floor_estimate (string, e.g. '16', '~10', 'unknown'), evidence (with source URLs), confidence (low/medium/high), open_questions, next_step." },
  { label: "String theory floor", prompt: "You are one of five researchers attacking a single physics question for a synthesis. Context (take as given): flux sector floor = 1 (the tadpole). SM has 19 free parameters (the independent flavor invariants). Question: what is the MINIMUM number of free parameters any consistent UV completion of the SM can reach? YOUR ANGLE: string compactifications. What is the minimum free-parameter count in KNOWN string constructions — do moduli (dilaton, Kahler, complex-structure) admit a lower bound, or can they be driven to zero by flux? Are there fully moduli-stabilized vacua, and how many continuous parameters do they leave? Use web search (KKLT, LVS, IIA flux vacua). Return ONLY a JSON object with fields: direction, claim, floor_estimate (string), evidence (with source URLs), confidence, open_questions, next_step." },
  { label: "Swampland floor", prompt: "You are one of five researchers attacking a single physics question for a synthesis. Context (take as given): flux floor = 1 (tadpole); SM has 19 free parameters. Question: what is the MINIMUM number of free parameters any consistent UV completion can reach? YOUR ANGLE: swampland constraints. Do the swampland conjectures (no global symmetries, Weak Gravity, distance, tadpole, species) FORCE a minimum number of free parameters? Does 'no global symmetries' forbid a zero-parameter theory? Does the WGC forbid the g->0 decoupling limit? Use web search. Return ONLY a JSON object with fields: direction, claim, floor_estimate (string), evidence (with source URLs), confidence, open_questions, next_step." },
  { label: "Mathematical floor", prompt: "You are one of five researchers attacking a single physics question for a synthesis. Context (take as given): the SM's 19 parameters are the orbit-space dimension of the flavor group SU(3)^5 on the Yukawa matrices. Question: what is the MINIMUM number of free parameters any consistent UV completion can reach? YOUR ANGLE: the mathematical/invariant-theory lower bound. Is there a representation-theory or invariant-theory FLOOR on the number of free parameters (rank of the gauge group, coset dimension, syzygy count)? What is the mathematical obstruction to a zero- or one-parameter ToE? Use web search (Hilbert series, Molien-Weyl, parameter counting). Return ONLY a JSON object with fields: direction, claim, floor_estimate (string), evidence (with source URLs), confidence, open_questions, next_step." },
  { label: "Flux-sector lesson", prompt: "You are one of five researchers attacking a single physics question for a synthesis. Context (take as given): the flux sector's floor is 1 because a duality group Sp(b3) with the First Fundamental Theorem collapses the orbit space to one invariant (the tadpole). The SM's flavor group SU(3)^5 has an orbit space of dimension 19. Question: what is the MINIMUM number of free parameters any consistent UV completion can reach? YOUR ANGLE: generalize the flux-sector lesson. What MECHANISM drove the flux floor to 1, and does it generalize to the SM? Is SU(3)^5 a duality or merely a reparametrization group, and does its invariant ring (19 generators) preclude a collapse to 1? Use web search (duality groups, flavor invariant rings, FFT). Return ONLY a JSON object with fields: direction, claim, floor_estimate (string), evidence (with source URLs), confidence, open_questions, next_step." }
];

const schema = {
  type: "object",
  properties: {
    direction: { type: "string" },
    claim: { type: "string" },
    floor_estimate: { type: "string" },
    evidence: { type: "string" },
    confidence: { type: "string", enum: ["low", "medium", "high"] },
    open_questions: { type: "string" },
    next_step: { type: "string" }
  },
  required: ["direction", "claim", "floor_estimate", "evidence", "confidence", "open_questions", "next_step"]
};

const results = await parallel(directions.map(d => () =>
  agent(d.prompt, { label: d.label, schema })
    .then(r => r ? { ...r, direction: d.label } : null)
));

return results.map((r, i) => r || {
  direction: directions[i].label, error: "failed", claim: "", floor_estimate: "unknown",
  evidence: "", confidence: "low", open_questions: "", next_step: ""
});
