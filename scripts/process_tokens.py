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
            semantic_files = list(semantic_tokens_dir.glob("*.scss")) + list(semantic_tokens_dir.glob("_*.scss"))
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
        
        # Step 3: Resolve placeholders in semantic tokens
        resolved_tokens = {}
        unresolved_tokens = set()
        
        for token_name, token_value in semantic_tokens.items():
            # Check if token has placeholders like {color.cerulean.500-main}
            if '{' in token_value and '}' in token_value:
                # Extract the placeholder name
                placeholder_match = re.match(r'\{([^}]+)\}', token_value)
                if placeholder_match:
                    placeholder = placeholder_match.group(1)
                    placeholder_parts = placeholder.split('.')
                    
                    # Handle color tokens like {color.cerulean.500-main} that should map to Sass variables
                    if placeholder_parts[0] == 'color':
                        # Convert placeholder to sass variable name: color.cerulean.500-main → color-cerulean-500-main
                        sass_var_name = '-'.join(placeholder_parts)
                        
                        if sass_var_name in sass_tokens:
                            # We found a direct match in Sass variables
                            resolved_tokens[token_name] = sass_tokens[sass_var_name]
                            continue
                        
                        # Try without 'color-' prefix (some might be defined as $cerulean-500-main)
                        if len(placeholder_parts) > 1:
                            sass_var_name_without_prefix = '-'.join(placeholder_parts[1:])
                            if sass_var_name_without_prefix in sass_tokens:
                                resolved_tokens[token_name] = sass_tokens[sass_var_name_without_prefix]
                                continue
                        
                        # For colors, we'll use a neutral color as fallback if not found
                        resolved_tokens[token_name] = "#CCCCCC"
                        unresolved_tokens.add(f"{placeholder}")
                    
                    # Handle different types of base tokens
                    elif placeholder_parts[0] == 'base':
                        if placeholder_parts[1] == 'radius':
                            # Map radius tokens to scale values
                            radius_name = placeholder_parts[2]
                            scale_value = None
                            
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
                                scale_value = base_tokens.get(scale_token)
                            
                            if scale_value:
                                resolved_tokens[token_name] = scale_value
                            else:
                                # Default fallback
                                resolved_tokens[token_name] = "4px"
                                unresolved_tokens.add(f"{placeholder}")
                        
                        elif placeholder_parts[1] == 'gap' or placeholder_parts[1] == 'padding':
                            # Handle gap and padding tokens similarly
                            size_name = placeholder_parts[2]
                            scale_value = None
                            
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
                                scale_value = base_tokens.get(scale_token)
                            
                            if scale_value:
                                resolved_tokens[token_name] = scale_value
                            else:
                                resolved_tokens[token_name] = "8px"  # Default fallback
                                unresolved_tokens.add(f"{placeholder}")
                    
                    else:
                        # For other unresolved placeholders
                        resolved_tokens[token_name] = token_value
                        unresolved_tokens.add(f"{placeholder}")
                else:
                    resolved_tokens[token_name] = token_value
            else:
                # No placeholder, use as is
                resolved_tokens[token_name] = token_value
        
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