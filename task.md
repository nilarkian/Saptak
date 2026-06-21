I found the culprit.

The extra space on the right is coming from this export code, not from Mermaid itself: 

```js
var PAD = 36;

var exportW = Math.round(rect.width) + PAD * 2;
var exportH = Math.round(rect.height) + PAD * 2;

mermaidDiv.style.cssText = [
  ...
  'padding:' + PAD + 'px',
  ...
].join(';');
```

What's happening:

1. You add `36px` padding left and right.
2. Then you increase capture width by another `72px` (`PAD * 2`).
3. `html-to-image` captures the padded element AND the enlarged canvas.

So the padding is effectively being counted twice.

Result:

```text
actual diagram
+ 36px left padding
+ 36px right padding
+ another 36px left export area
+ another 36px right export area
```

That produces the large blank margins visible in your screenshot.

The most suspicious line is:

```js
width: exportW,
height: exportH
```

because `mermaidDiv` already became larger after:

```js
padding:36px;
box-sizing:content-box;
```

The export dimensions are being manually enlarged again.

Try:

```js
var exportW = mermaidDiv.offsetWidth;
var exportH = mermaidDiv.offsetHeight;
```

or simply remove:

```js
width: exportW,
height: exportH
```

from:

```js
blob = await htmlToImage.toBlob(mermaidDiv, {
  pixelRatio: 2,
  cacheBust: true,
  fontEmbedCSS: fontCSS || undefined,
  backgroundColor: isDark ? '#1a1a1c' : '#e8e8e4'
});
```

A second possibility is Mermaid itself generating a wider SVG viewport than the visible content. To verify:

```js
console.log(
  mermaidDiv.querySelector('svg').viewBox.baseVal.width,
  mermaidDiv.querySelector('svg').getBBox().width
);
```

If:

```text
viewBox width >> bbox width
```

then Mermaid is the source.

If:

```text
viewBox width ≈ bbox width
```

then the export code is the source.

From the screenshot, I would put the odds at:

```text
90% exportW/exportH + padding double-counting
10% Mermaid SVG viewport
```

because the blank area appears symmetrically around the entire diagram rather than only around Mermaid nodes.
