// =============================================================================
// MathJax configuration for the ASSIP 2026 wiki
// -----------------------------------------------------------------------------
// Material for MkDocs ships with MathJax 3 (loaded via the `extra_javascript`
// CDN entry in mkdocs.yml). We pair it with `pymdownx.arithmatex` in
// `generic: true` mode so authors can write `$...$`, `\(...\)`, `$$...$$`,
// or `\[...\]` directly in markdown.
//
// If we later swap to KaTeX, the wiring is similar — just change the CDN URL
// in `mkdocs.yml` and replace the body of this file with a KaTeX auto-render
// snippet. For now, MathJax is the Material-recommended default.
// =============================================================================

window.MathJax = {
  tex: {
    inlineMath:  [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true,
    tags: "ams",
    macros: {
      // Common shorthands used across the empirical-finance chapters
      E:       "\\mathbb{E}",
      Var:     "\\mathrm{Var}",
      Cov:     "\\mathrm{Cov}",
      Corr:    "\\mathrm{Corr}",
      sd:      "\\mathrm{sd}",
      argmin:  "\\mathop{\\mathrm{arg\\,min}}",
      argmax:  "\\mathop{\\mathrm{arg\\,max}}",
      R:       "\\mathbb{R}",
      // Returns / risk
      RF:      ["R_{f,#1}", 1],
      RM:      ["R_{m,#1}", 1],
    }
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  },
  loader: {
    load: ["[tex]/ams"]
  }
};

// -----------------------------------------------------------------------------
// Re-typeset on Material's instant-navigation page changes so math renders
// correctly when readers click around without a full reload.
// -----------------------------------------------------------------------------
document$.subscribe(() => {
  if (typeof MathJax !== "undefined" && MathJax.typesetPromise) {
    MathJax.startup.output.clearCache?.();
    MathJax.typesetClear?.();
    MathJax.texReset?.();
    MathJax.typesetPromise();
  }
});
