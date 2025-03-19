#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("token-processor")

def resolve_placeholder(placeholder, base_tokens, sass_tokens, resolved_tokens, resolution_stack=None):
    """
    Recursively resolve token placeholders
    
    Args:
        placeholder: The placeholder string without braces (e.g. "color.cerulean.500-main")
        base_tokens: Dictionary of base CSS tokens
        sass_tokens: Dictionary of Sass variables
        resolved_tokens: Dictionary of already resolved tokens
        resolution_stack: Stack to prevent circular references
        
    Returns:
        Resolved value or None if unresolvable
    """
    if resolution_stack is None:
        resolution_stack = []
    
    # Prevent circular references
    if placeholder in resolution_stack:
        logger.warning(f"Circular reference detected: {' -> '.join(resolution_stack)} -> {placeholder}")
        return None
    
    resolution_stack.append(placeholder)
    placeholder_parts = placeholder.split('.')
    
    # Handle color tokens
    if placeholder_parts[0] == 'color':
        sass_var_name = '-'.join(placeholder_parts)
        
        if sass_var_name in sass_tokens:
            return sass_tokens[sass_var_name]
        
        # Try without 'color-' prefix
        if len(placeholder_parts) > 1:
            sass_var_name_without_prefix = '-'.join(placeholder_parts[1:])
            if sass_var_name_without_prefix in sass_tokens:
                return sass_tokens[sass_var_name_without_prefix]
        
        return "#CCCCCC"  # Fallback
    
    # Handle base tokens
    elif placeholder_parts[0] == 'base':
        if placeholder_parts[1] == 'radius':
            # Map radius tokens to scale values
            radius_name = placeholder_parts[2]
            
            # Map size-1 through size-9 to appropriate scale percentages
            size_mapping = {
                'size-1': '6percent',
                'size-2': '12percent', 
                'size-3': '37percent',
                'size-4': '50percent',
                'size-5': '75percent',
                'size-6': '100percent',
                'size-7': '125percent',
                'size-8': '150percent',
                'size-9': '175percent',
                'pill': '500percent',
                'none': '0percent'
            }
            
            if radius_name in size_mapping:
                scale_token = f"16px-scale-{size_mapping[radius_name]}"
                return base_tokens.get(scale_token, "4px")
            
            return "4px"  # Default fallback
        
        elif placeholder_parts[1] in ['gap', 'padding', 'margin', 'spacing']:
            # Handle gap, padding, margin, and spacing tokens
            size_name = placeholder_parts[2]
            
            # Map size-1 through size-16 to appropriate scale percentages
            size_mapping = {
                'size-1': '6percent',
                'size-2': '12percent', 
                'size-3': '37percent',
                'size-4': '50percent',
                'size-5': '75percent',
                'size-6': '100percent',
                'size-7': '125percent',
                'size-8': '150percent',
                'size-9': '175percent',
                'size-10': '200percent',
                'size-11': '225percent',
                'size-12': '250percent',
                'size-15': '350percent',
                'size-16': '400percent',
                'none': '0percent'
            }
            
            if size_name in size_mapping:
                scale_token = f"16px-scale-{size_mapping[size_name]}"
                return base_tokens.get(scale_token, "8px")
            
            return "8px"  # Default fallback
        
        # Handle other base token types
        elif len(placeholder_parts) > 2:
            base_token_name = '-'.join(placeholder_parts[1:])
            if base_token_name in base_tokens:
                return base_tokens[base_token_name]
    
    # Handle component tokens (may reference other tokens)
    elif placeholder_parts[0] == 'comp':
        comp_token_name = '-'.join(placeholder_parts)
        if comp_token_name in resolved_tokens:
            return resolved_tokens[comp_token_name]
    
    return None  # Couldn't resolve

def main():
    try:
        # Get the project root directory
        root_dir = Path(__file__).parent.parent
        tokens_dir = root_dir / "src" / "styles" / "tokens"
        option_tokens_dir = tokens_dir / "option-tokens"
        semantic_tokens_dir = tokens_dir / "semantic-tokens"
        output_file = root_dir / "src" / "styles" / "compiled-tokens.css"
        
        logger.info("Processing design system tokens...")
        start_time = time.time()
        
        # Define brands to process
        brands = ['evydcore', 'bruhealth']
        
        # Step 1: Load base token definitions - both CSS variables and Sass variables
        # Initialize dictionaries for each theme and brand
        base_tokens = {'light': {}, 'dark': {}}
        sass_tokens = {'light': {}, 'dark': {}}
        
        # Process color token files separately for each theme
        color_light_file = option_tokens_dir / "colors_light.scss"
        color_dark_file = option_tokens_dir / "colors_dark.scss"
        scale_file = option_tokens_dir / "_scale.scss"
        typography_file = option_tokens_dir / "_typography.scss"
        
        # Verify directories exist
        if not tokens_dir.exists():
            logger.error(f"Tokens directory not found at {tokens_dir}")
            sys.exit(1)
        
        # Load theme-independent tokens first
        for file_path in [scale_file, typography_file]:
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract --token-name: value; pairs (CSS variables)
                        css_token_matches = re.findall(r'--([a-zA-Z0-9-]+):\s*([^;]+);', content)
                        for name, value in css_token_matches:
                            base_tokens['light'][name] = value.strip()
                            base_tokens['dark'][name] = value.strip()
                        
                        # Extract $token-name: value; pairs (Sass variables)
                        sass_token_matches = re.findall(r'\$([a-zA-Z0-9-]+):\s*([^;]+);', content)
                        for name, value in sass_token_matches:
                            sass_tokens['light'][name] = value.strip()
                            sass_tokens['dark'][name] = value.strip()
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")
        
        # Load theme-specific tokens
        if color_light_file.exists():
            with open(color_light_file, 'r', encoding='utf-8') as f:
                content = f.read()
                css_token_matches = re.findall(r'--([a-zA-Z0-9-]+):\s*([^;]+);', content)
                for name, value in css_token_matches:
                    base_tokens['light'][name] = value.strip()
                sass_token_matches = re.findall(r'\$([a-zA-Z0-9-]+):\s*([^;]+);', content)
                for name, value in sass_token_matches:
                    sass_tokens['light'][name] = value.strip()
        
        if color_dark_file.exists():
            with open(color_dark_file, 'r', encoding='utf-8') as f:
                content = f.read()
                css_token_matches = re.findall(r'--([a-zA-Z0-9-]+):\s*([^;]+);', content)
                for name, value in css_token_matches:
                    base_tokens['dark'][name] = value.strip()
                sass_token_matches = re.findall(r'\$([a-zA-Z0-9-]+):\s*([^;]+);', content)
                for name, value in sass_token_matches:
                    sass_tokens['dark'][name] = value.strip()
        
        # Step 2: Process semantic token files for each brand
        semantic_tokens = {
            'evydcore': {'light': {}, 'dark': {}},
            'bruhealth': {'light': {}, 'dark': {}}
        }
        
        # Common semantic tokens that are brand-independent
        common_semantic_files = []
        if semantic_tokens_dir.exists():
            common_semantic_files = list(semantic_tokens_dir.glob("_common*.scss"))
        
        # Process each common semantic token file
        for file_path in common_semantic_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    token_matches = re.findall(r'--([a-zA-Z0-9-]+):\s*([^;]+);', content)
                    for name, value in token_matches:
                        for brand in brands:
                            semantic_tokens[brand]['light'][name] = value.strip()
                            semantic_tokens[brand]['dark'][name] = value.strip()
            except Exception as e:
                logger.error(f"Error processing common file {file_path}: {str(e)}")
        
        # Process brand-specific semantic token files
        for brand in brands:
            brand_files = []
            if semantic_tokens_dir.exists():
                brand_files = list(semantic_tokens_dir.glob(f"_{brand}*.scss"))
            
            for file_path in brand_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        token_matches = re.findall(r'--([a-zA-Z0-9-]+):\s*([^;]+);', content)
                        for name, value in token_matches:
                            semantic_tokens[brand]['light'][name] = value.strip()
                            semantic_tokens[brand]['dark'][name] = value.strip()
                except Exception as e:
                    logger.error(f"Error processing brand file {file_path}: {str(e)}")
        
        # Step 3: Resolve placeholders for both themes and brands
        resolved_tokens = {
            'evydcore': {'light': {}, 'dark': {}},
            'bruhealth': {'light': {}, 'dark': {}}
        }
        
        for brand in brands:
            for theme in ['light', 'dark']:
                # Initialize with empty values
                for token_name in semantic_tokens[brand][theme]:
                    resolved_tokens[brand][theme][token_name] = None
                
                # Process in multiple passes
                max_passes = 5
                for pass_num in range(1, max_passes + 1):
                    logger.info(f"Resolution pass {pass_num}/{max_passes} for {brand} in {theme} theme")
                    for token_name, token_value in semantic_tokens[brand][theme].items():
                        if '{' in token_value and '}' in token_value:
                            resolved_value = token_value
                            placeholders = re.findall(r'\{([^}]+)\}', token_value)
                            
                            for placeholder in placeholders:
                                placeholder_value = resolve_placeholder(
                                    placeholder,
                                    base_tokens[theme],
                                    sass_tokens[theme],
                                    resolved_tokens[brand][theme]
                                )
                                
                                if placeholder_value:
                                    resolved_value = resolved_value.replace(f"{{{placeholder}}}", placeholder_value)
                            
                            resolved_tokens[brand][theme][token_name] = resolved_value
                        else:
                            resolved_tokens[brand][theme][token_name] = token_value
        
        # Step 4: Generate compiled CSS output with theme and brand support
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("/* Generated Semantic Tokens - DO NOT EDIT DIRECTLY */\n")
            f.write("/* Generated on: " + time.strftime("%Y-%m-%d %H:%M:%S") + " */\n\n")
            
            # Write theme-independent tokens
            f.write(":root {\n")
            # Write scale and typography tokens that are theme-independent
            for name, value in base_tokens['light'].items():
                if name in base_tokens['dark'] and base_tokens['dark'][name] == value:
                    f.write(f"  --{name}: {value};\n")
            f.write("}\n\n")
            
            # Write theme tokens for each brand
            for brand in brands:
                # Light theme tokens
                f.write(f":root[data-brand=\"{brand}\"][data-theme=\"light\"], ")
                # Default case when brand is set but theme is not explicitly set
                if brand == 'evydcore':
                    f.write(f":root[data-brand=\"{brand}\"]:not([data-theme=\"dark\"]) {{\n")
                else:
                    f.write(f":root[data-brand=\"{brand}\"]:not([data-theme]) {{\n")
                    
                for name, value in resolved_tokens[brand]['light'].items():
                    if value is not None:
                        if '{' in value and '}' in value:
                            value = re.sub(r'\{[^}]+\}', "#CCCCCC", value)
                        f.write(f"  --{name}: {value};\n")
                f.write("}\n\n")
                
                # Dark theme tokens
                f.write(f":root[data-brand=\"{brand}\"][data-theme=\"dark\"] {{\n")
                for name, value in resolved_tokens[brand]['dark'].items():
                    if value is not None:
                        if '{' in value and '}' in value:
                            value = re.sub(r'\{[^}]+\}', "#333333", value)
                        f.write(f"  --{name}: {value};\n")
                f.write("}\n\n")
            
            # Write default tokens (using evydcore as the default)
            # Light theme (default)
            f.write(":root[data-theme=\"light\"], :root:not([data-theme=\"dark\"]) {\n")
            for name, value in resolved_tokens['evydcore']['light'].items():
                if value is not None:
                    if '{' in value and '}' in value:
                        value = re.sub(r'\{[^}]+\}', "#CCCCCC", value)
                    f.write(f"  --{name}: {value};\n")
            f.write("}\n\n")
            
            # Dark theme
            f.write(":root[data-theme=\"dark\"] {\n")
            for name, value in resolved_tokens['evydcore']['dark'].items():
                if value is not None:
                    if '{' in value and '}' in value:
                        value = re.sub(r'\{[^}]+\}', "#333333", value)
                    f.write(f"  --{name}: {value};\n")
            f.write("}\n")
        
        elapsed_time = time.time() - start_time
        logger.info(f"Tokens processed successfully in {elapsed_time:.2f} seconds")
        logger.info(f"Generated compiled tokens for brands: {', '.join(brands)}")
        logger.info(f"Output file: {output_file}")
        
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 