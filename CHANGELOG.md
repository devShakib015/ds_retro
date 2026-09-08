## 0.1.0

First release. Two variants — **ds_retro**, green-dominant with retro colour
sparks, and **ds_retro Phosphor**, near-monochrome green.

- 258 workbench colours each, 33 TextMate token rules, 24 semantic token rules,
  and the full ANSI set so the integrated terminal matches.
- Semantic highlighting is on and mapped for Dart: enum members read as
  constants, type parameters as their own hue, declarations bold.
- Selection inverts to a solid block rather than a translucent wash.
- Contrast is asserted at build time. `tool/build_themes.py` exits non-zero if
  any syntax role falls below 4.5:1 on its own background; the worst that ships
  is the comment colour at 4.79:1.

Both variants are generated from one spec, so the two cannot drift apart.
