# Wardrobe

A personal outfit planner: outfits for spring, summer, autumn and winter, made from clothes I already own plus pieces worth buying. Each piece has a photo, price and shop link.

- **`outfits-autumn-winter-2026.html`**: the page. Open it in any browser. Product photos load from the shops' websites.
- **`builder/`**: the script and data that generate the page.
  - `owned.json`: clothes I already own.
  - `products_*.json`: researched pieces to buy.
- **`img/`**: photos that aren't hosted online.

## Rebuild the page

```bash
cd builder && python3 build_outfits.py
```
