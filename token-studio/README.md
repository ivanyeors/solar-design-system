# Solar Design System Token Studio

This directory contains tools for managing design tokens in the Solar Design System.

## Token Generation

The token generation script processes the tokens.json file and splits it into separate SCSS token files.

### Running the Script

To generate tokens, run:

```bash
# From the token-studio directory
python split_tokens.py
```

### Token Types and Structure

The script handles different token types as follows:

1. **Color Tokens**:
   - Primitive color tokens (e.g., `$color-primary-500`) are stored in option-tokens directory
   - Semantic color tokens (e.g., `--color-text-brand`) are stored in semantic-tokens directory

2. **Typography Tokens**:
   - All typography tokens are stored in option-tokens directory

3. **Scale Tokens**:
   - All scale tokens are stored in option-tokens directory

4. **Component Tokens**:
   - All component tokens (bruhealth, evydcore) are stored in semantic-tokens directory

### File Structure

The script generates the following files:

- `_colors_light.scss` - Light theme color tokens
- `_colors_dark.scss` - Dark theme color tokens
- `_typography.scss` - Typography tokens
- `_scale.scss` - Scale tokens
- `_bruhealth.scss` - BruHealth component tokens
- `_evydcore.scss` - EVYD Core component tokens 