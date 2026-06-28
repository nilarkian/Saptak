; ═══════════════════════════════════════════════════════════════════════════════
; copy-to-linkedin.ahk  —  CopyEngine CDP client v1.0.0
; Transfers all PNG-copyable items (tables + Mermaid diagrams) from a Saptak
; blog note to an open LinkedIn article editor, one image per paste.
; ═══════════════════════════════════════════════════════════════════════════════
;
; REQUIREMENTS
; ─────────────────────────────────────────────────────────────────────────────
; 1. AutoHotkey v2 (https://www.autohotkey.com/download/)
;
; 2. Chrome.ahk v2 by G33kDude — place in the same directory as this file:
;      https://github.com/G33kDude/Chrome.ahk  (use the v2 branch)
;
; 3. Microsoft Edge launched with the remote debugging port:
;      msedge.exe --remote-debugging-port=9222
;    Create a shortcut or run from cmd/PowerShell once per session.
;
; USAGE
; ─────────────────────────────────────────────────────────────────────────────
; 1. Launch Edge with --remote-debugging-port=9222
; 2. Open your blog note in Tab 1
; 3. Open the LinkedIn article editor in Tab 2 (immediately to the right of Tab 1)
; 4. Give focus to the Edge window (click anywhere in it)
; 5. Press Ctrl+Alt+C
;
; The script will:
;   - Find the blog tab (matched by BLOG_PATTERN)
;   - Call CopyEngine.reset() to start a fresh copy session
;   - Loop:  CopyEngine.next() → wait for PNG on clipboard
;            → Ctrl+Tab (blog → LinkedIn)
;            → Ctrl+V  (paste PNG)
;            → wait for LinkedIn upload
;            → Ctrl+Shift+Tab (LinkedIn → blog)
;   - Show progress in a tooltip; show a TrayTip when done
;
; ═══════════════════════════════════════════════════════════════════════════════

#Requires AutoHotkey v2.0
#SingleInstance Force
#Include JSON.ahk      ; must come before Chrome.ahk — Chrome.ahk uses JSON but does not include it
#Include Chrome.ahk

; ─── Configuration ────────────────────────────────────────────────────────────

BLOG_PATTERN    := "/Saptak/notes/"   ; matches both localhost:4000 and nilarkian.github.io
CDP_PORT        := 9222

; Time (ms) to wait after pasting an IMAGE before switching back.
; LinkedIn uploads the PNG to its CDN asynchronously — switching too early loses it.
; Increase if images land missing or out of order.
PASTE_WAIT      := 2500

; Time (ms) to wait after pasting TEXT before switching back.
; Text paste is synchronous — no CDN upload, short wait is sufficient.
TEXT_PASTE_WAIT := 300

; Time (ms) to wait after a tab switch (Ctrl+Tab / Ctrl+Shift+Tab).
; Short — just gives the browser time to focus the new tab.
TAB_SWITCH_WAIT := 350

; ─── Hotkey ───────────────────────────────────────────────────────────────────

^!c:: RunWorkflow()          ; Ctrl+Alt+C triggers the full copy workflow

; ─── Main workflow ────────────────────────────────────────────────────────────

RunWorkflow() {
    global BLOG_PATTERN, CDP_PORT, PASTE_WAIT, TEXT_PASTE_WAIT, TAB_SWITCH_WAIT

    ; Query CDP HTTP endpoint directly — bypasses Chrome.ahk browser detection
    ; which resolves to Chrome.exe and launches the wrong browser.
    ; Whatever browser is on port CDP_PORT is the one we talk to.
    http := ComObject('WinHttp.WinHttpRequest.5.1')
    try {
        http.Open('GET', 'http://127.0.0.1:' CDP_PORT '/json', false)
        http.Send()
    } catch {
        MsgBox(
            "Cannot connect to browser on port " CDP_PORT ".`n`n"
            "Launch Edge with:`n"
            "    msedge.exe --remote-debugging-port=" CDP_PORT,
            "CopyEngine", 0x10
        )
        return
    }

    ; Locate the blog tab by URL pattern
    BlogPage := FindPage(JSON.parse(http.responseText), BLOG_PATTERN)
    if (!BlogPage) {
        MsgBox(
            "No tab found matching:`n    " BLOG_PATTERN "`n`n"
            "Open your blog note in Edge first.",
            "CopyEngine", 0x10
        )
        return
    }

    ; Reset the CopyEngine session (also rebuilds the element queue)
    reset := CdpEval(BlogPage, "CopyEngine.reset()")
    total := reset.totalItems

    if (total = 0) {
        MsgBox(
            "No copyable items found on this page.`n"
            "(Tables and Mermaid diagrams are scanned on page load.)",
            "CopyEngine", 0x40   ; 0x40 = info icon
        )
        return
    }

    ToolTip "CopyEngine: starting " total " item" (total = 1 ? "" : "s") "..."

    ; ── Copy loop ─────────────────────────────────────────────────────────────
    copied := 0

    loop {
        ; Ask the browser to copy the next PNG to the system clipboard
        r := CdpEval(BlogPage, "CopyEngine.next()")

        ; next() failed — check why
        if (!r.success) {
            ; Clean exit: queue exhausted (extra next() after last item returned DONE)
            if (r.state = "DONE")
                break

            ; Actual error
            ToolTip
            errCode := IsObject(r.error) ? r.error.code    : "UNKNOWN"
            errMsg  := IsObject(r.error) ? r.error.message : String(r.error)
            MsgBox(
                "Item " (r.currentIndex + 1) " failed:`n"
                "  Code: " errCode "`n"
                "  " errMsg "`n`n"
                "Fix the issue, then press Ctrl+Alt+C again`n"
                "(the session will reset automatically).",
                "CopyEngine — Error", 0x10
            )
            return
        }

        ; Copy succeeded (state may be READY or DONE — paste either way)
        copied++
        ToolTip(
            "CopyEngine: " copied "/" total
            " — " r.copiedType
            " (" r.durationMs "ms)"
        )

        ; ── Paste into LinkedIn ───────────────────────────────────────────────
        Send "^{Tab}"               ; Switch: blog → LinkedIn (next tab to the right)
        Sleep TAB_SWITCH_WAIT
        Send "^v"                   ; Paste into LinkedIn editor
        if (r.copiedType = "text")
            Sleep TEXT_PASTE_WAIT   ; text paste is synchronous — short wait
        else
            Sleep PASTE_WAIT        ; image paste triggers CDN upload — full wait
        Send "^+{Tab}"              ; Switch: LinkedIn → blog (previous tab)
        Sleep TAB_SWITCH_WAIT
    }

    ToolTip   ; clear tooltip

    TrayTip(
        "CopyEngine",
        "Done — " copied "/" total " item" (copied = 1 ? "" : "s") " transferred to LinkedIn.",
        3   ; display for 3 seconds
    )
}

; ─── Helpers ──────────────────────────────────────────────────────────────────

; Find the first tab whose URL contains Pattern in a CDP page list (Array of Maps).
; Returns a Chrome.Page WebSocket connection, or false if not found.
FindPage(Pages, Pattern) {
    for PageData in Pages {
        if (InStr(PageData['url'], Pattern))
            return Chrome.Page(PageData['webSocketDebuggerUrl'])
    }
    return false
}

; Evaluate a JS expression in the page and await Promise resolution.
; v2 Evaluate() hardcodes awaitPromise:false — unusable for async CopyEngine.next().
; Use Page.Call() directly to pass awaitPromise:true and returnByValue:true.
; Returns an AHK Object (not Map) so callers can use .field dot-access.
CdpEval(Page, Expr) {
    response := Page.Call("Runtime.evaluate", Map(
        "expression",          Expr,
        "awaitPromise",        JSON.true,
        "returnByValue",       JSON.true,
        "userGesture",         JSON.true,
        "includeCommandLineAPI", JSON.false
    ))
    ; response = Map{"result": Map{"type":"object","value": Map{...}}}
    return MapToObj(response['result']['value'])
}

; Recursively convert a JSON Map (from JSON.parse) to an AHK Object
; so callers can use .field dot-access instead of ['field'] Map syntax.
MapToObj(m) {
    if !(m is Map)
        return m
    obj := {}
    for k, v in m
        obj.%k% := MapToObj(v)
    return obj
}

; ═══════════════════════════════════════════════════════════════════════════════
; DESIGN NOTES
; ═══════════════════════════════════════════════════════════════════════════════
;
; WHY Sleep PASTE_WAIT?
;   CopyEngine lives in the blog tab and cannot observe LinkedIn's upload.
;   After ^v, LinkedIn receives a raw PNG blob and uploads it to its CDN
;   asynchronously. If we switch back to the blog before the upload completes,
;   the next CopyEngine.next() may overwrite the clipboard before LinkedIn
;   has finished reading it. Sleep PASTE_WAIT is the only available signal.
;   This is a deliberate, isolated exception to the "no arbitrary sleep" rule.
;
; WHY CDP, NOT KEYBOARD SIMULATION?
;   Browser ↔ AHK communication goes through Chrome DevTools Protocol only.
;   - No focus dependency         (CDP works even when the tab is in background)
;   - No timing heuristics        (awaitPromise: true blocks until PNG is on clipboard)
;   - Structured JSON responses   (success/error/state readable without parsing)
;   - Transport-swappable later   (swap Chrome.ahk for a WebSocket lib; CopyEngine unchanged)
;
; TAB LAYOUT ASSUMPTION:
;   Blog tab must be immediately to the LEFT of the LinkedIn tab.
;   (Ctrl+Tab moves right; Ctrl+Shift+Tab moves left.)
;   Arrange your tabs before pressing Ctrl+Alt+C.
;
; CHROME.AHK COMPATIBILITY:
;   Written against Chrome.ahk v2 (GeekDude/Chrome.ahk, v2 branch).
;   If your version differs:
;   - Constructor:   Chrome("", PORT) — empty path = attach only, no browser launch
;   - GetPageList(): returns array of {id, url, title, type, ...}
;   - GetPage(id):   connects to a specific tab by its CDP target ID
;   - Evaluate(expr, true): Runtime.evaluate with awaitPromise:true, returnByValue:true
;
; ADJUSTING PASTE_WAIT:
;   If images appear missing or land in the wrong order, increase PASTE_WAIT.
;   2500ms covers most LinkedIn upload scenarios on a normal connection.
;   On slow connections try 4000–5000ms.
;
; ═══════════════════════════════════════════════════════════════════════════════
