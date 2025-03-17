import json
import os
import sys
from pathlib import Path

def create_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

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

def generate_scss_files(base_dir):
    """Generate SCSS files from JSON tokens"""
    # Create SCSS output directory
    scss_dir = os.path.join(base_dir, 'src', 'styles', 'tokens')
    create_directory(scss_dir)
    
    # Process brand tokens
    brands = ['BruHealth', 'EVYDCore']
    for brand in brands:
        try:
            brand_path = os.path.join(base_dir, 'tokens', 'brands', f'{brand}.json')
            with open(brand_path, 'r') as f:
                brand_data = json.load(f)
                
            scss_vars = []
            for category, tokens in brand_data.items():
                for key, value in tokens.items():
                    scss_vars.extend(json_to_scss_var(key, value, category).split('\n'))
                    
            # Write brand variables
            scss_file = os.path.join(scss_dir, f'_{brand.lower()}.scss')
            with open(scss_file, 'w') as f:
                f.write(':root {\n')
                f.write('  // Auto-generated brand variables\n')
                f.write('  ' + '\n  '.join(filter(None, scss_vars)))
                f.write('\n}\n')
        except FileNotFoundError:
            print(f"Warning: {brand} brand tokens file not found")

    # Process color tokens
    themes = ['Light', 'Dark']
    for theme in themes:
        try:
            color_path = os.path.join(base_dir, 'tokens', 'color', f'{theme}.json')
            with open(color_path, 'r') as f:
                color_data = json.load(f)
                
            scss_vars = []
            for category, tokens in color_data.items():
                for key, value in tokens.items():
                    scss_vars.extend(json_to_scss_var(key, value, category).split('\n'))
                    
            # Write color variables
            theme_name = theme.lower()
            scss_file = os.path.join(scss_dir, f'_colors_{theme_name}.scss')
            with open(scss_file, 'w') as f:
                f.write(f'[data-theme="{theme_name}"] {{\n')
                f.write('  // Auto-generated color variables\n')
                f.write('  ' + '\n  '.join(filter(None, scss_vars)))
                f.write('\n}\n')
        except FileNotFoundError:
            print(f"Warning: {theme} color tokens file not found")

    # Process font tokens
    try:
        font_path = os.path.join(base_dir, 'tokens', 'font', 'option-token.json')
        with open(font_path, 'r') as f:
            font_data = json.load(f)
            
        scss_vars = []
        for category, tokens in font_data['font'].items():
            for key, value in tokens.items():
                scss_vars.extend(json_to_scss_var(key, value, f'font-{category}').split('\n'))
                
        # Write font variables
        scss_file = os.path.join(scss_dir, '_typography.scss')
        with open(scss_file, 'w') as f:
            f.write(':root {\n')
            f.write('  // Auto-generated typography variables\n')
            f.write('  ' + '\n  '.join(filter(None, scss_vars)))
            f.write('\n}\n')
    except FileNotFoundError:
        print("Warning: Font tokens file not found")

    # Process scale tokens
    try:
        scale_path = os.path.join(base_dir, 'tokens', 'scale', 'option-token.json')
        with open(scale_path, 'r') as f:
            scale_data = json.load(f)
            
        scss_vars = []
        for scale_type, tokens in scale_data.items():
            for key, value in tokens.items():
                scss_vars.extend(json_to_scss_var(key, value, scale_type).split('\n'))
                
        # Write scale variables
        scss_file = os.path.join(scss_dir, '_scale.scss')
        with open(scss_file, 'w') as f:
            f.write(':root {\n')
            f.write('  // Auto-generated scale variables\n')
            f.write('  ' + '\n  '.join(filter(None, scss_vars)))
            f.write('\n}\n')
    except FileNotFoundError:
        print("Warning: Scale tokens file not found")

def split_tokens():
    # Get the script directory as the base directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Read the original tokens.json file
    tokens_path = os.path.join(script_dir, 'tokens.json')
    with open(tokens_path, 'r', encoding='utf-8') as f:
        tokens = json.load(f)

    # Create main directories within the script directory
    for dir_name in ['tokens/brands', 'tokens/color', 'tokens/font', 'tokens/scale', 'src/styles/tokens']:
        create_directory(os.path.join(script_dir, dir_name))

    # Extract and save Light theme colors
    if 'color/Light' in tokens:
        light_colors = tokens['color/Light']
        save_json(light_colors, os.path.join(script_dir, 'tokens', 'color', 'Light.json'))

    # Extract and save Dark theme colors
    if 'color/Dark' in tokens:
        dark_colors = tokens['color/Dark']
        save_json(dark_colors, os.path.join(script_dir, 'tokens', 'color', 'Dark.json'))

    # Extract and save EVYDCore brand tokens
    if 'brands/EVYDCore' in tokens:
        evyd_core = tokens['brands/EVYDCore']
        save_json(evyd_core, os.path.join(script_dir, 'tokens', 'brands', 'EVYDCore.json'))

    # Extract and save BruHealth brand tokens
    if 'brands/BruHealth' in tokens:
        bru_health = tokens['brands/BruHealth']
        save_json(bru_health, os.path.join(script_dir, 'tokens', 'brands', 'BruHealth.json'))

    # Extract and save font tokens
    if 'font/option-token' in tokens:
        font_tokens = tokens['font/option-token']
        save_json(font_tokens, os.path.join(script_dir, 'tokens', 'font', 'option-token.json'))

    # Extract and save scale tokens
    if 'scale/option-token' in tokens:
        scale_tokens = tokens['scale/option-token']
        save_json(scale_tokens, os.path.join(script_dir, 'tokens', 'scale', 'option-token.json'))
          
    # Extract and save $metadata
    if '$metadata' in tokens:
        metadata = tokens['$metadata']
        save_json(metadata, os.path.join(script_dir, 'tokens', '$metadata.json'))

    # Extract and save $themes
    if '$themes' in tokens:
        themes = tokens['$themes']
        save_json(themes, os.path.join(script_dir, 'tokens', '$themes.json'))

    # Check for any remaining tokens not handled
    handled_tokens = {
        '$metadata',
        '$themes', 
        'brands/BruHealth',
        'brands/EVYDCore',
        'color/Dark',
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
    generate_scss_files(script_dir)
    
    print("Token files and SCSS variables have been generated successfully!")

if __name__ == "__main__":
    split_tokens()