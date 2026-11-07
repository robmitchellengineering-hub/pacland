import Gleason.Real3.FrameFunction

/-!
**FR.** # Lemme du simplexe (échauffement, semaine 1)

Version abstraite du « warm-up » de Cooke–Keane–Moran / du lemme quantitatif de
Richman–Bridges : une fonction bornée sur `[0,1]` dont la somme sur les paires ne
dépend que de la somme des arguments est affine. Preuve par récurrence dyadique +
bornitude (aucun choix, aucune continuité supposée).

C'est le PREMIER lemme analytique à prouver : il valide le style de preuve
(récurrences dyadiques, encadrements) avant d'attaquer la sphère.

**EN.** # Simplex lemma (warm-up, week 1)

Abstract version of the Cooke–Keane–Moran "warm-up" / of the Richman–Bridges
quantitative lemma: a bounded function on `[0,1]` whose sum over pairs depends
only on the sum of the arguments is affine. Proof by dyadic induction +
boundedness (no choice, no continuity assumed).

This is the FIRST analytic lemma to prove: it validates the proof style (dyadic
inductions, sandwich bounds) before tackling the sphere.
-/

namespace Gleason

/- ═══════════════════════════════════════════════════════════════════
   Recherche Mathlib (avant de prouver quoi que ce soit) :
   AUCUN théorème générique « additive + bornée ⇒ linéaire » (équation de
   Cauchy) n'existe dans Mathlib : ni version measurable/continue automatique,
   ni théorème de Steinhaus. Le seul élément utile,
   `AddMonoidHom.toRealLinearMap` (continue ⇒ ℝ-linéaire sur un morphisme
   GLOBAL), ne s'applique pas ici car `g` n'est défini que sur `[0,1]` avec
   une additivité restreinte (pas un morphisme sur `ℝ` tout entier) : l'argument
   classique « f(nx) mod 1 » suppose un domaine global. Il faut donc l'argument
   dyadique à la main (étapes ci-dessous, toutes prouvées : 0 `sorry`).
   ═══════════════════════════════════════════════════════════════════ -/

/--
**FR.** **Étape 1.** `g x := h x - h 0 - x * (h 1 - h 0)` s'annule en `0` et en `1`,
reste bornée sur `[0,1]` (par `4C`), et hérite de l'additivité restreinte de `h`.

**EN.** **Step 1.** `g x := h x - h 0 - x * (h 1 - h 0)` vanishes at `0` and `1`,
stays bounded on `[0,1]` (by `4C`), and inherits the restricted additivity of
`h`.
-/
private theorem simplex_g_props (h : ℝ → ℝ) (C : ℝ)
    (hb : ∀ x ∈ Set.Icc (0 : ℝ) 1, |h x| ≤ C)
    (hadd : ∀ x y u v : ℝ, x ∈ Set.Icc (0 : ℝ) 1 → y ∈ Set.Icc (0 : ℝ) 1 →
      u ∈ Set.Icc (0 : ℝ) 1 → v ∈ Set.Icc (0 : ℝ) 1 →
      x + y = u + v → h x + h y = h u + h v) :
    h 0 - h 0 - (0 : ℝ) * (h 1 - h 0) = 0 ∧
    h 1 - h 0 - (1 : ℝ) * (h 1 - h 0) = 0 ∧
    (∀ x ∈ Set.Icc (0 : ℝ) 1, |h x - h 0 - x * (h 1 - h 0)| ≤ 4 * C) ∧
    (∀ x y u v : ℝ, x ∈ Set.Icc (0 : ℝ) 1 → y ∈ Set.Icc (0 : ℝ) 1 →
      u ∈ Set.Icc (0 : ℝ) 1 → v ∈ Set.Icc (0 : ℝ) 1 → x + y = u + v →
      (h x - h 0 - x * (h 1 - h 0)) + (h y - h 0 - y * (h 1 - h 0)) =
      (h u - h 0 - u * (h 1 - h 0)) + (h v - h 0 - v * (h 1 - h 0))) := by
  refine ⟨by ring, by ring, ?_, ?_⟩
  · intro x hx
    obtain ⟨hx0, hx1⟩ := hx
    have hbx := hb x ⟨hx0, hx1⟩
    have hb0 := hb 0 ⟨le_refl 0, zero_le_one⟩
    have hb1 := hb 1 ⟨zero_le_one, le_refl 1⟩
    have hxabs : |x| = x := abs_of_nonneg hx0
    have htri1 : |h 1 - h 0| ≤ |h 1| + |h 0| := by
      have := abs_add_le (h 1) (-(h 0))
      simpa [sub_eq_add_neg] using this
    have h2C : |h 1 - h 0| ≤ 2 * C := by linarith
    have hxy : |x * (h 1 - h 0)| ≤ 2 * C := by
      rw [abs_mul, hxabs]
      calc x * |h 1 - h 0| ≤ 1 * |h 1 - h 0| :=
            mul_le_mul_of_nonneg_right hx1 (abs_nonneg _)
        _ = |h 1 - h 0| := one_mul _
        _ ≤ 2 * C := h2C
    have htri2 : |h x - h 0 - x * (h 1 - h 0)| ≤ |h x - h 0| + |x * (h 1 - h 0)| := by
      have := abs_add_le (h x - h 0) (-(x * (h 1 - h 0)))
      simpa [sub_eq_add_neg] using this
    have htri3 : |h x - h 0| ≤ |h x| + |h 0| := by
      have := abs_add_le (h x) (-(h 0))
      simpa [sub_eq_add_neg] using this
    linarith
  · intro x y u v hx hy hu hv hsum
    have heq := hadd x y u v hx hy hu hv hsum
    have key : x * (h 1 - h 0) + y * (h 1 - h 0) = u * (h 1 - h 0) + v * (h 1 - h 0) := by
      rw [← add_mul, ← add_mul, hsum]
    linarith [heq, key]

/--
**FR.** **Étape 2.** Spécialisation de l'additivité restreinte à `y = 0`, `v = x - u` :
pour `0 ≤ u ≤ x ≤ 1`, `g x = g u + g (x - u)`.

**EN.** **Step 2.** Specialization of the restricted additivity at `y = 0`,
`v = x - u`: for `0 ≤ u ≤ x ≤ 1`, `g x = g u + g (x - u)`.
-/
private theorem simplex_split (g : ℝ → ℝ) (hg0 : g 0 = 0)
    (hgadd : ∀ x y u v : ℝ, x ∈ Set.Icc (0 : ℝ) 1 → y ∈ Set.Icc (0 : ℝ) 1 →
      u ∈ Set.Icc (0 : ℝ) 1 → v ∈ Set.Icc (0 : ℝ) 1 → x + y = u + v →
      g x + g y = g u + g v) :
    ∀ x u : ℝ, u ∈ Set.Icc (0 : ℝ) 1 → x ∈ Set.Icc (0 : ℝ) 1 → u ≤ x →
      g x = g u + g (x - u) := by
  intro x u hu hx hux
  obtain ⟨hu0, hu1⟩ := hu
  obtain ⟨hx0, hx1⟩ := hx
  have hv : x - u ∈ Set.Icc (0 : ℝ) 1 := ⟨by linarith, by linarith⟩
  have h0mem : (0 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨le_refl 0, zero_le_one⟩
  have heq := hgadd x 0 u (x - u) ⟨hx0, hx1⟩ h0mem ⟨hu0, hu1⟩ hv (by ring)
  rw [hg0] at heq
  linarith

/--
**FR.** **Étape 3a (halving).** Récurrence sur `n` via `simplex_split` (avec
`u = x / 2`) : `g (x / 2^n) = g x / 2^n` pour `x ∈ [0,1]`.

**EN.** **Step 3a (halving).** Induction on `n` via `simplex_split` (with
`u = x / 2`): `g (x / 2^n) = g x / 2^n` for `x ∈ [0,1]`.
-/
private theorem simplex_halve (g : ℝ → ℝ)
    (hsplit : ∀ x u : ℝ, u ∈ Set.Icc (0 : ℝ) 1 → x ∈ Set.Icc (0 : ℝ) 1 → u ≤ x →
      g x = g u + g (x - u)) :
    ∀ x ∈ Set.Icc (0 : ℝ) 1, ∀ n : ℕ, g (x / 2 ^ n) = g x / 2 ^ n := by
  have hhalf : ∀ x ∈ Set.Icc (0 : ℝ) 1, g (x / 2) = g x / 2 := by
    intro x hx
    obtain ⟨hx0, hx1⟩ := hx
    have hu : x / 2 ∈ Set.Icc (0 : ℝ) 1 := ⟨by linarith, by linarith⟩
    have heq := hsplit x (x / 2) hu ⟨hx0, hx1⟩ (by linarith)
    have hsub : x - x / 2 = x / 2 := by ring
    rw [hsub] at heq
    linarith
  have main : ∀ n : ℕ, ∀ x ∈ Set.Icc (0 : ℝ) 1, g (x / 2 ^ n) = g x / 2 ^ n := by
    intro n
    induction n with
    | zero => intro x _; simp
    | succ n ih =>
      intro x hx
      obtain ⟨hx0, hx1⟩ := hx
      have hx2 : x / 2 ∈ Set.Icc (0 : ℝ) 1 := ⟨by linarith, by linarith⟩
      have step1 : x / 2 ^ (n + 1) = (x / 2) / 2 ^ n := by rw [pow_succ]; ring
      rw [step1, ih (x / 2) hx2, hhalf x ⟨hx0, hx1⟩, pow_succ]
      ring
  intro x hx n
  exact main n x hx

/--
**FR.** **Étape 3b (multiples entiers, base réelle arbitraire).** Récurrence sur `k`
via `simplex_split` (avec `u = k * t`, `x = (k+1) * t`) : `g (k * t) = k * g t`
pour tout réel `t ≥ 0` tel que `k * t ≤ 1`. Généralise le cas dyadique
`t = 1/2^n` : nécessaire pour `simplex_vanish`, où l'amplification
`g (2^n * r) = 2^n * g r` porte sur un réel `r` quelconque (le reste de
`Int.fract`), pas seulement sur `t = 1/2^n`. Le cas de base `k = 0` utilise
`g 0 = 0`, lui-même dérivable de `hsplit` en `x = u = 0`.

**EN.** **Step 3b (integer multiples, arbitrary real base).** Induction on `k`
via `simplex_split` (with `u = k * t`, `x = (k+1) * t`): `g (k * t) = k * g t`
for every real `t ≥ 0` such that `k * t ≤ 1`. Generalizes the dyadic case
`t = 1/2^n`: needed for `simplex_vanish`, where the amplification
`g (2^n * r) = 2^n * g r` applies to an arbitrary real `r` (the remainder of
`Int.fract`), not just to `t = 1/2^n`. The base case `k = 0` uses `g 0 = 0`,
itself derivable from `hsplit` at `x = u = 0`.
-/
private theorem simplex_nat_mul (g : ℝ → ℝ)
    (hsplit : ∀ x u : ℝ, u ∈ Set.Icc (0 : ℝ) 1 → x ∈ Set.Icc (0 : ℝ) 1 → u ≤ x →
      g x = g u + g (x - u)) :
    ∀ (k : ℕ) (t : ℝ), 0 ≤ t → (k : ℝ) * t ≤ 1 → g ((k : ℝ) * t) = (k : ℝ) * g t := by
  have hg0 : g 0 = 0 := by
    have := hsplit 0 0 ⟨le_refl 0, zero_le_one⟩ ⟨le_refl 0, zero_le_one⟩ (le_refl 0)
    simpa using this
  intro k
  induction k with
  | zero => intro t _ _; simp [hg0]
  | succ k ih =>
    intro t ht0 ht1
    push_cast at ht1 ⊢
    have hkt1 : (k : ℝ) * t ≤ 1 :=
      le_trans (mul_le_mul_of_nonneg_right (by linarith : (k : ℝ) ≤ (k : ℝ) + 1) ht0) ht1
    have hmem_kt : (k : ℝ) * t ∈ Set.Icc (0 : ℝ) 1 :=
      ⟨mul_nonneg (Nat.cast_nonneg k) ht0, hkt1⟩
    have hmem_succ : ((k : ℝ) + 1) * t ∈ Set.Icc (0 : ℝ) 1 :=
      ⟨mul_nonneg (by positivity) ht0, ht1⟩
    have hle : (k : ℝ) * t ≤ ((k : ℝ) + 1) * t :=
      mul_le_mul_of_nonneg_right (by linarith) ht0
    have heq := hsplit (((k : ℝ) + 1) * t) ((k : ℝ) * t) hmem_kt hmem_succ hle
    have hdiff : ((k : ℝ) + 1) * t - (k : ℝ) * t = t := by ring
    rw [hdiff, ih t ht0 hkt1] at heq
    rw [heq]
    ring

/--
**FR.** **Étape 3 (assemblage, corollaire dyadique de `simplex_nat_mul`).** Combine
`simplex_halve` en `x = 1` (donnant `g (1/2^n) = g 1 / 2^n = 0`) avec
`simplex_nat_mul` en `t = 1/2^n` : `g` s'annule sur tous les dyadiques de
`[0,1]`. Purement algébrique, AUCUNE bornitude requise (contrairement à
l'étape 4).

**EN.** **Step 3 (assembly, dyadic corollary of `simplex_nat_mul`).** Combines
`simplex_halve` at `x = 1` (giving `g (1/2^n) = g 1 / 2^n = 0`) with
`simplex_nat_mul` at `t = 1/2^n`: `g` vanishes on all dyadics of `[0,1]`. Purely
algebraic, NO boundedness required (unlike step 4).
-/
private theorem simplex_dyadic_vanish (g : ℝ → ℝ) (hg1 : g 1 = 0)
    (hhalve : ∀ x ∈ Set.Icc (0 : ℝ) 1, ∀ n : ℕ, g (x / 2 ^ n) = g x / 2 ^ n)
    (hmul : ∀ (k : ℕ) (t : ℝ), 0 ≤ t → (k : ℝ) * t ≤ 1 → g ((k : ℝ) * t) = (k : ℝ) * g t) :
    ∀ n k : ℕ, k ≤ 2 ^ n → g ((k : ℝ) / 2 ^ n) = 0 := by
  intro n k hk
  have hmem1 : (1 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨zero_le_one, le_refl 1⟩
  have ht0 : (0 : ℝ) ≤ 1 / 2 ^ n := by positivity
  have hgt : g (1 / 2 ^ n) = 0 := by
    have := hhalve 1 hmem1 n
    rw [hg1] at this
    simpa using this
  have hkcast : (k : ℝ) ≤ (2 : ℝ) ^ n := by exact_mod_cast hk
  have hkt1 : (k : ℝ) * (1 / 2 ^ n) ≤ 1 := by
    rw [mul_one_div, div_le_one (by positivity)]
    exact hkcast
  have heq := hmul k (1 / 2 ^ n) ht0 hkt1
  rw [hgt, mul_zero] at heq
  have hcast : (k : ℝ) / 2 ^ n = (k : ℝ) * (1 / 2 ^ n) := by rw [mul_one_div]
  rw [hcast]
  exact heq

/--
**FR.** **Étape 4 (le cœur analytique).** Pour `x ∈ [0,1]` et tout `n`, en posant
`k = ⌊x·2^n⌋` et `r = x - k/2^n ∈ [0, 1/2^n)`, `simplex_split` donne
`g x = g (k/2^n) + g r = g r` (dyadique nul). Puis `simplex_nat_mul` en
`k' = 2^n`, `t = r` (licite car `2^n · r < 1`) donne
`g (2^n · r) = 2^n · g r`, donc `|g r| ≤ C / 2^n` (bornitude de `g (2^n r)`
via `hb`), d'où `|g x| ≤ C / 2^n` pour tout `n` : `g x = 0` par la propriété
d'Archimède. C'est ici, et seulement ici, que la bornitude de `g` est
utilisée.

**EN.** **Step 4 (the analytic core).** For `x ∈ [0,1]` and every `n`, setting
`k = ⌊x·2^n⌋` and `r = x - k/2^n ∈ [0, 1/2^n)`, `simplex_split` gives
`g x = g (k/2^n) + g r = g r` (dyadic, zero). Then `simplex_nat_mul` at
`k' = 2^n`, `t = r` (valid since `2^n · r < 1`) gives
`g (2^n · r) = 2^n · g r`, so `|g r| ≤ C / 2^n` (boundedness of `g (2^n r)` via
`hb`), hence `|g x| ≤ C / 2^n` for every `n`: `g x = 0` by the Archimedean
property. This is the only place where boundedness of `g` is used.
-/
private theorem simplex_vanish (g : ℝ → ℝ) (C : ℝ)
    (hb : ∀ x ∈ Set.Icc (0 : ℝ) 1, |g x| ≤ C)
    (hsplit : ∀ x u : ℝ, u ∈ Set.Icc (0 : ℝ) 1 → x ∈ Set.Icc (0 : ℝ) 1 → u ≤ x →
      g x = g u + g (x - u))
    (hmul : ∀ (k : ℕ) (t : ℝ), 0 ≤ t → (k : ℝ) * t ≤ 1 → g ((k : ℝ) * t) = (k : ℝ) * g t)
    (hdyadic : ∀ n k : ℕ, k ≤ 2 ^ n → g ((k : ℝ) / 2 ^ n) = 0) :
    ∀ x ∈ Set.Icc (0 : ℝ) 1, g x = 0 := by
  intro x hx
  obtain ⟨hx0, hx1⟩ := hx
  have hC0 : 0 ≤ C := le_trans (abs_nonneg _) (hb 0 ⟨le_refl 0, zero_le_one⟩)
  have hbound : ∀ n : ℕ, |g x| ≤ C / 2 ^ n := by
    intro n
    have hpow_pos : (0:ℝ) < 2 ^ n := by positivity
    set y : ℝ := (2 : ℝ) ^ n * x with hy_def
    have hy0 : 0 ≤ y := by positivity
    have hm0 : 0 ≤ ⌊y⌋ := Int.le_floor.mpr (by simpa using hy0)
    set k : ℕ := ⌊y⌋.toNat with hk_def
    have hk_cast : (k : ℤ) = ⌊y⌋ := Int.toNat_of_nonneg hm0
    have hk_cast' : (k : ℝ) = (⌊y⌋ : ℝ) := by exact_mod_cast hk_cast
    have hyle : y ≤ (2 : ℝ) ^ n := by rw [hy_def]; nlinarith
    have hkle : k ≤ 2 ^ n := by
      have h1 : ⌊y⌋ ≤ ⌊(2 : ℝ) ^ n⌋ := Int.floor_le_floor hyle
      rw [show ((2 : ℝ) ^ n) = ((2 ^ n : ℕ) : ℝ) by push_cast; ring,
          Int.floor_natCast] at h1
      have h2 : (k : ℤ) ≤ (2 ^ n : ℕ) := hk_cast ▸ h1
      exact_mod_cast h2
    have hd_le_x : (k : ℝ) / 2 ^ n ≤ x := by
      rw [hk_cast', div_le_iff₀ hpow_pos]
      have := Int.floor_le y
      rw [hy_def] at this
      linarith
    have hd_mem : (k : ℝ) / 2 ^ n ∈ Set.Icc (0 : ℝ) 1 :=
      ⟨by positivity, by linarith⟩
    have hgd : g ((k : ℝ) / 2 ^ n) = 0 := hdyadic n k hkle
    have hsplit_eq := hsplit x ((k : ℝ) / 2 ^ n) hd_mem ⟨hx0, hx1⟩ hd_le_x
    rw [hgd, zero_add] at hsplit_eq
    set r : ℝ := x - (k : ℝ) / 2 ^ n with hr_def
    have hr0 : 0 ≤ r := by rw [hr_def]; linarith
    have hr_lt : (2 : ℝ) ^ n * r < 1 := by
      have hlt := Int.lt_floor_add_one y
      rw [hy_def] at hlt
      have hexpand : (2 : ℝ) ^ n * r = (2 : ℝ) ^ n * x - (k : ℝ) := by
        rw [hr_def, hk_cast']; field_simp
      rw [hexpand]
      linarith
    have hr_le : (2 : ℝ) ^ n * r ≤ 1 := le_of_lt hr_lt
    have hmul_eq := hmul (2 ^ n) r hr0 (by push_cast; exact hr_le)
    rw [show ((2 ^ n : ℕ) : ℝ) = (2 : ℝ) ^ n by push_cast; ring] at hmul_eq
    have hmem2r : (2 : ℝ) ^ n * r ∈ Set.Icc (0 : ℝ) 1 := ⟨by positivity, hr_le⟩
    have hb2r : |g ((2 : ℝ) ^ n * r)| ≤ C := hb _ hmem2r
    have hgr_bound : |g r| ≤ C / 2 ^ n := by
      rw [hmul_eq, abs_mul, abs_of_pos hpow_pos] at hb2r
      rw [le_div_iff₀ hpow_pos]
      linarith
    rw [hsplit_eq]
    exact hgr_bound
  by_contra hne
  have hpos : 0 < |g x| := abs_pos.mpr hne
  obtain ⟨n, hn⟩ := pow_unbounded_of_one_lt (C / |g x|) (by norm_num : (1:ℝ) < 2)
  rw [div_lt_iff₀ hpos] at hn
  have hb2 := hbound n
  rw [le_div_iff₀ (by positivity : (0:ℝ) < 2 ^ n)] at hb2
  linarith

/--
**FR.** **Étape 5 / Lemme du simplexe (assemblage final).** `g ≡ 0` sur `[0,1]` se
retraduit en `h x = a * x + b` avec `a = h 1 - h 0`, `b = h 0`. Si `h` est bornée
sur `[0,1]` et si `h x + h y` ne dépend que de `x + y`, alors `h` est affine
sur `[0,1]`.

**EN.** **Step 5 / Simplex lemma (final assembly).** `g ≡ 0` on `[0,1]` translates
back to `h x = a * x + b` with `a = h 1 - h 0`, `b = h 0`. If `h` is bounded on
`[0,1]` and `h x + h y` depends only on `x + y`, then `h` is affine on `[0,1]`.
-/
theorem bounded_additive_affine (h : ℝ → ℝ) (C : ℝ)
    (hb : ∀ x ∈ Set.Icc (0 : ℝ) 1, |h x| ≤ C)
    (hadd : ∀ x y u v : ℝ, x ∈ Set.Icc (0 : ℝ) 1 → y ∈ Set.Icc (0 : ℝ) 1 →
      u ∈ Set.Icc (0 : ℝ) 1 → v ∈ Set.Icc (0 : ℝ) 1 →
      x + y = u + v → h x + h y = h u + h v) :
    ∃ a b : ℝ, ∀ x ∈ Set.Icc (0 : ℝ) 1, h x = a * x + b := by
  obtain ⟨hg0, hg1, hgb, hgadd⟩ := simplex_g_props h C hb hadd
  have hsplit := simplex_split (fun x => h x - h 0 - x * (h 1 - h 0)) hg0 hgadd
  have hhalve := simplex_halve (fun x => h x - h 0 - x * (h 1 - h 0)) hsplit
  have hmul := simplex_nat_mul (fun x => h x - h 0 - x * (h 1 - h 0)) hsplit
  have hdyadic := simplex_dyadic_vanish (fun x => h x - h 0 - x * (h 1 - h 0)) hg1 hhalve hmul
  have hvanish := simplex_vanish (fun x => h x - h 0 - x * (h 1 - h 0)) (4 * C) hgb hsplit
    hmul hdyadic
  refine ⟨h 1 - h 0, h 0, fun x hx => ?_⟩
  have hgx : h x - h 0 - x * (h 1 - h 0) = 0 := hvanish x hx
  linarith

-- ═══════════════════════════════════════════════════════════════════
-- Warmup Theorem II (CKM 1985 §3) : monotone + additif-à-1 sur [0,1] \ C
-- (C dénombrable, C ⊆ (0,1)) ⇒ f = identité sur [0,1] \ C.
-- Recherche Mathlib (avant de prouver quoi que ce soit) : aucun théorème
-- générique « monotone + additif ⇒ linéaire » n'existe. Non-dénombrabilité de
-- Ioo 0 1 : pas de lemme direct `¬Countable`, mais route cardinale propre via
-- Cardinal.mk_Ioo_real + Cardinal.aleph0_lt_continuum + le_aleph0_iff_set_countable
-- (préférée à la route mesure, qui marche aussi via Real.volume_Ioo +
-- Set.Countable.measure_zero mais alourdit les imports).
-- ═══════════════════════════════════════════════════════════════════

/--
**FR.** **D1.** `f 1 = 1`, via le triplet `(0,0,1)` (`0,1 ∉ C` car `C ⊆ Ioo 0 1`).

**EN.** **D1.** `f 1 = 1`, via the triple `(0,0,1)` (`0,1 ∉ C` since
`C ⊆ Ioo 0 1`).
-/
private theorem warmup_II_D1 {C : Set ℝ} (hCsub : C ⊆ Set.Ioo (0 : ℝ) 1) (f : ℝ → ℝ)
    (hf0 : f 0 = 0)
    (htriple : ∀ a b c, a ∈ Set.Icc (0 : ℝ) 1 \ C → b ∈ Set.Icc (0 : ℝ) 1 \ C →
      c ∈ Set.Icc (0 : ℝ) 1 \ C → a + b + c = 1 → f a + f b + f c = 1) :
    f 1 = 1 := by
  have h0 : (0 : ℝ) ∈ Set.Icc (0 : ℝ) 1 \ C := by
    refine ⟨⟨le_refl 0, zero_le_one⟩, fun hc => ?_⟩
    exact absurd (hCsub hc).1 (lt_irrefl 0)
  have h1 : (1 : ℝ) ∈ Set.Icc (0 : ℝ) 1 \ C := by
    refine ⟨⟨zero_le_one, le_refl 1⟩, fun hc => ?_⟩
    exact absurd (hCsub hc).2 (lt_irrefl 1)
  have h := htriple 0 0 1 h0 h0 h1 (by ring)
  rw [hf0] at h
  linarith

/--
**FR.** **D2.** Il existe un point `a₀ ∈ (0,1)` « générique » : pour tous `p q : ℕ`
avec `q > 0` et `(p/q)·a₀ ≤ 1`, ni `(p/q)·a₀` ni `1 - (p/q)·a₀` ne sont dans `C`.
Construit via l'ensemble dénombrable `⋃_{c∈C} ℚ·c ∪ ⋃_{c∈C} ℚ·(1-c)` : tout point
hors de cet ensemble a la propriété (sinon `a₀` s'écrirait `(q/p)·c` ou
`(q/p)·(1-c)` pour un `c ∈ C`, avec `p ≠ 0` car `c ∈ (0,1)`).

**EN.** **D2.** There exists a "generic" point `a₀ ∈ (0,1)`: for all `p q : ℕ`
with `q > 0` and `(p/q)·a₀ ≤ 1`, neither `(p/q)·a₀` nor `1 - (p/q)·a₀` lies in
`C`. Built from the countable set
`⋃_{c∈C} ℚ·c ∪ ⋃_{c∈C} ℚ·(1-c)`: any point outside this set has the property
(otherwise `a₀` would be `(q/p)·c` or `(q/p)·(1-c)` for some `c ∈ C`, with
`p ≠ 0` since `c ∈ (0,1)`).
-/
private theorem warmup_II_D2 {C : Set ℝ} (hC : C.Countable) (hCsub : C ⊆ Set.Ioo (0 : ℝ) 1) :
    ∃ a₀ ∈ Set.Ioo (0 : ℝ) 1, ∀ p q : ℕ, 0 < q → (p : ℝ) / q * a₀ ≤ 1 →
      (p : ℝ) / q * a₀ ∉ C ∧ 1 - (p : ℝ) / q * a₀ ∉ C := by
  set S1 : Set ℝ := ⋃ c ∈ C, Set.range (fun r : ℚ => (r : ℝ) * c) with hS1_def
  set S2 : Set ℝ := ⋃ c ∈ C, Set.range (fun r : ℚ => (r : ℝ) * (1 - c)) with hS2_def
  have hS1 : S1.Countable := hC.biUnion (fun c _ => Set.countable_range _)
  have hS2 : S2.Countable := hC.biUnion (fun c _ => Set.countable_range _)
  have hSC : (S1 ∪ S2).Countable := hS1.union hS2
  have hUncount : ¬ (Set.Ioo (0 : ℝ) 1).Countable := by
    intro hcount
    have h1 : Cardinal.mk (Set.Ioo (0 : ℝ) 1) ≤ Cardinal.aleph0 :=
      Cardinal.le_aleph0_iff_set_countable.mpr hcount
    rw [Cardinal.mk_Ioo_real (by norm_num : (0 : ℝ) < 1)] at h1
    exact absurd h1 (not_le.mpr Cardinal.aleph0_lt_continuum)
  have hnotsub : ¬ Set.Ioo (0 : ℝ) 1 ⊆ S1 ∪ S2 := fun hsub => hUncount (hSC.mono hsub)
  obtain ⟨a₀, ha₀mem, ha₀notin⟩ := Set.not_subset.mp hnotsub
  refine ⟨a₀, ha₀mem, ?_⟩
  intro p q hq hle
  have hqR : (q : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hq.ne'
  constructor
  · intro hcmem
    apply ha₀notin
    have hppos : 0 < (p : ℝ) / q * a₀ := (hCsub hcmem).1
    have hp0 : p ≠ 0 := by intro h; subst h; simp at hppos
    have hpR : (p : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hp0
    refine Set.mem_union_left _ (Set.mem_biUnion hcmem ⟨(q : ℚ) / (p : ℚ), ?_⟩)
    push_cast
    field_simp
  · intro hcmem
    apply ha₀notin
    have hclt : 1 - (p : ℝ) / q * a₀ < 1 := (hCsub hcmem).2
    have hppos : 0 < (p : ℝ) / q * a₀ := by linarith
    have hp0 : p ≠ 0 := by intro h; subst h; simp at hppos
    have hpR : (p : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hp0
    refine Set.mem_union_right _ (Set.mem_biUnion hcmem ⟨(q : ℚ) / (p : ℚ), ?_⟩)
    push_cast
    field_simp
    ring

/--
**FR.** **D3.** Additivité sur l'orbite de `a₀` : deux applications de `htriple`
(`(p/q·a₀, p'/q·a₀, 1-(p+p')/q·a₀)` puis `((p+p')/q·a₀, 1-(p+p')/q·a₀, 0)`),
soustraction, `hf0`. Toutes les appartenances viennent de `hgen` (D2).

**EN.** **D3.** Additivity on the orbit of `a₀`: two applications of `htriple`
(`(p/q·a₀, p'/q·a₀, 1-(p+p')/q·a₀)` then
`((p+p')/q·a₀, 1-(p+p')/q·a₀, 0)`), subtraction, `hf0`. All memberships come
from `hgen` (D2).
-/
private theorem warmup_II_D3 {C : Set ℝ} (f : ℝ → ℝ) (hf0 : f 0 = 0)
    (htriple : ∀ a b c, a ∈ Set.Icc (0 : ℝ) 1 \ C → b ∈ Set.Icc (0 : ℝ) 1 \ C →
      c ∈ Set.Icc (0 : ℝ) 1 \ C → a + b + c = 1 → f a + f b + f c = 1)
    {a₀ : ℝ} (ha₀ : a₀ ∈ Set.Ioo (0 : ℝ) 1)
    (hgen : ∀ p q : ℕ, 0 < q → (p : ℝ) / q * a₀ ≤ 1 →
      (p : ℝ) / q * a₀ ∉ C ∧ 1 - (p : ℝ) / q * a₀ ∉ C) :
    ∀ p p' q : ℕ, 0 < q → ((p + p' : ℕ) : ℝ) / q * a₀ ≤ 1 →
      f ((p : ℝ) / q * a₀) + f ((p' : ℝ) / q * a₀) = f (((p + p' : ℕ) : ℝ) / q * a₀) := by
  intro p p' q hq hle
  have ha₀pos : 0 < a₀ := ha₀.1
  set x : ℝ := (p : ℝ) / q * a₀ with hx_def
  set y : ℝ := (p' : ℝ) / q * a₀ with hy_def
  set z : ℝ := ((p + p' : ℕ) : ℝ) / q * a₀ with hz_def
  have hxy : x + y = z := by rw [hx_def, hy_def, hz_def]; push_cast; ring
  have hx0 : 0 ≤ x := by rw [hx_def]; positivity
  have hy0 : 0 ≤ y := by rw [hy_def]; positivity
  have hz0 : 0 ≤ z := by rw [← hxy]; linarith
  have hxz : x ≤ z := by rw [← hxy]; linarith
  have hyz : y ≤ z := by rw [← hxy]; linarith
  have hx1 : x ≤ 1 := le_trans hxz hle
  have hy1 : y ≤ 1 := le_trans hyz hle
  have hxC : x ∉ C := (hgen p q hq hx1).1
  have hyC : y ∉ C := (hgen p' q hq hy1).1
  have hzC : z ∉ C := (hgen (p + p') q hq hle).1
  have hwC : 1 - z ∉ C := (hgen (p + p') q hq hle).2
  have h0aux := hgen 0 1 one_pos (by norm_num)
  have h0C : (0 : ℝ) ∉ C := by simpa using h0aux.1
  have hxmem : x ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨hx0, hx1⟩, hxC⟩
  have hymem : y ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨hy0, hy1⟩, hyC⟩
  have hzmem : z ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨hz0, hle⟩, hzC⟩
  have hwmem : (1 - z) ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨by linarith, by linarith⟩, hwC⟩
  have h0mem : (0 : ℝ) ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨le_refl 0, zero_le_one⟩, h0C⟩
  have heq1 := htriple x y (1 - z) hxmem hymem hwmem (by linarith)
  have heq2 := htriple z (1 - z) 0 hzmem hwmem h0mem (by ring)
  rw [hf0] at heq2
  linarith

/--
**FR.** **D4.** Homogénéité rationnelle sur l'orbite : `f((p/q)·a₀) = (p/q)·f(a₀)`.
Deux temps : (i) récurrence sur `p` via D3 pour `f(p·(a₀/q)) = p·f(a₀/q)` tant
que `p·(a₀/q) ≤ 1` ; (ii) cas `p = q` donne `f(a₀) = q·f(a₀/q)` ; combiner.

**EN.** **D4.** Rational homogeneity on the orbit:
`f((p/q)·a₀) = (p/q)·f(a₀)`. Two steps: (i) induction on `p` via D3 for
`f(p·(a₀/q)) = p·f(a₀/q)` as long as `p·(a₀/q) ≤ 1`; (ii) case `p = q` gives
`f(a₀) = q·f(a₀/q)`; combine.
-/
private theorem warmup_II_D4 {C : Set ℝ} (f : ℝ → ℝ) (hf0 : f 0 = 0)
    (htriple : ∀ a b c, a ∈ Set.Icc (0 : ℝ) 1 \ C → b ∈ Set.Icc (0 : ℝ) 1 \ C →
      c ∈ Set.Icc (0 : ℝ) 1 \ C → a + b + c = 1 → f a + f b + f c = 1)
    {a₀ : ℝ} (ha₀ : a₀ ∈ Set.Ioo (0 : ℝ) 1)
    (hgen : ∀ p q : ℕ, 0 < q → (p : ℝ) / q * a₀ ≤ 1 →
      (p : ℝ) / q * a₀ ∉ C ∧ 1 - (p : ℝ) / q * a₀ ∉ C) :
    ∀ p q : ℕ, 0 < q → (p : ℝ) / q * a₀ ≤ 1 → f ((p : ℝ) / q * a₀) = (p : ℝ) / q * f a₀ := by
  have hD3 := warmup_II_D3 f hf0 htriple ha₀ hgen
  intro p q hq
  have hqR_ne : (q : ℝ) ≠ 0 := by exact_mod_cast hq.ne'
  -- (i) f (p/q·a₀) = p · f (1/q·a₀), par récurrence sur p
  have hstep : ∀ p : ℕ, (p : ℝ) / q * a₀ ≤ 1 →
      f ((p : ℝ) / q * a₀) = (p : ℝ) * f ((1 : ℝ) / q * a₀) := by
    intro p
    induction p with
    | zero => intro _; simp [hf0]
    | succ n ih =>
      intro hle
      have hdecomp : ((n + 1 : ℕ) : ℝ) / q * a₀ = (n : ℝ) / q * a₀ + (1 : ℝ) / q * a₀ := by
        push_cast; ring
      have hle' := hle
      rw [hdecomp] at hle'
      have ha₀pos : 0 < a₀ := ha₀.1
      have hqR : (0 : ℝ) < q := by exact_mod_cast hq
      have hpos2 : 0 ≤ (1 : ℝ) / q * a₀ := by positivity
      have hnle : (n : ℝ) / q * a₀ ≤ 1 := by linarith
      have key := hD3 n 1 q hq hle
      rw [ih hnle] at key
      push_cast at key ⊢
      rw [← key]
      ring
  -- (ii) cas p = q : f(a₀) = q · f(1/q·a₀)
  have hqeq : f a₀ = (q : ℝ) * f ((1 : ℝ) / q * a₀) := by
    have hqle : (q : ℝ) / q * a₀ ≤ 1 := by
      rw [div_self hqR_ne, one_mul]; exact ha₀.2.le
    have hh := hstep q hqle
    rwa [div_self hqR_ne, one_mul] at hh
  -- combinaison
  intro hle
  have hinv : f ((1 : ℝ) / q * a₀) = f a₀ / q := by
    rw [hqeq, mul_div_cancel_left₀ _ hqR_ne]
  rw [hstep p hle, hinv]
  ring

/--
**FR.** **D6-existence.** Il existe `b ∈ (0,1)` avec `b ∉ C` et `1 - b ∉ C`
(l'ensemble `C ∪ {x | 1 - x ∈ C}` est dénombrable, ne peut recouvrir `(0,1)`).

**EN.** **D6-existence.** There exists `b ∈ (0,1)` with `b ∉ C` and `1 - b ∉ C`
(the set `C ∪ {x | 1 - x ∈ C}` is countable, cannot cover `(0,1)`).
-/
private theorem warmup_II_D6_exists {C : Set ℝ} (hC : C.Countable) :
    ∃ b ∈ Set.Ioo (0 : ℝ) 1, b ∉ C ∧ 1 - b ∉ C := by
  set C' : Set ℝ := C ∪ (fun x => 1 - x) '' C with hC'_def
  have hC' : C'.Countable := hC.union (hC.image _)
  have hUncount : ¬ (Set.Ioo (0 : ℝ) 1).Countable := by
    intro hcount
    have h1 : Cardinal.mk (Set.Ioo (0 : ℝ) 1) ≤ Cardinal.aleph0 :=
      Cardinal.le_aleph0_iff_set_countable.mpr hcount
    rw [Cardinal.mk_Ioo_real (by norm_num : (0 : ℝ) < 1)] at h1
    exact absurd h1 (not_le.mpr Cardinal.aleph0_lt_continuum)
  have hnotsub : ¬ Set.Ioo (0 : ℝ) 1 ⊆ C' := fun hsub => hUncount (hC'.mono hsub)
  obtain ⟨b, hbmem, hbnotin⟩ := Set.not_subset.mp hnotsub
  refine ⟨b, hbmem, fun hbC => hbnotin (Set.mem_union_left _ hbC), fun h1bC => ?_⟩
  apply hbnotin
  exact Set.mem_union_right _ ⟨1 - b, h1bC, by ring⟩

/--
**FR.** **D5 (le cœur, squeeze).** Pour `a ∈ [0,1) \ C`, `f a = (f a₀ / a₀) · a`.
Par `le_antisymm`, chaque sens via `∀ ε > 0` : `exists_rat_btwn` donne des
rationnels `r < a/a₀ < r'` (dénominateur commun `q`) avec `r'·a₀ ≤ 1` et
`(r' - r)·a₀` arbitrairement petit ; `hmono` encadre `f a` par
`f(r·a₀) ≤ f a ≤ f(r'·a₀)`, D4 réécrit les bornes en `r·f(a₀)` et `r'·f(a₀)`.

**EN.** **D5 (the core, squeeze).** For `a ∈ [0,1) \ C`, `f a = (f a₀ / a₀) · a`.
By `le_antisymm`, each direction via `∀ ε > 0`: `exists_rat_btwn` gives rationals
`r < a/a₀ < r'` (common denominator `q`) with `r'·a₀ ≤ 1` and
`(r' - r)·a₀` arbitrarily small; `hmono` sandwiches `f a` between
`f(r·a₀) ≤ f a ≤ f(r'·a₀)`, D4 rewrites the bounds as `r·f(a₀)` and
`r'·f(a₀)`.
-/
private theorem warmup_II_D5 {C : Set ℝ} (f : ℝ → ℝ) (hf0 : f 0 = 0)
    (hmono : ∀ a b, a ∈ Set.Icc (0 : ℝ) 1 \ C → b ∈ Set.Icc (0 : ℝ) 1 \ C → a ≤ b → f a ≤ f b)
    {a₀ : ℝ} (ha₀ : a₀ ∈ Set.Ioo (0 : ℝ) 1)
    (hgen : ∀ p q : ℕ, 0 < q → (p : ℝ) / q * a₀ ≤ 1 →
      (p : ℝ) / q * a₀ ∉ C ∧ 1 - (p : ℝ) / q * a₀ ∉ C)
    (hD4 : ∀ p q : ℕ, 0 < q → (p : ℝ) / q * a₀ ≤ 1 → f ((p : ℝ) / q * a₀) = (p : ℝ) / q * f a₀) :
    ∀ a ∈ Set.Ico (0 : ℝ) 1 \ C, f a = (f a₀ / a₀) * a := by
  have ha₀pos : 0 < a₀ := ha₀.1
  have h0C : (0 : ℝ) ∉ C := by simpa using (hgen 0 1 one_pos (by norm_num)).1
  have h0mem : (0 : ℝ) ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨le_refl 0, zero_le_one⟩, h0C⟩
  have ha₀C : a₀ ∉ C := by simpa using (hgen 1 1 one_pos (by simpa using ha₀.2.le)).1
  have ha₀mem : a₀ ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨ha₀pos.le, ha₀.2.le⟩, ha₀C⟩
  have hβ0 : 0 ≤ f a₀ / a₀ := by
    have h := hmono 0 a₀ h0mem ha₀mem ha₀pos.le
    rw [hf0] at h
    exact div_nonneg h ha₀pos.le
  set β : ℝ := f a₀ / a₀ with hβ_def
  have hfa0 : f a₀ = β * a₀ := by rw [hβ_def]; field_simp
  intro a ha
  obtain ⟨⟨ha0, ha1⟩, haC⟩ := ha
  have hamem : a ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨ha0, ha1.le⟩, haC⟩
  have hbound : ∀ ε : ℝ, 0 < ε → |f a - β * a| ≤ ε := by
    intro ε hε
    have h1a : (0 : ℝ) < 1 - a := by linarith
    have hM1 : (0 : ℝ) ≤ a₀ / (1 - a) := by positivity
    have hM2 : (0 : ℝ) ≤ a₀ * β / ε := by positivity
    obtain ⟨q, hq⟩ := exists_nat_gt (max (a₀ / (1 - a)) (a₀ * β / ε))
    have hqQ1 : a₀ / (1 - a) < q := lt_of_le_of_lt (le_max_left _ _) hq
    have hqQ2 : a₀ * β / ε < q := lt_of_le_of_lt (le_max_right _ _) hq
    have hq0 : 0 < q := by
      have : (0 : ℝ) < q := lt_of_le_of_lt hM1 hqQ1
      exact_mod_cast this
    have hqR : (0 : ℝ) < q := by exact_mod_cast hq0
    set p : ℕ := ⌊a / a₀ * q⌋₊ with hp_def
    have ht0 : (0 : ℝ) ≤ a / a₀ * q := by positivity
    have hpa : (p : ℝ) ≤ a / a₀ * q := Nat.floor_le ht0
    have hpb : a / a₀ * q < (p : ℝ) + 1 := Nat.lt_floor_add_one _
    have hrle : (p : ℝ) / q * a₀ ≤ a := by
      rw [div_mul_eq_mul_div, div_le_iff₀ hqR]
      calc (p : ℝ) * a₀ ≤ a / a₀ * q * a₀ := mul_le_mul_of_nonneg_right hpa ha₀pos.le
        _ = a * q := by field_simp
    have hrle' : a ≤ ((p : ℝ) + 1) / q * a₀ := by
      rw [div_mul_eq_mul_div, le_div_iff₀ hqR]
      calc a * q = a / a₀ * q * a₀ := by field_simp
        _ ≤ ((p : ℝ) + 1) * a₀ := mul_le_mul_of_nonneg_right hpb.le ha₀pos.le
    have hqa0 : a₀ / q < 1 - a := by
      rw [div_lt_iff₀ hqR]
      rw [div_lt_iff₀ h1a, mul_comm] at hqQ1
      linarith
    have hr'1 : ((p : ℝ) + 1) / q * a₀ ≤ 1 := by
      have hple : (p : ℝ) + 1 ≤ a / a₀ * q + 1 := by linarith
      have hstep : ((p : ℝ) + 1) / q * a₀ ≤ (a / a₀ * q + 1) / q * a₀ := by
        gcongr
      have heq : (a / a₀ * q + 1) / q * a₀ = a + a₀ / q := by field_simp
      rw [heq] at hstep
      linarith
    have hr'1' : ((p + 1 : ℕ) : ℝ) / q * a₀ ≤ 1 := by push_cast; linarith [hr'1]
    have hp0 : (0 : ℝ) ≤ (p : ℝ) / q * a₀ := by positivity
    have hp0' : (0 : ℝ) ≤ ((p + 1 : ℕ) : ℝ) / q * a₀ := by positivity
    have hpmem : (p : ℝ) / q * a₀ ∈ Set.Icc (0 : ℝ) 1 \ C :=
      ⟨⟨hp0, hrle.trans ha1.le⟩, (hgen p q hq0 (hrle.trans ha1.le)).1⟩
    have hp'mem : ((p + 1 : ℕ) : ℝ) / q * a₀ ∈ Set.Icc (0 : ℝ) 1 \ C :=
      ⟨⟨hp0', hr'1'⟩, (hgen (p + 1) q hq0 hr'1').1⟩
    have hrle'_raw : a ≤ ((p + 1 : ℕ) : ℝ) / q * a₀ := by push_cast; linarith [hrle']
    have hm1 : f ((p : ℝ) / q * a₀) ≤ f a := hmono _ a hpmem hamem hrle
    have hm2 : f a ≤ f (((p + 1 : ℕ) : ℝ) / q * a₀) := hmono a _ hamem hp'mem hrle'_raw
    have hd1 : f ((p : ℝ) / q * a₀) = (p : ℝ) / q * f a₀ := hD4 p q hq0 (hrle.trans ha1.le)
    have hd2 : f (((p + 1 : ℕ) : ℝ) / q * a₀) = ((p + 1 : ℕ) : ℝ) / q * f a₀ :=
      hD4 (p + 1) q hq0 hr'1'
    rw [hfa0] at hd1 hd2
    have hcast : ((p + 1 : ℕ) : ℝ) = (p : ℝ) + 1 := by push_cast; ring
    rw [hcast] at hm2 hd2
    have hd1' : f ((p : ℝ) / q * a₀) = (p : ℝ) / q * a₀ * β := by rw [hd1]; ring
    have hd2' : f (((p : ℝ) + 1) / q * a₀) = ((p : ℝ) + 1) / q * a₀ * β := by rw [hd2]; ring
    have hdiff : ((p : ℝ) + 1) / q * a₀ * β - (p : ℝ) / q * a₀ * β = a₀ * β / q := by
      field_simp; ring
    have hint1 : (p : ℝ) / q * a₀ * β ≤ a * β := mul_le_mul_of_nonneg_right hrle hβ0
    have hint2 : a * β ≤ ((p : ℝ) + 1) / q * a₀ * β := mul_le_mul_of_nonneg_right hrle' hβ0
    have hwidth : |f a - β * a| ≤ a₀ * β / q := by
      rw [abs_le]
      constructor
      · nlinarith [hm1, hm2, hd1', hd2', hint1, hint2, hdiff]
      · nlinarith [hm1, hm2, hd1', hd2', hint1, hint2, hdiff]
    have hfinal : a₀ * β / q < ε := by
      rw [div_lt_iff₀ hqR]
      rw [div_lt_iff₀ hε] at hqQ2
      linarith
    linarith [hwidth, hfinal]
  by_contra hne
  have hpos : 0 < |f a - β * a| := abs_pos.mpr (sub_ne_zero.mpr hne)
  exact absurd (hbound (|f a - β * a| / 2) (by linarith)) (by linarith)

/--
**FR.** **D6.** `f a₀ / a₀ = 1` : triplet `(b, 1-b, 0)` (`htriple`) donne
`f b + f(1-b) = 1` (avec `f 0 = 0`) ; D5 sur `b` et `1-b` (tous deux `< 1`)
donne `β·b + β·(1-b) = β = 1`.

**EN.** **D6.** `f a₀ / a₀ = 1`: the triple `(b, 1-b, 0)` (`htriple`) gives
`f b + f(1-b) = 1` (with `f 0 = 0`); D5 applied to `b` and `1-b` (both `< 1`)
gives `β·b + β·(1-b) = β = 1`.
-/
private theorem warmup_II_D6 {C : Set ℝ} (f : ℝ → ℝ) (hf0 : f 0 = 0)
    (htriple : ∀ a b c, a ∈ Set.Icc (0 : ℝ) 1 \ C → b ∈ Set.Icc (0 : ℝ) 1 \ C →
      c ∈ Set.Icc (0 : ℝ) 1 \ C → a + b + c = 1 → f a + f b + f c = 1)
    {a₀ : ℝ} (hgen : ∀ p q : ℕ, 0 < q → (p : ℝ) / q * a₀ ≤ 1 →
      (p : ℝ) / q * a₀ ∉ C ∧ 1 - (p : ℝ) / q * a₀ ∉ C)
    (hD5 : ∀ a ∈ Set.Ico (0 : ℝ) 1 \ C, f a = (f a₀ / a₀) * a)
    {b : ℝ} (hb : b ∈ Set.Ioo (0 : ℝ) 1) (hbC : b ∉ C) (hbC' : 1 - b ∉ C) :
    f a₀ / a₀ = 1 := by
  have h0C : (0 : ℝ) ∉ C := by simpa using (hgen 0 1 one_pos (by norm_num)).1
  have h0mem : (0 : ℝ) ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨le_refl 0, zero_le_one⟩, h0C⟩
  have hbmem : b ∈ Set.Icc (0 : ℝ) 1 \ C := ⟨⟨hb.1.le, hb.2.le⟩, hbC⟩
  have hb'mem : (1 - b) ∈ Set.Icc (0 : ℝ) 1 \ C :=
    ⟨⟨by linarith [hb.2], by linarith [hb.1]⟩, hbC'⟩
  have htr := htriple b (1 - b) 0 hbmem hb'mem h0mem (by ring)
  rw [hf0] at htr
  have hbIco : b ∈ Set.Ico (0 : ℝ) 1 \ C := ⟨⟨hb.1.le, hb.2⟩, hbC⟩
  have hb'Ico : (1 - b) ∈ Set.Ico (0 : ℝ) 1 \ C :=
    ⟨⟨by linarith [hb.2], by linarith [hb.1]⟩, hbC'⟩
  have hfb := hD5 b hbIco
  have hfb' := hD5 (1 - b) hb'Ico
  rw [hfb, hfb'] at htr
  have hfactor : f a₀ / a₀ * b + f a₀ / a₀ * (1 - b) = f a₀ / a₀ := by ring
  rw [hfactor] at htr
  linarith

/--
**FR.** **D7 / Warmup Theorem II (CKM 1985 §3).** Si `f` est monotone et
« additive-à-1 » sur `[0,1] \ C` (`C` dénombrable, `C ⊆ (0,1)`), avec `f 0 = 0`,
alors `f = id` sur `[0,1] \ C`.

**EN.** **D7 / Warmup Theorem II (CKM 1985 §3).** If `f` is monotone and
"additive-to-1" on `[0,1] \ C` (`C` countable, `C ⊆ (0,1)`), with `f 0 = 0`,
then `f = id` on `[0,1] \ C`.
-/
theorem warmup_II (C : Set ℝ) (hC : C.Countable) (hCsub : C ⊆ Set.Ioo (0 : ℝ) 1) (f : ℝ → ℝ)
    (hf0 : f 0 = 0)
    (hmono : ∀ a b, a ∈ Set.Icc (0 : ℝ) 1 \ C → b ∈ Set.Icc (0 : ℝ) 1 \ C → a ≤ b → f a ≤ f b)
    (htriple : ∀ a b c, a ∈ Set.Icc (0 : ℝ) 1 \ C → b ∈ Set.Icc (0 : ℝ) 1 \ C →
      c ∈ Set.Icc (0 : ℝ) 1 \ C → a + b + c = 1 → f a + f b + f c = 1) :
    ∀ a ∈ Set.Icc (0 : ℝ) 1 \ C, f a = a := by
  have hD1 := warmup_II_D1 hCsub f hf0 htriple
  obtain ⟨a₀, ha₀, hgen⟩ := warmup_II_D2 hC hCsub
  have hD4 := warmup_II_D4 f hf0 htriple ha₀ hgen
  have hD5 := warmup_II_D5 f hf0 hmono ha₀ hgen hD4
  obtain ⟨b, hb, hbC, hbC'⟩ := warmup_II_D6_exists hC
  have hβ := warmup_II_D6 f hf0 htriple hgen hD5 hb hbC hbC'
  intro a ha
  obtain ⟨ha01, haC⟩ := ha
  rcases ha01.2.lt_or_eq with hlt | heq
  · have haIco : a ∈ Set.Ico (0 : ℝ) 1 \ C := ⟨⟨ha01.1, hlt⟩, haC⟩
    rw [hD5 a haIco, hβ, one_mul]
  · rw [heq]; exact hD1

end Gleason
