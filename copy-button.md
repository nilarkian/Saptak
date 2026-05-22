# Copy Button Feature: Table to PNG

## Overview

Tables in note-layout render with a "📷 copy" button that converts the table to a PNG image and copies it to clipboard. Enables quick sharing of table data as images.

## Implementation

### HTML Library
- External: `html-to-image` (unpkg CDN) at line 871
- Converts DOM elements to image blobs

### JavaScript Logic (lines 728–779)

```javascript
document.querySelectorAll('.note-body table').forEach(table => {
  const wrapper = table.parentElement;  // .table-scroll-wrapper
  
  const btn = document.createElement('button');
  btn.className = 'table-copy-btn';
  btn.textContent = '📷 copy';
  
  btn.addEventListener('click', async () => {
    try {
      const blob = await htmlToImage.toBlob(table, {
        pixelRatio: 6,                    // High DPI (6x)
        skipFonts: false,                 // Include embedded fonts
        cacheBust: true,                  // Force fresh render
        backgroundColor: document.body.classList.contains('dark')
          ? '#1e1e1e'                     // Dark mode bg
          : '#f7f7f7'                     // Light mode bg
      });
      
      await navigator.clipboard.write([
        new ClipboardItem({
          'image/png': blob
        })
      ]);
      
      btn.textContent = '✓ Copied';
      setTimeout(() => {
        btn.textContent = '📷 copy';
      }, 1500);
      
    } catch (err) {
      console.error(err);
      btn.textContent = '✗ Failed';
      setTimeout(() => {
        btn.textContent = '📷 copy';
      }, 1500);
    }
  });
  
  wrapper.appendChild(btn);  // Add button to scroll wrapper
});
```

### Styling (lines 343–372)

```css
.table-copy-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  
  background: #111;
  color: #f7f7f7;
  
  border: none;
  border-radius: 6px;
  
  padding: 6px 12px;
  
  font-family: 'Syne', Arial, sans-serif;
  font-size: 11px;
  font-weight: 600;
  
  cursor: pointer;
  z-index: 10;
}

.table-copy-btn:hover {
  opacity: .85;
}

body.dark .table-copy-btn {
  background: #252526;
  color: #d4d4d4;
  border: 1px solid #3e3e42;
}
```

## Key Features

| Feature | Behavior |
|---------|----------|
| **Resolution** | `pixelRatio: 6` (6x pixel density for crisp copying) |
| **Dark Mode** | Detects `body.dark` class; sets matching background color |
| **Position** | Absolute positioned in top-right of `.table-scroll-wrapper` |
| **Visual Feedback** | Text changes to "✓ Copied" / "✗ Failed" for 1.5 seconds |
| **Fonts** | `skipFonts: false` — preserves EB Garamond, Syne in output image |
| **Clipboard API** | Uses modern `navigator.clipboard.write()` with `ClipboardItem` |

## Assumptions & Dependencies

- **Browser Support**: Requires Clipboard API (not IE11)
- **Library**: `html-to-image@1.x` (loaded from CDN at runtime)
- **DOM Structure**: Tables must be wrapped in `.table-scroll-wrapper` (added by separate script at lines 720–725)
- **CSS**: Dark mode styling requires `body.dark` class (managed by theme toggle, lines 657–681)

## Related Code

- **Table Wrapper Creation** (lines 720–725): Wraps all `.note-body table` in `<div class="table-scroll-wrapper">`
- **Code Copy Button** (lines 781–818): Separate implementation for `<pre>` blocks (text-to-clipboard, not image)
- **Theme Toggle** (lines 657–681): Manages `body.dark` class that sets background color for PNG
