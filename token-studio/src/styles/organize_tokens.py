import os
import re
import sys
import shutil

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
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
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
        # Fix spacing issue in variable names - replace spaces with hyphens
        variant = variant.replace(' ', '-')
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
                
                # Extract primitive tokens from semantic token values if they reference color families
                match = re.search(r'\{color\.([^.]+)\.([^}]+)\}', color_value)
                if match:
                    family = match.group(1)
                    variant = match.group(2)
                    # Fix spacing issue - replace spaces with hyphens
                    variant = variant.replace(' ', '-')
                    scss_var = f"$color-{family}-{variant}"
                    # Use a placeholder color value since we don't have the actual value
                    if family not in primitive_by_family:
                        primitive_by_family[family] = []
                    # Only add if not already in the list
                    placeholder_line = f"{scss_var}: #placeholder; /* Extracted from {token_name} */"
                    if not any(line.startswith(scss_var) for line in primitive_by_family[family]):
                        primitive_by_family[family].append(placeholder_line)
                
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

def fix_color_tokens_format(file_path):
    """Fix any malformed color token variable names in the file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Fix specific variable format issues
        # Replace "$color-stone-00 white:" with "$color-stone-00-white:"
        # Replace "$color-stone-1000 black:" with "$color-stone-1000-black:"
        content = re.sub(r'\$color-([a-zA-Z0-9-]+)\s+([a-zA-Z0-9-]+):', r'$color-\1-\2:', content)
        
        # Also fix variable references in the component tokens
        # Replace "#{$color-stone-00 white}" with "#{$color-stone-00-white}"
        content = re.sub(r'#\{\$color-([a-zA-Z0-9-]+)\s+([a-zA-Z0-9-]+)\}', r'#{$color-\1-\2}', content)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            
        print(f"Fixed color token format in {file_path}")
        return True
    except Exception as e:
        print(f"Error fixing color tokens in {file_path}: {str(e)}", file=sys.stderr)
        return False

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
        # Check if line contains a CSS variable definition
        if any(x in line for x in ['--font-family-', '--font-weight-', '--font-line-height-', 
                                  '--font-size-', '--font-letter-spacing-', 
                                  '--font-paragraph-spacing-', '--font-paragraph-indent-']):
            
            # Split by first colon to separate variable name and value
            parts = line.split(':', 1)  # Split by first colon only
            if len(parts) >= 2:
                # Extract variable name and value
                var_name = parts[0].strip()
                value = parts[1].strip()
                if value.endswith(';'):
                    value = value[:-1]
                
                # Replace spaces in variable names with hyphens
                if ' ' in var_name:
                    var_name = var_name.replace(' ', '-')
                
                # Add px suffix to numeric values
                if any(x in line for x in ['--font-size-', '--font-line-height-', 
                                         '--font-paragraph-spacing-', '--font-paragraph-indent-']):
                    # If the value is numeric and not already has 'px' suffix, add it
                    if value.isdigit() and not 'Auto' in value and not value.endswith('px'):
                        value = f"{value}px"
                
                # Recreate the line with fixed variable name
                line = f"{var_name}: {value};"
        
        # Add line to the appropriate group
        if '--font-family-' in line:
            typography_groups['family'].append('  ' + line.strip())
        elif '--font-weight-' in line:
            typography_groups['weight'].append('  ' + line.strip())
        elif '--font-line-height-' in line:
            typography_groups['lineHeight'].append('  ' + line.strip())
        elif '--font-size-' in line:
            typography_groups['size'].append('  ' + line.strip())
        elif '--font-letter-spacing-' in line:
            typography_groups['letterSpacing'].append('  ' + line.strip())
        elif '--font-paragraph-spacing-' in line:
            typography_groups['paragraphSpacing'].append('  ' + line.strip())
        elif '--font-paragraph-indent-' in line:
            typography_groups['paragraphIndent'].append('  ' + line.strip())

    # Ensure proper nesting in :root
    organized = ':root {\n'
    for group, tokens in typography_groups.items():
        if tokens:
            organized += f'  // ==========================================\n'
            organized += f'  // Font {group.capitalize()}\n'
            organized += f'  // ==========================================\n'
            organized += '\n'.join(tokens) + '\n\n'
    organized += '}\n'

    return organized

def organize_scale_tokens(content):
    """Organize scale tokens into groups"""
    scale_groups = {
        '16px': [],
        '8px': []
    }

    lines = content.split('\n')
    
    for line in lines:
        # Replace percentage signs in variable names with the word 'percent'
        if any(x in line for x in ['--16px-scale-', '--8px-scale-']) and '%' in line:
            # Extract the variable name
            parts = line.split(':')
            if len(parts) >= 2:
                var_name = parts[0].strip()
                value = parts[1].strip()
                if value.endswith(';'):
                    value = value[:-1]
                
                # Replace % with 'percent' in the variable name
                var_name = var_name.replace('%', 'percent')
                
                # If the value is numeric or a decimal and doesn't already have 'px', add it
                if value.replace('.', '', 1).isdigit():
                    line = f"{var_name}: {value}px;"
                else:
                    # Ensure line ends with semicolon
                    if not line.strip().endswith(';'):
                        line = f"{var_name}: {value};"
                    else:
                        line = f"{var_name}: {value}"
        # Regular processing for lines without percentage signs
        elif any(x in line for x in ['--16px-scale-', '--8px-scale-']):
            parts = line.split(':')
            if len(parts) >= 2:
                token_name = parts[0].strip()
                value = parts[1].strip()
                if value.endswith(';'):
                    value = value[:-1]
                
                # If the value is numeric or a decimal and doesn't already have 'px', add it
                if value.replace('.', '', 1).isdigit():
                    line = f"{token_name}: {value}px;"
                else:
                    # Ensure line ends with semicolon
                    if not line.strip().endswith(';'):
                        line = f"{line.strip()};"
                
        if '--16px-scale-' in line:
            # Store with proper indentation and ensure semicolon
            formatted_line = line.strip() if line.strip().endswith(';') else f"{line.strip()};"
            scale_groups['16px'].append('  ' + formatted_line)
        elif '--8px-scale-' in line:
            # Store with proper indentation and ensure semicolon
            formatted_line = line.strip() if line.strip().endswith(';') else f"{line.strip()};"
            scale_groups['8px'].append('  ' + formatted_line)

    # In SCSS syntax we need the entire :root with properly nested CSS properties
    # Each property must end with a semicolon and be properly indented
    organized = ':root {\n'
    for group, tokens in scale_groups.items():
        if tokens:
            organized += f'  // ==========================================\n'
            organized += f'  // {group} Scale\n'
            organized += f'  // ==========================================\n'
            for token in tokens:
                # Ensure each token is properly formatted and indented
                if not token.strip().endswith(';'):
                    token += ';'
                organized += f"{token}\n"
            organized += '\n'
    organized += '}\n'  # Add newline after closing brace

    return organized

def organize_component_tokens(content):
    """Organize component tokens into groups"""
    component_groups = {}
    lines = content.split('\n')
    
    # Extract component tokens
    for line in lines:
        if '--comp-' in line:
            # Replace spaces in variable names with hyphens
            parts = line.split(':', 1)  # Split by first colon only
            if len(parts) >= 2:
                var_name = parts[0].strip()
                value = parts[1].strip()
                
                # Replace spaces in variable names with hyphens
                if ' ' in var_name:
                    var_name = var_name.replace(' ', '-')
                
                # Recreate the line with fixed variable name
                line = f"{var_name}: {value}"
                
            match = re.search(r'--comp-([^-]+)', line)
            if match:
                component = match.group(1)
                if component not in component_groups:
                    component_groups[component] = []
                component_groups[component].append('  ' + line.strip())

    # Process semantic color tokens
    color_tokens = []
    for line in lines:
        if any(x in line for x in ['--color-', '--effect-', '--overlay-']):
            # Replace spaces in variable names with hyphens
            parts = line.split(':', 1)  # Split by first colon only
            if len(parts) >= 2:
                var_name = parts[0].strip()
                value = parts[1].strip()
                
                # Replace spaces in variable names with hyphens
                if ' ' in var_name:
                    var_name = var_name.replace(' ', '-')
                
                # Fix color value references if needed
                if '{color.' in value:
                    # Find all color references and fix spaces in them
                    matches = re.findall(r'\{color\.([^.]+)\.([^}]+)\}', value)
                    for match in matches:
                        family = match[0]
                        variant = match[1]
                        
                        # Replace spaces with hyphens in variant
                        if ' ' in variant:
                            new_variant = variant.replace(' ', '-')
                            old_ref = f"{{color.{family}.{variant}}}"
                            new_ref = f"{{color.{family}.{new_variant}}}"
                            value = value.replace(old_ref, new_ref)
                
                # Recreate the line with fixed variable name
                line = f"{var_name}: {value}"
            
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
                    parts = line.split(':', 1)  # Split by first colon only
                    if len(parts) >= 2:
                        token_name = parts[0].strip()
                        color_value = parts[1].strip()
                        if color_value.endswith(';'):
                            color_value = color_value[:-1]
                        
                        # Fix variable references by replacing spaces with hyphens
                        if "#{$color-" in color_value:
                            color_value = re.sub(r'#\{\$color-([a-zA-Z0-9-]+)\s+([a-zA-Z0-9-]+)\}', r'#{$color-\1-\2}', color_value)
                        
                        formatted_line = token_name + ": " + color_value + ";"
                        color_tokens.append('  ' + formatted_line)
            elif token_name.startswith(('--overlay-', '--effect-', '--logo-')):
                color_tokens.append('  ' + line.strip())

    # Ensure proper nesting in :root
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
    
    organized += '}\n'
    return organized

def extract_primitive_tokens(content):
    """Extract primitive token definitions from content and convert them to SCSS variables"""
    # Extract primitive token section
    primitive_section = "// Primitive Color Tokens\n\n"
    
    # Flag to check if we have a new or old format file
    is_css_variable_format = '--color-' in content
    is_scss_variable_format = '$color-' in content
    
    # If the file has color tokens in CSS variable format
    if is_css_variable_format:
        # Extract all CSS color variables from the content
        css_vars = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('--color-') and ':' in line:
                css_vars.append(line)
        
        # Convert CSS variables to SCSS variables
        scss_vars = []
        for var in css_vars:
            parts = var.split(':')
            if len(parts) >= 2:
                name = parts[0].strip()
                value = ':'.join(parts[1:]).strip()
                if value.endswith(';'):
                    value = value[:-1]
                
                # Skip semantic tokens (those with text, fill, etc.)
                semantic_types = ['text', 'fill', 'border', 'icon', 'surface', 'data', 'illustration']
                is_semantic = False
                for semantic_type in semantic_types:
                    if f"-{semantic_type}-" in name:
                        is_semantic = True
                        break
                
                if not is_semantic and name.startswith('--color-'):
                    # Convert --color-family-variant to $color-family-variant
                    scss_name = name.replace('--color-', '$color-')
                    scss_vars.append(f"{scss_name}: {value};")
        
        # Group SCSS variables by color family
        by_family = {}
        for var in scss_vars:
            name_part = var.split(':')[0].strip()
            matches = re.match(r'\$color-([^-]+)', name_part)
            if matches:
                family = matches.group(1)
                if family not in by_family:
                    by_family[family] = []
                by_family[family].append(var)
        
        # Add variables by family
        for family, vars in sorted(by_family.items()):
            primitive_section += f"// {family.capitalize()} Colors\n"
            primitive_section += '\n'.join(sorted(vars)) + '\n\n'
    
    # If the file already has primitive tokens in SCSS format
    elif is_scss_variable_format:
        # Find all primitive color variables (starting with $color-)
        primitive_vars = []
        for line in content.split('\n'):
            # Fix issue with space in variable names (like "$color-stone-00 white")
            line = re.sub(r'\$color-([a-zA-Z0-9-]+)\s+([a-zA-Z0-9-]+):', r'$color-\1-\2:', line)
            
            if line.strip().startswith('$color-') and ': ' in line:
                primitive_vars.append(line.strip())
        
        # Group by family
        by_family = {}
        for var in primitive_vars:
            matches = re.match(r'\$color-([^-]+)', var)
            if matches:
                family = matches.group(1)
                if family not in by_family:
                    by_family[family] = []
                by_family[family].append(var)
        
        # Add variables by family
        for family, vars in sorted(by_family.items()):
            primitive_section += f"// {family.capitalize()} Colors\n"
            primitive_section += '\n'.join(sorted(vars)) + '\n\n'
    
    # If we have neither format or extraction didn't find anything, create fallback tokens
    if (not is_css_variable_format and not is_scss_variable_format) or primitive_section == "// Primitive Color Tokens\n\n":
        print("Warning: No color tokens found in expected format. Creating fallbacks.")
        
        # Try an alternative extraction method
        theme_match = re.search(r'\[data-theme[^\{]+\{([\s\S]+?)\}', content)
        if theme_match:
            theme_content = theme_match.group(1)
            
            # Extract all color variables from theme content
            theme_vars = []
            primitive_tokens = {}
            
            for line in theme_content.split('\n'):
                line = line.strip()
                if line.startswith('--color-') and ':' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        value = ':'.join(parts[1:]).strip()
                        if value.endswith(';'):
                            value = value[:-1]
                        
                        # Skip semantic tokens
                        semantic_types = ['text', 'fill', 'border', 'icon', 'surface', 'data', 'illustration']
                        is_semantic = False
                        for semantic_type in semantic_types:
                            if f"-{semantic_type}-" in name:
                                is_semantic = True
                                break
                        
                        if not is_semantic:
                            # Convert --color-family-variant to $color-family-variant
                            match = re.match(r'--color-([^-]+)-(.+)', name)
                            if match:
                                family = match.group(1)
                                variant = match.group(2)
                                scss_var = f"$color-{family}-{variant}"
                                
                                if family not in primitive_tokens:
                                    primitive_tokens[family] = []
                                
                                primitive_tokens[family].append(f"{scss_var}: {value};")
            
            # Add the extracted primitive tokens to the output
            for family, tokens in sorted(primitive_tokens.items()):
                primitive_section += f"// {family.capitalize()} Colors\n"
                primitive_section += '\n'.join(sorted(tokens)) + '\n\n'
    
    # If we still don't have any tokens, add placeholder tokens
    if primitive_section == "// Primitive Color Tokens\n\n":
        primitive_section += "/* NOTE: No color tokens found in the source file. Here are some example token families. */\n\n"
        
        # Add example color families
        example_families = {
            'stone': ['25', '50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
            'cerulean': ['50', '100', '200', '300', '400', '500-main', '600', '700', '800', '900'],
            'brick': ['50', '100', '200', '300', '400', '500-main', '600', '700', '800', '900']
        }
        
        for family, variants in example_families.items():
            primitive_section += f"// {family.capitalize()} Colors\n"
            for variant in variants:
                primitive_section += f"$color-{family}-{variant}: #placeholder;\n"
            primitive_section += "\n"
    
    return primitive_section

def extract_semantic_tokens(content):
    """Extract only semantic token definitions from the content"""
    # Find the data-theme section
    theme_match = re.search(r'(\[data-theme[^\{]+\{)([\s\S]+?)(\})', content)
    if theme_match:
        theme_selector = theme_match.group(1) 
        theme_content = theme_match.group(2)
        theme_end = theme_match.group(3)
        
        # Only extract semantic and special tokens
        semantic_lines = []
        for line in theme_content.split('\n'):
            line = line.strip()
            # Add semantic color tokens (--color- with text, fill, border, etc.)
            if line.startswith('--color-'):
                # Check if it's a semantic token
                semantic_types = ['text', 'fill', 'border', 'icon', 'surface', 'data', 'illustration']
                for semantic_type in semantic_types:
                    if f"-{semantic_type}-" in line:
                        # Fix any variable references by replacing spaces with hyphens
                        if "#{$color-" in line:
                            line = re.sub(r'#\{\$color-([a-zA-Z0-9-]+)\s+([a-zA-Z0-9-]+)\}', r'#{$color-\1-\2}', line)
                        semantic_lines.append(line)
                        break
            # Add special tokens
            elif line.startswith(('--overlay-', '--effect-', '--logo-')):
                semantic_lines.append(line)
        
        if semantic_lines:
            return f"{theme_selector}\n  " + "\n  ".join(semantic_lines) + f"\n{theme_end}"
    
    return "// No semantic tokens found"

def organize_tokens():
    """Main function to organize all token files"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        token_dir = os.path.join(script_dir, 'tokens')
        
        # Define target directories for mirrored tokens
        project_root = os.path.abspath(os.path.join(script_dir, '../../../'))
        option_tokens_dir = os.path.join(project_root, 'src/styles/tokens/option-tokens')
        semantic_tokens_dir = os.path.join(project_root, 'src/styles/tokens/semantic-tokens')
        
        # Create target directories if they don't exist
        os.makedirs(option_tokens_dir, exist_ok=True)
        os.makedirs(semantic_tokens_dir, exist_ok=True)
        
        print(f"Working directory: {token_dir}")
        print(f"Files in directory: {os.listdir(token_dir)}")
        print(f"Mirroring to option tokens directory: {option_tokens_dir}")
        print(f"Mirroring to semantic tokens directory: {semantic_tokens_dir}")
        
        # First, fix any syntax issues in the token files
        for filename in os.listdir(token_dir):
            if filename.endswith('.scss'):
                file_path = os.path.join(token_dir, filename)
                fix_color_tokens_format(file_path)
        
        # List of files to process with changed names for component files
        files = {
            '_colors_light.scss': organize_color_tokens,
            '_colors_dark.scss': organize_color_tokens,
            '_typography.scss': organize_typography_tokens,
            '_scale.scss': organize_scale_tokens,
            '_bruhealth.scss': organize_component_tokens,  # Original name kept for reading
            '_evydcore.scss': organize_component_tokens    # Original name kept for reading
        }
        
        # Define which files go to which target directory
        option_token_files = ['_typography.scss', '_scale.scss']
        
        # Updated semantic token files with new names
        semantic_token_files = {
            '_bruhealth.scss': '_bruhealth_comp.scss',  # Map original name to new name
            '_evydcore.scss': '_evydcore_comp.scss'     # Map original name to new name
        }
        
        # Map for color tokens - only one version (without underscore)
        color_token_files = {
            '_colors_light.scss': 'colors_light.scss',  # Map original name to destination name (no underscore)
            '_colors_dark.scss': 'colors_dark.scss'     # Map original name to destination name (no underscore)
        }
        
        # First, remove any existing color files with underscores in the option tokens directory
        for filename in os.listdir(option_tokens_dir):
            if filename.startswith('_colors_') and filename.endswith('.scss'):
                file_to_remove = os.path.join(option_tokens_dir, filename)
                try:
                    os.remove(file_to_remove)
                    print(f"Removed existing underscore-prefixed file: {file_to_remove}")
                except Exception as e:
                    print(f"Warning: Failed to remove {file_to_remove}: {str(e)}")
        
        for filename, processor in files.items():
            file_path = os.path.join(token_dir, filename)
            if os.path.exists(file_path):
                print(f"\nProcessing {filename}...")
                content = read_scss_file(file_path)
                organized = processor(content)
                
                # Write to original location
                write_scss_file(file_path, organized)
                
                # Mirror to appropriate target directory
                if filename in option_token_files:
                    mirror_path = os.path.join(option_tokens_dir, filename)
                    write_scss_file(mirror_path, organized)
                    print(f"Mirrored to option tokens: {mirror_path}")
                
                # Mirror component files with new names to semantic tokens directory
                if filename in semantic_token_files:
                    new_filename = semantic_token_files[filename]
                    mirror_path = os.path.join(semantic_tokens_dir, new_filename)
                    # Apply variable name fixes one more time before writing
                    content_to_write = organized
                    content_to_write = re.sub(r'#\{\$color-([a-zA-Z0-9-]+)\s+([a-zA-Z0-9-]+)\}', r'#{$color-\1-\2}', content_to_write)
                    write_scss_file(mirror_path, content_to_write)
                    print(f"Mirrored to semantic tokens with new name: {mirror_path}")
                
                # Mirror colors files to option tokens directory - only one version (without underscore)
                if filename in color_token_files:
                    # Extract primitive tokens content
                    primitive_content = extract_primitive_tokens(organized)
                    
                    # Generate only the version without leading underscore
                    dest_filename = color_token_files[filename]
                    dest_path = os.path.join(option_tokens_dir, dest_filename)
                    write_scss_file(dest_path, primitive_content)
                    print(f"Mirrored color tokens to: {dest_path}")
                
                print(f"Finished processing {filename}")
            else:
                print(f"Warning: File not found - {file_path}", file=sys.stderr)
        
        # Additionally, directly copy any color token files from token-studio to option-tokens
        print("\nChecking for additional color token files to mirror...")
        for filename in os.listdir(token_dir):
            if filename.endswith('.scss') and 'color' in filename.lower() and filename not in files:
                src_path = os.path.join(token_dir, filename)
                # Remove leading underscore for the destination name
                dest_name = filename[1:] if filename.startswith('_') else filename
                dest_path = os.path.join(option_tokens_dir, dest_name)
                
                print(f"Found additional color file: {filename}")
                content = read_scss_file(src_path)
                primitive_content = extract_primitive_tokens(content)
                write_scss_file(dest_path, primitive_content)
                print(f"Mirrored additional color file to: {dest_path}")

        # Fix any remaining issues in the files after processing
        print("\nFixing any remaining issues in the generated files...")
        for root, dirs, files in os.walk(option_tokens_dir):
            for filename in files:
                if filename.endswith('.scss'):
                    file_path = os.path.join(root, filename)
                    fix_color_tokens_format(file_path)
        
        for root, dirs, files in os.walk(semantic_tokens_dir):
            for filename in files:
                if filename.endswith('.scss'):
                    file_path = os.path.join(root, filename)
                    fix_color_tokens_format(file_path)
                    
    except Exception as e:
        print(f"Error organizing tokens: {str(e)}", file=sys.stderr)
        raise

if __name__ == '__main__':
    organize_tokens() 