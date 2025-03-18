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
        
        # Step 1: Load base token definitions - both CSS variables and Sass variables
        base_tokens = {}
        sass_tokens = {}
        
        # Process color token files
        color_light_file = option_tokens_dir / "colors_light.scss"
        color_dark_file = option_tokens_dir / "colors_dark.scss"
        scale_file = option_tokens_dir / "_scale.scss"
        typography_file = option_tokens_dir / "_typography.scss"
        
        # Verify directories exist
        if not tokens_dir.exists():
            logger.error(f"Tokens directory not found at {tokens_dir}")
            sys.exit(1)
        
        # Load all base tokens (CSS variables with -- prefix)
        css_var_count = 0
        sass_var_count = 0
        
        for file_path in [color_light_file, color_dark_file, scale_file, typography_file]:
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract --token-name: value; pairs (CSS variables)
                        css_token_matches = re.findall(r'--([a-zA-Z0-9-]+):\s*([^;]+);', content)
                        for name, value in css_token_matches:
                            base_tokens[name] = value.strip()
                        css_var_count += len(css_token_matches)
                        
                        # Extract $token-name: value; pairs (Sass variables)
                        sass_token_matches = re.findall(r'\$([a-zA-Z0-9-]+):\s*([^;]+);', content)
                        for name, value in sass_token_matches:
                            sass_tokens[name] = value.strip()
                        sass_var_count += len(sass_token_matches)
                        
                    logger.info(f"Processed {file_path.name} - found {len(css_token_matches)} CSS vars, {len(sass_token_matches)} Sass vars")
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")
        
        logger.info(f"Loaded {css_var_count} CSS variables and {sass_var_count} Sass variables from base tokens")
        
        # Step 2: Process semantic token files that use placeholders
        semantic_tokens = {}
        
        # Find all semantic token files
        semantic_files = []
        if semantic_tokens_dir.exists():
            # Get all SCSS files, including those in subdirectories
            semantic_files = list(semantic_tokens_dir.glob("**/*.scss")) + list(semantic_tokens_dir.glob("**/_*.scss"))
        else:
            logger.warning(f"Semantic tokens directory not found at {semantic_tokens_dir}")
        
        # Process each semantic token file
        for file_path in semantic_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract --token-name: {placeholder}; pairs
                    token_matches = re.findall(r'--([a-zA-Z0-9-]+):\s*([^;]+);', content)
                    for name, value in token_matches:
                        semantic_tokens[name] = value.strip()
                logger.info(f"Processed {file_path.name} - found {len(token_matches)} tokens")
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
        
        # Step 3: Resolve placeholders in semantic tokens using multiple passes
        resolved_tokens = {}
        unresolved_tokens = set()
        
        # Initialize with empty values
        for token_name in semantic_tokens:
            resolved_tokens[token_name] = None
        
        # Process in multiple passes to handle dependencies between tokens
        max_passes = 5
        for pass_num in range(1, max_passes + 1):
            logger.info(f"Resolution pass {pass_num}/{max_passes}")
            unresolved_count_before = len([t for t in resolved_tokens.values() if t is None or '{' in t])
            
            for token_name, token_value in semantic_tokens.items():
                # Skip already resolved tokens
                if resolved_tokens[token_name] is not None and '{' not in resolved_tokens[token_name]:
                    continue
                
                # Process tokens with placeholders
                if '{' in token_value and '}' in token_value:
                    # Handle multiple placeholders in one value
                    resolved_value = token_value
                    placeholders = re.findall(r'\{([^}]+)\}', token_value)
                    all_resolved = True
                    
                    for placeholder in placeholders:
                        placeholder_value = resolve_placeholder(
                            placeholder, 
                            base_tokens, 
                            sass_tokens, 
                            resolved_tokens
                        )
                        
                        if placeholder_value:
                            # Replace the placeholder with its value
                            resolved_value = resolved_value.replace(f"{{{placeholder}}}", placeholder_value)
                        else:
                            all_resolved = False
                            unresolved_tokens.add(placeholder)
                    
                    if all_resolved:
                        resolved_tokens[token_name] = resolved_value
                    elif pass_num == max_passes:
                        # On the final pass, use partially resolved values
                        resolved_tokens[token_name] = resolved_value
                else:
                    # No placeholder, use as is
                    resolved_tokens[token_name] = token_value
            
            # Check if we've made progress in this pass
            unresolved_count_after = len([t for t in resolved_tokens.values() if t is None or '{' in t])
            logger.info(f"Pass {pass_num}: Resolved {unresolved_count_before - unresolved_count_after} additional tokens")
            
            # If all tokens are resolved, break early
            if unresolved_count_after == 0:
                logger.info(f"All tokens resolved after {pass_num} passes")
                break
        
        # Step 4: Generate compiled CSS output
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("/* Generated Semantic Tokens - DO NOT EDIT DIRECTLY */\n")
                f.write("/* Generated on: " + time.strftime("%Y-%m-%d %H:%M:%S") + " */\n\n")
                
                f.write(":root {\n")
                
                # Write all base tokens first
                for name, value in base_tokens.items():
                    f.write(f"  --{name}: {value};\n")
                
                f.write("\n  /* Semantic Tokens */\n")
                
                # Write all resolved semantic tokens
                for name, value in resolved_tokens.items():
                    if value is not None:
                        # Handle any leftover unresolved placeholders
                        if '{' in value and '}' in value:
                            value = re.sub(r'\{[^}]+\}', "#CCCCCC", value)
                        f.write(f"  --{name}: {value};\n")
                
                f.write("}\n")
        except Exception as e:
            logger.error(f"Error writing output file {output_file}: {str(e)}")
            sys.exit(1)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Tokens processed successfully in {elapsed_time:.2f} seconds")
        logger.info(f"Generated compiled tokens at: {output_file}")
        logger.info(f"Processed {len(base_tokens)} base tokens, {len(sass_tokens)} Sass variables, and {len(resolved_tokens)} semantic tokens")
        
        # Summarize unresolved tokens
        if unresolved_tokens:
            resolved_percentage = ((len(semantic_tokens) - len(unresolved_tokens)) / len(semantic_tokens)) * 100
            logger.warning(f"Found {len(unresolved_tokens)} unique unresolved token types ({resolved_percentage:.1f}% tokens resolved)")
            if "--verbose" in sys.argv:
                logger.warning("Unresolved tokens:")
                for token in sorted(unresolved_tokens):
                    logger.warning(f"  - {token}")
        
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 