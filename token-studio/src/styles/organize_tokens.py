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

def organize_color_tokens(content):
    """Organize color tokens into groups"""
    color_groups = {
        'neutral': [],
        'sky': [],
        'brick': [],
        'marmalade': [],
        'jade': [],
        'merigold': [],
        'violet': [],
        'grape': [],
        'turquoise': [],
        'lime': [],
        'cobalt': [],
        'lemon': [],
        'cerulean': [],
        'stone': [],
        'crimson': [],
        'sea': [],
        'rose': [],
        'lavender': [],
        'effects': []
    }

    lines = content.split('\n')
    
    for line in lines:
        if '--color-' in line:
            for group in color_groups:
                if f'--color-{group}' in line:
                    color_groups[group].append(line.strip())
                    break
        elif any(x in line for x in ['--effect-', '--overlay-', '--logo-']):
            color_groups['effects'].append(line.strip())

    organized = '[data-theme="light"] {\n'
    for group, tokens in color_groups.items():
        if tokens:
            organized += f'  // ==========================================\n'
            organized += f'  // {group.capitalize()} Colors\n'
            organized += f'  // ==========================================\n'
            organized += '\n'.join(tokens) + '\n\n'
    organized += '}'

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

    # Extract color tokens
    color_tokens = [line.strip() for line in lines if any(x in line for x in ['--color-', '--effect-', '--overlay-'])]

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