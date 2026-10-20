# Publication plan — the independent-researcher path to being checked

The goal is not "publish" first — it is **get the work in front of the people who can
check it**. Everything else (endorsement, arXiv, citation) follows from one expert saying
"yes, this is sound."

## The three-step path

1. **Make it citable now** — upload the 5-page paper to **Zenodo** (or OSF Preprints):
   free, no endorsement, no affiliation, mints a permanent DOI in minutes. This
   establishes priority and gives a citable link that isn't a GitHub URL.
2. **Email the people who can check it** — five named researchers whose work this builds
   on, each with a personalized three-sentence email (template below).
3. **Their "yes" is the endorsement** — the people on this list are arXiv endorsers by
   definition (they have published hep-th papers); one of them vouching is exactly the
   signal the arXiv gate is looking for.

## Why this can work

The work is **checkable**, which is the entire thing an endorser needs to be willing to
vouch: falsifiable claim + sympy symbolic proofs (zero tolerance) + Lean 4 kernel checks
(no axioms) + a public reproducible repo + it builds on named, citable papers. An expert
can verify the core theorem in an afternoon, not take it on faith.

## The contact list (from the research fan-out, 2026-10-20)

| person | affiliation | email | relevance | confidence |
|---|---|---|---|---|
| Sven Krippendorf | Cambridge DAMTP | `slk38@cam.ac.uk` | JAXVacua lead — the flux-vacua measurements run on his tool | high |
| Andreas Schachner | Cornell CLASSE | `as3475@cornell.edu` | JAXVacua co-author | high |
| Andreas Trautner | IST Lisbon (CFTP) | `andreas.trautner@tecnico.ulisboa.pt` | the "19 = orbit-space dimension" theorem is his (Bento–Silva–Trautner) | high |
| Michael R. Douglas | Harvard CMSA | `mdouglas@cmsa.fas.harvard.edu` | Denef–Douglas landscape statistics — the field's central figure | high |
| Abhishek Dubey | LMU Munich (former) | `Abhishek.Dubey@physik.uni-muenchen.de` | JAXVacua first author (email may be stale) | medium |

Send order: **Krippendorf → Trautner → Schachner → Douglas**, personalized, one at a
time (never a mass BCC). Hold Dubey until the others are tried.

## The email (personalize the bracketed parts)

```
Subject: your [JAXVacua framework / basis-invariant flavor puzzle / Denef–Douglas
distribution] and a machine-checked consequence of it

Dear Dr. [Name],

I'm an independent researcher. My work builds directly on your [paper], and I've
turned one of its consequences into a machine-checked theorem, which I'd value your
judgment on.

The claim: the D3 tadpole is the unique symplectic invariant of the flux pair (Weyl's
FFT at k=2), so the landscape's only exact structure is its constraint — and the
Standard Model's 19 free parameters form a real, not reducible, floor. It is verified
two independent ways: symbolically (sympy, zero tolerance) and in Lean 4
(kernel-checked, no axioms), and measured on real flux vacua.

Everything is reproducible:
github.com/robmitchellengineering-hub/pacland

If you have ten minutes to look at the short statement
(docs/constraint-first-theorem.md), I'd be grateful for a yes/no on whether it's sound.
If it holds, an arXiv endorsement would mean a great deal — but a comment on the
correctness is what I'm really asking for.

Thank you for your time,
Rob Mitchell
```

## What "working" looks like

- **Zenodo DOI minted** (priority secured).
- **One reply that says "this is correct/interesting"** — that single reply is the
  unlock: it becomes the endorsement, or the person who can point to the right endorser.
- **Then arXiv** via Route B (personal endorsement) — the repo's
  `docs/arxiv-submission.md` already has the submission steps.

## Honest caveats

- Cold email has a low response rate — five well-chosen, personalized, short emails over
  a week beat one long blast.
- Do not overclaim in the email; the paper already scopes itself ("no exact polynomial
  selector", not "search is dead"). Keep the email's claim to that.
- The Dubey address is medium-confidence and may bounce; it is last.
