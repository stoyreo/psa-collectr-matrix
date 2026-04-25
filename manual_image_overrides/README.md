# Manual Image Overrides

Escape hatch for cards that fail CDN fetch. Place images here and they will be used instead of network requests.

## Naming Convention

- **PSA cert exceptions** (always failing cards): `psa_<cert>.jpg`
  - Example: `psa_136143757.jpg`
  - Used for PSA cert numbers that consistently fail CloudFront CDN
  
- **Collectr-keyed cards**: `<collectr_pid>.webp`
  - Example: `10010048.webp`
  - Used for Collectr product IDs

## Guidelines

- Any file placed here is used as-is and never overwritten
- Minimum size: **500 bytes**
- Once cached, manual overrides are permanent (no refresh/refetch)
- For PSA cert cards: screenshot from psacard.com or right-click save from PriceCharting
- For Collectr cards: save product image from Collectr marketplace directly

## How to Generate

- **Screenshot**: Open psacard.com or PriceCharting, screenshot the card, save as JPG/WebP
- **Save image**: Right-click image → Save as (JPG/WebP)
- **Scanned slab**: Manually scan your physical PSA slab, save as JPG
