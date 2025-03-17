import json
import os

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def save_json(data, filepath):
    """Save data to JSON file with pretty printing, overwriting if exists"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def json_to_scss_var(key, value, prefix=''):
    """Convert JSON token to SCSS variable"""
    if isinstance(value, dict):
        if 'value' in value:
            # Handle direct value tokens
            scss_key = f'{prefix}-{key}' if prefix else key
            return f'--{scss_key}: {value["value"]};'
        else:
            # Handle nested objects
            scss_vars = []
            new_prefix = f'{prefix}-{key}' if prefix else key
            for k, v in value.items():
                scss_vars.extend(json_to_scss_var(k, v, new_prefix).split('\n'))
            return '\n'.join(scss_vars)
    return ''

def generate_scss_files():
    """Generate SCSS files from JSON tokens"""
    # Create SCSS output directory
    scss_dir = 'src/styles/tokens'
    create_directory(scss_dir)
    
    # Process brand tokens
    brands = ['BruHealth', 'EVYDCore']
    for brand in brands:
        with open(f'tokens/brands/{brand}.json', 'r') as f:
            brand_data = json.load(f)
            
        scss_vars = []
        for category, tokens in brand_data.items():
            for key, value in tokens.items():
                scss_vars.extend(json_to_scss_var(key, value, category).split('\n'))
                
        # Write brand variables
        with open(f'{scss_dir}/_{brand.lower()}.scss', 'w') as f:
            f.write(':root {\n')
            f.write('  // Auto-generated brand variables\n')
            f.write('  ' + '\n  '.join(filter(None, scss_vars)))
            f.write('\n}\n')

    # Process color tokens
    themes = ['Light', 'Dark (WIP)']
    for theme in themes:
        with open(f'tokens/color/{theme}.json', 'r') as f:
            color_data = json.load(f)
            
        scss_vars = []
        for category, tokens in color_data.items():
            for key, value in tokens.items():
                scss_vars.extend(json_to_scss_var(key, value, category).split('\n'))
                
        # Write color variables
        theme_name = 'dark' if 'Dark' in theme else 'light'
        with open(f'{scss_dir}/_colors_{theme_name}.scss', 'w') as f:
            f.write(f'[data-theme="{theme_name}"] {{\n')
            f.write('  // Auto-generated color variables\n')
            f.write('  ' + '\n  '.join(filter(None, scss_vars)))
            f.write('\n}\n')

    # Process font tokens
    with open('tokens/font/option-token.json', 'r') as f:
        font_data = json.load(f)
        
    scss_vars = []
    for category, tokens in font_data['font'].items():
        for key, value in tokens.items():
            scss_vars.extend(json_to_scss_var(key, value, f'font-{category}').split('\n'))
            
    # Write font variables
    with open(f'{scss_dir}/_typography.scss', 'w') as f:
        f.write(':root {\n')
        f.write('  // Auto-generated typography variables\n')
        f.write('  ' + '\n  '.join(filter(None, scss_vars)))
        f.write('\n}\n')

    # Process scale tokens
    with open('tokens/scale/option-token.json', 'r') as f:
        scale_data = json.load(f)
        
    scss_vars = []
    for scale_type, tokens in scale_data.items():
        for key, value in tokens.items():
            scss_vars.extend(json_to_scss_var(key, value, scale_type).split('\n'))
            
    # Write scale variables
    with open(f'{scss_dir}/_scale.scss', 'w') as f:
        f.write(':root {\n')
        f.write('  // Auto-generated scale variables\n')
        f.write('  ' + '\n  '.join(filter(None, scss_vars)))
        f.write('\n}\n')

def split_tokens():
    # Read the original tokens.json file
    with open('tokens.json', 'r', encoding='utf-8') as f:
        tokens = json.load(f)

    # Create main directories
    create_directory('tokens/brands')
    create_directory('tokens/color')
    create_directory('tokens/font')
    create_directory('tokens/scale')

    # Extract and save Light theme colors
    if 'color/Light' in tokens:
        light_colors = tokens['color/Light']
        save_json(light_colors, 'tokens/color/Light.json')

    # Extract and save Dark theme colors
    if 'color/Dark (WIP)' in tokens:
        dark_colors = tokens['color/Dark (WIP)']
        save_json(dark_colors, 'tokens/color/Dark (WIP).json')

    # Extract and save EVYDCore brand tokens
    if 'brands/EVYDCore' in tokens:
        evyd_core = tokens['brands/EVYDCore']
        save_json(evyd_core, 'tokens/brands/EVYDCore.json')

    # Extract and save BruHealth brand tokens
    if 'brands/BruHealth' in tokens:
        bru_health = tokens['brands/BruHealth']
        save_json(bru_health, 'tokens/brands/BruHealth.json')

    # Extract and save font tokens
    if 'font/option-token' in tokens:
        font_tokens = tokens['font/option-token']
        save_json(font_tokens, 'tokens/font/option-token.json')

    # Extract and save scale tokens
    if 'scale/option-token' in tokens:
        scale_tokens = tokens['scale/option-token']
        save_json(scale_tokens, 'tokens/scale/option-token.json')
          
    # Extract and save $metadata
    if '$metadata' in tokens:
        metadata = tokens['$metadata']
        save_json(metadata, 'tokens/$metadata.json')

    # Extract and save $themes
    if '$themes' in tokens:
        themes = tokens['$themes']
        save_json(themes, 'tokens/$themes.json')

    # Check for any remaining tokens not handled
    handled_tokens = {
        '$metadata',
        '$themes', 
        'brands/BruHealth',
        'brands/EVYDCore',
        'color/Dark (WIP)',
        'color/Light',
        'comp',
        'font/option-token',
        'scale/option-token'
    }
    
    remaining_tokens = set(tokens.keys()) - handled_tokens
    if remaining_tokens:
        print("\nWarning: The following tokens were not processed:")
        for token in sorted(remaining_tokens):
            print(f"- {token}")
            
    # Generate SCSS files
    generate_scss_files()
    
    print("Token files and SCSS variables have been generated successfully!")

if __name__ == "__main__":
    split_tokens()