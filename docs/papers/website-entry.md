# Website entry (for pacland.morpheus.nz / verify.html) — insert when the DOIs land

Add a "proof arm" row/section to `web/verify.html`'s theorem tower, next to the five landscape
theorems. Placeholder `10.5281/zenodo.24024627` / `10.5281/zenodo.24024631` to be filled from the Zenodo upload.

```html
<h3>The proof arm (machine-checked, Lean 4)</h3>
<p class="headline">The Born rule and the Standard Model's exact structure are kernel-checked:
Gleason's theorem (Cooke-Keane-Moran route, no continuity) and the SM gauge-sector uniqueness.
The referee is the Lean kernel; it does not care about credentials.</p>
<table class='battery'><thead><tr><th>proof</th><th>claim</th><th>certificate</th></tr></thead><tbody>
<tr><td>Gleason (Born rule)</td><td>non-contextual probability on projectors is Tr(ρP)</td>
<td class='st'><span class='pill ok'>Gleason.frameFunction_regular</span> — <a href="https://doi.org/10.5281/zenodo.24024627">10.5281/zenodo.24024627</a></td></tr>
<tr><td>SM hypercharge uniqueness</td><td>anomaly cancellation forces the hypercharges (up to scale + u↔d)</td>
<td class='st'><span class='pill ok'>SM.Hypercharge.hypercharge_uniqueness</span></td></tr>
<tr><td>SM anomaly cancellation</td><td>the five anomaly coefficients vanish for (1/6,2/3,−1/3,−1/2,−1)</td>
<td class='st'><span class='pill ok'>SM.Anomaly.anomaly_cancellation</span></td></tr>
<tr><td>SM flavor invariant ring</td><td>exact Hilbert series (1−t²⁴)/…, dimension 13, Jarlskog syzygy</td>
<td class='st'><span class='pill ok'>validate_sm_molien_weyl.py</span> — <a href="https://doi.org/10.5281/zenodo.24024631">10.5281/zenodo.24024631</a></td></tr>
</tbody></table>
<p class="prov">evidence: pacland-proof/ (lake build green, #print axioms = propext + Classical.choice +
Quot.sound); scripts/validate_sm_*.py (dispose-verified on the harness mesh)</p>
```

Publish steps (after DOIs): paste the block into `web/verify.html`, then
`bash scripts/deploy-pages.sh`, then verify the live fetch (`curl -s https://pacland.morpheus.nz/ | grep "proof arm"`).
