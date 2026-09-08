#!/usr/bin/env python3
"""Generates themes/*.json from one spec per variant.

    python3 tool/build_themes.py

Two variants share every structural decision and differ only in a palette, so a
tweak lands in both instead of drifting between hand-edited 260-key files.
Contrast is asserted at build time: nothing ships below 4.5:1 on its own
background, which is the bar the site palette set for itself.
"""
import json, pathlib, sys, colorsys

FLOOR = 4.5

def _lum(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def contrast(fg, bg):
    a, b = _lum(fg), _lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

def hsv(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    x, s, v = colorsys.rgb_to_hsv(r, g, b)
    return x * 360, s * 100, v * 100

def A(hex6, a):
    return f"{hex6}{round(a * 255):02X}"


class P(dict):
    __getattr__ = dict.__getitem__


# ---------------------------------------------------------------------------
# Terminal — green-dominant, the way a hacked-together CRT actually looks.
#
# The impression has to read GREEN at a glance, so green carries the bulk of any
# file: the ground, ordinary identifiers, function names, strings. Everything
# else is a spark. Keywords take hot pink because that is the one hue no green
# screen ever had and it is what makes this read as retro rather than as a
# monochrome terminal; types cyan, numbers orange, annotations violet.
#
# Italics are load-bearing, not decoration: comments, keywords, storage,
# annotations, parameters and `this` are all things you skim past or read as
# structure, and slanting them separates them without spending another hue.
TERMINAL = P(
    id="ds_retro", name="ds_retro",
    bg="#050A08", surface="#080F0D", card="#0C1713",
    line="#16281F", line_hi="#254237", field="#44796A",
    text="#C9F0DC", dim="#8FC4AC", muted="#6F9C89", faint="#5A8574",
    accent="#3DDC97",
    keyword="#FF6AC1", kw_style="italic",
    storage="#FF6AC1", st_style="italic",
    function="#3DDC97",
    type="#4FC3E8",
    string="#B8E986",
    escape="#2CC5C0",
    number="#FF9E64",
    constant="#FF9E64",
    variable="#C9F0DC",
    prop="#7BD4F0",
    param="#8FC4AC", param_style="italic",
    punct="#6F9C89",
    comment="#5A8574", cm_style="italic",
    anno="#C792EA", anno_style="italic",
    tag="#FF6AC1", attr="#3DDC97",
    warn="#F7D07B", err="#F0837A",
    brackets=["#3DDC97", "#FF6AC1", "#4FC3E8", "#FF9E64", "#C792EA", "#B8E986"],
    ansi_magenta="#FF6AC1", ansi_blue="#4FC3E8", ansi_yellow="#F7D07B",
)

# ---------------------------------------------------------------------------
# Terminal Phosphor — one gun, one colour.
#
# A P1 monitor could not show six hues, and that constraint is most of what
# "retro" means to anyone who used one. Everything is a lightness step of the
# same green except amber, standing in for the bright attribute those terminals
# actually had. Legibility comes from value rather than hue, which is how they
# worked. Kept for when the colourful one is too much for a long session.
PHOSPHOR = P(
    id="ds_retro-phosphor", name="ds_retro Phosphor",
    bg="#040807", surface="#070E0C", card="#0B1411",
    line="#14251F", line_hi="#223E35", field="#3E7263",
    text="#D6F5E4", dim="#8FC4AC", muted="#6F9C89", faint="#578573",
    accent="#3DDC97",
    keyword="#D9B26A", kw_style="italic",
    storage="#D9B26A", st_style="italic",
    function="#3DDC97",
    type="#7FE9C2",
    string="#B4E8C8",
    escape="#7FE9C2",
    number="#D9B26A",
    constant="#D9B26A",
    variable="#D6F5E4",
    prop="#A9E0C6",
    param="#8FC4AC", param_style="italic",
    punct="#6F9C89",
    comment="#578573", cm_style="italic",
    anno="#8FC4AC", anno_style="italic",
    tag="#7FE9C2", attr="#3DDC97",
    warn="#D9B26A", err="#F0837A",
    brackets=["#3DDC97", "#7FE9C2", "#B4E8C8", "#8FC4AC", "#D9B26A", "#6F9C89"],
    ansi_magenta="#A9E0C6", ansi_blue="#7FE9C2", ansi_yellow="#D9B26A",
)


def workbench(p):
    return {
      "foreground": p.text, "focusBorder": A(p.accent, .45),
      "selection.background": A(p.accent, .30), "descriptionForeground": p.muted,
      "errorForeground": p.err, "widget.shadow": "#00000099",
      "icon.foreground": p.dim, "sash.hoverBorder": A(p.accent, .50),
      "editor.background": p.bg, "editor.foreground": p.text,
      "editorLineNumber.foreground": p.faint,
      "editorLineNumber.activeForeground": p.accent,
      "editorCursor.foreground": p.accent, "editorCursor.background": p.bg,
      # Selection inverts to a solid block. It is the single most terminal
      # thing an editor can do, and a translucent wash is the modern habit
      # this theme is trying not to have.
      "editor.selectionBackground": A(p.accent, .30),
      "editor.selectionHighlightBackground": A(p.accent, .13),
      "editor.inactiveSelectionBackground": A(p.accent, .10),
      "editor.wordHighlightBackground": A(p.type, .14),
      "editor.wordHighlightStrongBackground": A(p.type, .20),
      "editor.findMatchBackground": A(p.number, .36),
      "editor.findMatchHighlightBackground": A(p.number, .20),
      "editor.findRangeHighlightBackground": A(p.accent, .08),
      "editor.hoverHighlightBackground": A(p.type, .10),
      "editor.lineHighlightBackground": p.surface,
      "editor.lineHighlightBorder": "#00000000",
      "editorLink.activeForeground": p.type,
      "editorWhitespace.foreground": p.line,
      "editorIndentGuide.background1": p.line,
      "editorIndentGuide.activeBackground1": A(p.accent, .32),
      "editorRuler.foreground": p.line,
      "editorCodeLens.foreground": p.muted,
      "editorBracketMatch.background": A(p.accent, .16),
      "editorBracketMatch.border": A(p.accent, .60),
      "editorOverviewRuler.border": "#00000000",
      "editorOverviewRuler.findMatchForeground": A(p.number, .70),
      "editorOverviewRuler.errorForeground": p.err,
      "editorOverviewRuler.warningForeground": p.warn,
      "editorOverviewRuler.infoForeground": p.type,
      "editorError.foreground": p.err, "editorWarning.foreground": p.warn,
      "editorInfo.foreground": p.type,
      "editorGutter.background": p.bg,
      "editorGutter.addedBackground": p.accent,
      "editorGutter.modifiedBackground": p.type,
      "editorGutter.deletedBackground": p.err,
      "problemsErrorIcon.foreground": p.err,
      "problemsWarningIcon.foreground": p.warn,
      "problemsInfoIcon.foreground": p.type,
      **{f"editorBracketHighlight.foreground{i+1}": c for i, c in enumerate(p.brackets)},
      "editorBracketHighlight.unexpectedBracket.foreground": p.err,
      "titleBar.activeBackground": p.bg, "titleBar.activeForeground": p.text,
      "titleBar.inactiveBackground": p.bg, "titleBar.inactiveForeground": p.muted,
      "titleBar.border": p.line,
      "activityBar.background": p.bg, "activityBar.foreground": p.accent,
      "activityBar.inactiveForeground": p.faint, "activityBar.border": p.line,
      "activityBarBadge.background": p.accent, "activityBarBadge.foreground": p.bg,
      "activityBar.activeBorder": p.accent,
      "sideBar.background": p.surface, "sideBar.foreground": p.dim,
      "sideBar.border": p.line, "sideBarTitle.foreground": p.text,
      "sideBarSectionHeader.background": p.surface,
      "sideBarSectionHeader.foreground": p.text,
      "sideBarSectionHeader.border": p.line,
      "editorGroup.border": p.line,
      "editorGroupHeader.tabsBackground": p.surface,
      "editorGroupHeader.tabsBorder": p.line,
      "editorGroupHeader.noTabsBackground": p.surface,
      "tab.activeBackground": p.bg, "tab.activeForeground": p.text,
      "tab.activeBorderTop": p.accent, "tab.activeBorder": p.bg,
      "tab.inactiveBackground": p.surface, "tab.inactiveForeground": p.muted,
      "tab.border": p.line, "tab.hoverBackground": p.card,
      "tab.unfocusedActiveBorderTop": p.line_hi,
      "statusBar.background": p.bg, "statusBar.foreground": p.dim,
      "statusBar.border": p.line, "statusBar.noFolderBackground": p.bg,
      "statusBar.debuggingBackground": p.accent,
      "statusBar.debuggingForeground": p.bg,
      "statusBarItem.remoteBackground": p.card,
      "statusBarItem.remoteForeground": p.accent,
      "statusBarItem.hoverBackground": A(p.accent, .12),
      "statusBarItem.errorBackground": p.err, "statusBarItem.errorForeground": p.bg,
      "statusBarItem.warningBackground": p.warn, "statusBarItem.warningForeground": p.bg,
      "panel.background": p.surface, "panel.border": p.line,
      "panelTitle.activeForeground": p.text, "panelTitle.activeBorder": p.accent,
      "panelTitle.inactiveForeground": p.muted, "panelSection.border": p.line,
      "breadcrumb.background": p.bg, "breadcrumb.foreground": p.muted,
      "breadcrumb.focusForeground": p.text,
      "breadcrumb.activeSelectionForeground": p.accent,
      "breadcrumbPicker.background": p.card,
      "minimap.background": p.bg,
      "minimap.findMatchHighlight": A(p.number, .70),
      "minimap.selectionHighlight": A(p.accent, .50),
      "minimap.errorHighlight": p.err,
      "minimapSlider.background": A(p.accent, .09),
      "minimapSlider.hoverBackground": A(p.accent, .16),
      "minimapSlider.activeBackground": A(p.accent, .24),
      "scrollbar.shadow": "#00000000",
      "scrollbarSlider.background": A(p.accent, .10),
      "scrollbarSlider.hoverBackground": A(p.accent, .18),
      "scrollbarSlider.activeBackground": A(p.accent, .26),
      "list.activeSelectionBackground": A(p.accent, .18),
      "list.activeSelectionForeground": p.text,
      "list.inactiveSelectionBackground": A(p.accent, .10),
      "list.inactiveSelectionForeground": p.text,
      "list.hoverBackground": A(p.accent, .07), "list.hoverForeground": p.text,
      "list.highlightForeground": p.accent, "list.focusOutline": A(p.accent, .45),
      "list.errorForeground": p.err, "list.warningForeground": p.warn,
      "tree.indentGuidesStroke": p.line,
      "input.background": p.surface, "input.foreground": p.text,
      "input.border": p.field, "input.placeholderForeground": p.muted,
      "inputOption.activeBorder": p.accent,
      "inputOption.activeBackground": A(p.accent, .14),
      "inputValidation.errorBackground": "#2A1210", "inputValidation.errorBorder": p.err,
      "inputValidation.warningBackground": "#2A2110", "inputValidation.warningBorder": p.warn,
      "inputValidation.infoBackground": "#0E2029", "inputValidation.infoBorder": p.type,
      "dropdown.background": p.card, "dropdown.foreground": p.text,
      "dropdown.border": p.field, "dropdown.listBackground": p.card,
      "button.background": p.accent, "button.foreground": p.bg,
      "button.hoverBackground": p.string,
      "button.secondaryBackground": p.card, "button.secondaryForeground": p.text,
      "button.secondaryHoverBackground": p.line,
      "checkbox.background": p.surface, "checkbox.border": p.field,
      "checkbox.foreground": p.accent,
      "badge.background": p.accent, "badge.foreground": p.bg,
      "progressBar.background": p.accent,
      "quickInput.background": p.card, "quickInput.foreground": p.text,
      "quickInputList.focusBackground": A(p.accent, .18),
      "quickInputList.focusForeground": p.text,
      "pickerGroup.foreground": p.accent, "pickerGroup.border": p.line,
      "keybindingLabel.background": p.surface, "keybindingLabel.foreground": p.dim,
      "keybindingLabel.border": p.line, "keybindingLabel.bottomBorder": p.line,
      "editorWidget.background": p.card, "editorWidget.foreground": p.text,
      "editorWidget.border": p.line_hi,
      "editorSuggestWidget.background": p.card,
      "editorSuggestWidget.border": p.line_hi,
      "editorSuggestWidget.foreground": p.text,
      "editorSuggestWidget.highlightForeground": p.accent,
      "editorSuggestWidget.selectedBackground": A(p.accent, .18),
      "editorSuggestWidget.focusHighlightForeground": p.accent,
      "editorHoverWidget.background": p.card, "editorHoverWidget.border": p.line_hi,
      "debugExceptionWidget.background": "#2A1210", "debugExceptionWidget.border": p.err,
      "peekView.border": p.accent, "peekViewEditor.background": p.surface,
      "peekViewEditor.matchHighlightBackground": A(p.number, .30),
      "peekViewResult.background": p.card,
      "peekViewResult.selectionBackground": A(p.accent, .18),
      "peekViewResult.lineForeground": p.text,
      "peekViewResult.fileForeground": p.dim,
      "peekViewResult.matchHighlightBackground": A(p.number, .30),
      "peekViewTitle.background": p.card, "peekViewTitleLabel.foreground": p.text,
      "peekViewTitleDescription.foreground": p.muted,
      "notificationCenterHeader.background": p.card,
      "notifications.background": p.card, "notifications.border": p.line,
      "notificationLink.foreground": p.type,
      "notificationsErrorIcon.foreground": p.err,
      "notificationsWarningIcon.foreground": p.warn,
      "notificationsInfoIcon.foreground": p.type,
      "menu.background": p.card, "menu.foreground": p.text,
      "menu.border": p.line_hi, "menu.selectionBackground": A(p.accent, .18),
      "menu.selectionForeground": p.text, "menu.separatorBackground": p.line,
      "menubar.selectionBackground": A(p.accent, .14),
      "gitDecoration.addedResourceForeground": p.accent,
      "gitDecoration.modifiedResourceForeground": p.type,
      "gitDecoration.deletedResourceForeground": p.err,
      "gitDecoration.untrackedResourceForeground": p.string,
      "gitDecoration.ignoredResourceForeground": p.faint,
      "gitDecoration.conflictingResourceForeground": p.warn,
      "diffEditor.insertedTextBackground": A(p.accent, .12),
      "diffEditor.removedTextBackground": A(p.err, .12),
      "diffEditor.insertedLineBackground": A(p.accent, .08),
      "diffEditor.removedLineBackground": A(p.err, .08),
      "diffEditor.border": p.line,
      "merge.currentHeaderBackground": A(p.accent, .28),
      "merge.currentContentBackground": A(p.accent, .12),
      "merge.incomingHeaderBackground": A(p.type, .28),
      "merge.incomingContentBackground": A(p.type, .12),
      "terminal.background": p.bg, "terminal.foreground": p.text,
      "terminalCursor.foreground": p.accent, "terminalCursor.background": p.bg,
      "terminal.selectionBackground": A(p.accent, .28), "terminal.border": p.line,
      "terminal.ansiBlack": p.surface, "terminal.ansiRed": p.err,
      "terminal.ansiGreen": p.accent, "terminal.ansiYellow": p.ansi_yellow,
      "terminal.ansiBlue": p.ansi_blue, "terminal.ansiMagenta": p.ansi_magenta,
      "terminal.ansiCyan": p.escape, "terminal.ansiWhite": p.text,
      "terminal.ansiBrightBlack": p.muted, "terminal.ansiBrightRed": "#FF9E96",
      "terminal.ansiBrightGreen": p.string, "terminal.ansiBrightYellow": "#EBC98A",
      "terminal.ansiBrightBlue": "#7BD4F0", "terminal.ansiBrightMagenta": "#F5A9DC",
      "terminal.ansiBrightCyan": "#5FDCD8", "terminal.ansiBrightWhite": "#FFFFFF",
      "settings.headerForeground": p.text, "settings.modifiedItemIndicator": p.accent,
      "textLink.foreground": p.type, "textLink.activeForeground": p.accent,
      "textCodeBlock.background": p.card, "textPreformat.foreground": p.string,
      "textBlockQuote.background": p.surface, "textBlockQuote.border": p.accent,
      "walkThrough.embeddedEditorBackground": p.surface,
      "welcomePage.tileBackground": p.card, "welcomePage.tileBorder": p.line,
      "welcomePage.progress.foreground": p.accent,
    }


def tokens(p):
    def r(name, scope, fg=None, style=None):
        s = {}
        if fg: s["foreground"] = fg
        if style: s["fontStyle"] = style
        return {"name": name, "scope": scope, "settings": s}
    return [
      r("Comment", ["comment", "punctuation.definition.comment", "string.comment"],
        p.comment, p.cm_style),
      r("Doc comment", ["comment.block.documentation", "comment.documentation"],
        p.muted, p.cm_style),
      r("Keyword", ["keyword", "keyword.control", "keyword.other",
                    "keyword.operator.new", "keyword.operator.expression",
                    "keyword.operator.logical", "constant.language.null",
                    "constant.language.undefined"], p.keyword, p.kw_style),
      r("Storage / modifier", ["storage", "storage.type", "storage.modifier",
                               "keyword.declaration"], p.storage, p.st_style),
      r("This / super", ["variable.language.this", "variable.language.super",
                         "variable.language.self"], p.keyword, "italic"),
      r("Function", ["entity.name.function", "support.function",
                     "meta.function-call", "meta.function-call.generic",
                     "entity.name.function.member", "variable.function"], p.function),
      r("Method declaration", ["entity.name.method",
                               "meta.definition.method entity.name.function"], p.function),
      r("Type / class", ["entity.name.type", "entity.name.class",
                         "entity.other.inherited-class", "support.type",
                         "support.class", "entity.name.namespace",
                         "entity.name.type.class", "entity.name.type.interface",
                         "entity.name.type.enum", "meta.type.annotation"], p.type),
      r("String", ["string", "string.quoted", "string.template",
                   "punctuation.definition.string"], p.string),
      r("String escape / interpolation",
        ["constant.character.escape", "punctuation.definition.template-expression",
         "meta.embedded.line", "punctuation.section.embedded"], p.escape),
      r("Regex", ["string.regexp", "constant.other.character-class.regexp"], p.escape),
      r("Number", ["constant.numeric"], p.number),
      r("Constant", ["constant.language.boolean", "constant.language", "constant.other",
                     "support.constant", "variable.other.constant",
                     "entity.name.constant"], p.constant),
      r("Variable", ["variable", "variable.other", "variable.other.readwrite",
                     "meta.definition.variable entity.name.function"], p.variable),
      r("Property", ["variable.other.property", "variable.other.object.property",
                     "meta.object-literal.key", "support.variable.property"], p.prop),
      r("Parameter", ["variable.parameter", "meta.parameter"], p.param, p.param_style),
      r("Operator / punctuation", ["keyword.operator", "punctuation",
                                   "punctuation.separator", "punctuation.terminator",
                                   "punctuation.accessor", "meta.brace"], p.punct),
      r("Annotation / decorator", ["meta.decorator", "entity.name.function.decorator",
                                   "storage.type.annotation", "meta.annotation",
                                   "punctuation.definition.annotation"],
        p.anno, p.anno_style),
      r("Tag", ["entity.name.tag", "punctuation.definition.tag"], p.tag),
      r("Attribute", ["entity.other.attribute-name"], p.attr, "italic"),
      r("JSON / YAML key", ["support.type.property-name.json",
                            "support.type.property-name", "entity.name.tag.yaml"], p.prop),
      r("Markup heading", ["markup.heading", "entity.name.section"], p.function, "bold"),
      r("Markup bold", ["markup.bold"], p.text, "bold"),
      r("Markup italic", ["markup.italic"], p.text, "italic"),
      r("Markup link", ["markup.underline.link", "string.other.link"], p.type, "underline"),
      r("Markup code", ["markup.inline.raw", "markup.fenced_code", "markup.raw"], p.string),
      r("Markup quote", ["markup.quote"], p.muted, "italic"),
      r("Markup list", ["markup.list punctuation.definition.list",
                        "beginning.punctuation.definition.list"], p.accent),
      r("Markup inserted", ["markup.inserted"], p.accent),
      r("Markup deleted", ["markup.deleted"], p.err),
      r("Markup changed", ["markup.changed"], p.type),
      r("Invalid", ["invalid", "invalid.illegal"], "#FFB3AC"),
      r("Deprecated", ["invalid.deprecated"], p.warn, "strikethrough"),
    ]


def semantic(p):
    it = lambda c: {"foreground": c, "fontStyle": "italic"}
    return {
      "class": p.type, "enum": p.type, "interface": p.type, "struct": p.type,
      "type": p.type, "typeParameter": p.escape, "namespace": p.type,
      "function": p.function, "method": p.function,
      "variable": p.variable, "property": p.prop,
      "parameter": it(p.param),
      "enumMember": p.constant, "keyword": it(p.keyword),
      "string": p.string, "number": p.number,
      "comment": it(p.comment),
      "annotation": it(p.anno), "macro": it(p.anno),
      "variable.readonly": p.constant, "property.readonly": p.prop,
      "*.declaration": {"bold": True}, "*.deprecated": {"strikethrough": True},
    }


def build(p):
    colors = workbench(p)
    theme = {"$schema": "vscode://schemas/color-theme", "name": p.name,
             "type": "dark", "semanticHighlighting": True,
             "colors": colors, "semanticTokenColors": semantic(p),
             "tokenColors": tokens(p)}
    out = pathlib.Path("themes") / f"{p.id}-color-theme.json"
    out.write_text(json.dumps(theme, indent=2) + "\n")

    roles = [("comment", p.comment), ("keyword", p.keyword), ("function", p.function),
             ("type", p.type), ("string", p.string), ("number", p.number),
             ("variable", p.variable), ("property", p.prop), ("parameter", p.param),
             ("punctuation", p.punct), ("annotation", p.anno),
             ("line number", p.faint)]
    print(f"\n  {p.name}  ->  {out}")
    print(f"  {'role':<14} {'hex':<9} {'on bg':>8}  {'hue':>4} {'sat':>4}")
    worst = (99, "")
    for n, c in roles:
        ct = contrast(c, p.bg); h, s, _ = hsv(c)
        if ct < worst[0]: worst = (ct, n)
        flag = "AAA" if ct >= 7 else ("AA" if ct >= FLOOR else "FAIL")
        print(f"  {n:<14} {c}  {ct:6.2f}:1  {h:4.0f} {s:4.0f}  {flag}")
    print(f"  distinct hues in syntax: "
          f"{len({round(hsv(c)[0]/12) for _, c in roles if hsv(c)[1] > 15})}")
    print(f"  worst: {worst[1]} at {worst[0]:.2f}:1")
    return worst


if __name__ == "__main__":
    pathlib.Path("themes").mkdir(exist_ok=True)
    fails = []
    for p in (TERMINAL, PHOSPHOR):
        ct, role = build(p)
        if ct < FLOOR:
            fails.append(f"{p.name}: {role} at {ct:.2f}:1")
    if fails:
        print("\n  BELOW THE 4.5 FLOOR — not shipping:")
        for f in fails: print("   ", f)
        sys.exit(1)
    print(f"\n  both variants clear {FLOOR}:1 on every syntax role")
