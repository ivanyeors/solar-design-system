import os
import re
import sys

def read_scss_file(file_path):
    """Read and return contents of SCSS file"""
    try:
        print(f"Reading file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"Successfully read {len(content)} characters from {file_path}")
            return content
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}", file=sys.stderr)
        raise

def write_scss_file(file_path, content):
    """Write organized content to SCSS file"""
    try:
        print(f"Writing to file: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"Successfully wrote {len(content)} characters to {file_path}")
    except Exception as e:
        print(f"Error writing file {file_path}: {str(e)}", file=sys.stderr)
        raise

def transform_primitive_token(token_name, color_value):
    """Convert primitive token to SCSS variable with $color-[family]-[scale/variant] format"""
    # Extract color family and variant from token name
    # Example: --color-cerulean-500-main -> $color-cerulean-500-main
    match = re.match(r'--color-([^-]+)-(.+)', token_name)
    if match:
        family = match.group(1)
        variant = match.group(2)
        scss_var = f"$color-{family}-{variant}"
        return family, scss_var, f"{scss_var}: {color_value};"
    return None, None, None

def transform_semantic_token(token_name, color_value):
    """Convert semantic token to reference primitive token with #{$color-[family]-[scale/variant]}"""
    # Check if the value references a color family in {color.family.variant} format
    match = re.search(r'\{color\.([^.]+)\.([^}]+)\}', color_value)
    if match:
        family = match.group(1)
        variant = match.group(2)
        return f"{token_name}: #{{$color-{family}-{variant}}};"
    
    # If no match in the expected format, keep as is
    return f"{token_name}: {color_value};"

def organize_color_tokens(content):
    """Organize color tokens into primitive and semantic groups"""
    # Determine if this is a light or dark theme file by checking filename
    is_light = '_light' in content
    theme_selector = '[data-theme="light"]' if is_light else '[data-theme="dark"]'
    
    # Dictionary to group primitive tokens by color family
    primitive_by_family = {}
    semantic_tokens = []
    special_tokens = []  # For overlay, effect, logo tokens
    
    # Extract content within theme selector brackets
    theme_match = re.search(r'\[data-theme[^\{]+\{([\s\S]+?)\}', content)
    if theme_match:
        selector_content = theme_match.group(1)
    else:
        print("Warning: No theme selector found, using entire content")
        selector_content = content
    
    # Process all token lines
    lines = selector_content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('//'):
            continue
            
        parts = line.split(':')
        if len(parts) < 2:
            continue
            
        token_name = parts[0].strip()
        color_value = ':'.join(parts[1:]).strip()
        
        # Fix for values with colons in them (like rgba colors)
        if color_value.endswith(';'):
            color_value = color_value[:-1]
        
        # Process color-related tokens
        if token_name.startswith('--color-'):
            # Check if it's a primitive or semantic token
            is_semantic = False
            semantic_types = ['text', 'fill', 'border', 'icon', 'surface', 'data', 'illustration']
            for semantic_type in semantic_types:
                if f"-{semantic_type}-" in token_name:
                    is_semantic = True
                    break
            
            if not is_semantic:
                # It's a primitive color token (like --color-cerulean-500-main)
                family, scss_var, formatted_line = transform_primitive_token(token_name, color_value)
                if formatted_line:
                    if family not in primitive_by_family:
                        primitive_by_family[family] = []
                    primitive_by_family[family].append(formatted_line)
                else:
                    # Fallback if transformation fails
                    unknown_var = f"$color-unknown-{token_name[8:]}:"
                    primitive_by_family.setdefault('unknown', []).append(f"{unknown_var} {color_value};")
            else:
                # It's a semantic token (like --color-text-brand-rest)
                formatted_line = transform_semantic_token(token_name, color_value)
                semantic_tokens.append(formatted_line)
        elif token_name.startswith(('--overlay-', '--effect-', '--logo-')):
            # Handle special cases
            special_tokens.append(f"{token_name}: {color_value};")
    
    # Make sure we have primitive tokens
    if not primitive_by_family:
        print("Warning: No primitive color tokens found in the file!")
    
    # Define the order for common color families
    color_family_order = [
        'neutral', 'stone', 'cerulean', 'sky', 'brick', 'jade', 
        'merigold', 'marmalade', 'violet', 'grape', 'crimson',
        'rose', 'sea', 'turquoise', 'lime', 'lemon', 'cobalt', 'lavender'
    ]
    
    # Sort color families
    sorted_families = []
    
    # Add families in predefined order first
    for family in color_family_order:
        if family in primitive_by_family:
            sorted_families.append(family)
    
    # Add any remaining families alphabetically
    for family in sorted(primitive_by_family.keys()):
        if family not in sorted_families and family != 'unknown':
            sorted_families.append(family)
    
    # Add 'unknown' at the end if it exists
    if 'unknown' in primitive_by_family:
        sorted_families.append('unknown')
    
    # Build the organized output
    organized = '// Primitive Color Tokens\n\n'
    
    # Add primitive tokens grouped by color family
    for family in sorted_families:
        tokens = primitive_by_family[family]
        if tokens:
            organized += f'// {family.capitalize()} Colors\n'
            # Sort tokens within each family
            tokens.sort()
            organized += '\n'.join(tokens) + '\n\n'
    
    # Add semantic tokens and special tokens inside the theme selector
    organized += f'\n{theme_selector} {{\n'
    
    # Group semantic tokens by type for better organization
    semantic_by_type = {}
    for token in semantic_tokens:
        token_name = token.split(':')[0].strip()
        token_parts = token_name.split('-')
        if len(token_parts) > 2:
            token_type = token_parts[1]
            if token_type not in semantic_by_type:
                semantic_by_type[token_type] = []
            semantic_by_type[token_type].append(token)
    
    # Add semantic tokens by type
    for token_type in ['text', 'fill', 'border', 'icon', 'surface', 'data', 'illustration']:
        if token_type in semantic_by_type and semantic_by_type[token_type]:
            organized += f"  // ==========================================\n"
            organized += f"  // {token_type.capitalize()} Tokens\n"
            organized += f"  // ==========================================\n"
            for token in sorted(semantic_by_type[token_type]):
                organized += f"  {token}\n"
            organized += "\n"
    
    # Add any remaining semantic token types
    for token_type, tokens in semantic_by_type.items():
        if token_type not in ['text', 'fill', 'border', 'icon', 'surface', 'data', 'illustration'] and tokens:
            organized += f"  // {token_type.capitalize()} tokens\n"
            for token in sorted(tokens):
                organized += f"  {token}\n"
            organized += "\n"
    
    # Add special tokens
    if special_tokens:
        organized += f"  // ==========================================\n"
        organized += f"  // Special Tokens (overlay, effect, logo)\n"
        organized += f"  // ==========================================\n"
        for token in sorted(special_tokens):
            organized += f"  {token}\n"
    
    organized += '}\n'

    return organized

def organize_typography_tokens(content):
    """Organize typography tokens into groups"""
    typography_groups = {
        'family': [],
        'weight': [],
        'lineHeight': [],
        'size': [],
        'letterSpacing': [],
        'paragraphSpacing': [],
        'paragraphIndent': []
    }

    lines = content.split('\n')
    
    for line in lines:
        if '--font-family-' in line:
            typography_groups['family'].append(line.strip())
        elif '--font-weight-' in line:
            typography_groups['weight'].append(line.strip())
        elif '--font-line-height-' in line:
            typography_groups['lineHeight'].append(line.strip())
        elif '--font-size-' in line:
            typography_groups['size'].append(line.strip())
        elif '--font-letter-spacing-' in line:
            typography_groups['letterSpacing'].append(line.strip())
        elif '--font-paragraph-spacing-' in line:
            typography_groups['paragraphSpacing'].append(line.strip())
        elif '--font-paragraph-indent-' in line:
            typography_groups['paragraphIndent'].append(line.strip())

    organized = ':root {\n'
    for group, tokens in typography_groups.items():
        if tokens:
            organized += f'  // ==========================================\n'
            organized += f'  // Font {group.capitalize()}\n'
            organized += f'  // ==========================================\n'
            organized += '\n'.join(tokens) + '\n\n'
    organized += '}'

    return organized

def organize_scale_tokens(content):
    """Organize scale tokens into groups"""
    scale_groups = {
        '16px': [],
        '8px': []
    }

    lines = content.split('\n')
    
    for line in lines:
        if '--16px-scale-' in line:
            scale_groups['16px'].append(line.strip())
        elif '--8px-scale-' in line:
            scale_groups['8px'].append(line.strip())

    organized = ':root {\n'
    for group, tokens in scale_groups.items():
        if tokens:
            organized += f'  // ==========================================\n'
            organized += f'  // {group} Scale\n'
            organized += f'  // ==========================================\n'
            organized += '\n'.join(tokens) + '\n\n'
    organized += '}'

    return organized

def organize_component_tokens(content):
    """Organize component tokens into groups"""
    component_groups = {}
    lines = content.split('\n')
    
    # Extract component tokens
    for line in lines:
        if '--comp-' in line:
            match = re.search(r'--comp-([^-]+)', line)
            if match:
                component = match.group(1)
                if component not in component_groups:
                    component_groups[component] = []
                component_groups[component].append(line.strip())

    # Process semantic color tokens
    color_tokens = []
    for line in lines:
        if any(x in line for x in ['--color-', '--effect-', '--overlay-']):
            token_name = line.split(':')[0].strip()
            if token_name.startswith('--color-'):
                # Only include semantic tokens (those with types like text, fill, etc.)
                is_semantic = False
                semantic_types = ['text', 'fill', 'border', 'icon', 'surface', 'data', 'illustration']
                for semantic_type in semantic_types:
                    if f"-{semantic_type}-" in token_name:
                        is_semantic = True
                        break
                
                if is_semantic:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        token_name = parts[0].strip()
                        color_value = ':'.join(parts[1:]).strip()
                        if color_value.endswith(';'):
                            color_value = color_value[:-1]
                        formatted_line = transform_semantic_token(token_name, color_value)
                        color_tokens.append(formatted_line)
            elif token_name.startswith(('--overlay-', '--effect-', '--logo-')):
                color_tokens.append(line.strip())

    organized = ':root {\n'
    
    # Add color tokens first
    if color_tokens:
        organized += f'  // ==========================================\n'
        organized += f'  // Color Tokens\n'
        organized += f'  // ==========================================\n'
        organized += '\n'.join(color_tokens) + '\n\n'

    # Add component tokens
    for component, tokens in component_groups.items():
        organized += f'  // ==========================================\n'
        organized += f'  // Component - {component.capitalize()}\n'
        organized += f'  // ==========================================\n'
        organized += '\n'.join(tokens) + '\n\n'
    
    organized += '}'
    return organized

def organize_tokens():
    """Main function to organize all token files"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        token_dir = os.path.join(script_dir, 'tokens')
        print(f"Working directory: {token_dir}")
        print(f"Files in directory: {os.listdir(token_dir)}")
        
        # List of files to process
        files = {
            '_colors_light.scss': organize_color_tokens,
            '_colors_dark.scss': organize_color_tokens,
            '_typography.scss': organize_typography_tokens,
            '_scale.scss': organize_scale_tokens,
            '_bruhealth.scss': organize_component_tokens,
            '_evydcore.scss': organize_component_tokens
        }
        
        for filename, processor in files.items():
            file_path = os.path.join(token_dir, filename)
            if os.path.exists(file_path):
                print(f"\nProcessing {filename}...")
                content = read_scss_file(file_path)
                organized = processor(content)
                write_scss_file(file_path, organized)
                print(f"Finished processing {filename}")
            else:
                print(f"Warning: File not found - {file_path}", file=sys.stderr)

    except Exception as e:
        print(f"Error organizing tokens: {str(e)}", file=sys.stderr)
        raise

if __name__ == '__main__':
    organize_tokens() 