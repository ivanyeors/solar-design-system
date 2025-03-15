#!/usr/bin/env python3
"""
Test script to analyze tokens.json and check for base tokens
"""

import json
import os
import re

def main():
    token_file = "G:/WORKING FILES/solar-design-system/token-studio/tokens.json"
    
    # Check if file exists
    if not os.path.exists(token_file):
        print(f"Error: Token file not found at {token_file}")
        return
    
    # Read the JSON file
    try:
        with open(token_file, 'r', encoding='utf-8') as f:
            tokens_data = json.load(f)
    except Exception as e:
        print(f"Error reading token file: {e}")
        return
    
    # First, print the top-level keys to understand structure
    print("Top-level keys in token file:")
    for key in tokens_data.keys():
        print(f"  - {key}")
    
    # Flatten the token structure for easier analysis
    flattened_tokens = {}
    
    def flatten_tokens(data, prefix=""):
        if not isinstance(data, dict):
            return
            
        for key, value in data.items():
            if isinstance(value, dict) and "value" not in value and "type" not in value:
                # This is a group of tokens, recurse
                new_prefix = f"{prefix}.{key}" if prefix else key
                flatten_tokens(value, new_prefix)
            elif isinstance(value, dict) and "value" in value and "type" in value:
                # This is a token definition
                token_path = f"{prefix}.{key}" if prefix else key
                flattened_tokens[token_path] = {
                    "value": value["value"],
                    "type": value["type"],
                    "description": value.get("description", "")
                }
    
    flatten_tokens(tokens_data)
    
    # Search for base tokens in different ways
    print(f"\nTotal flattened tokens: {len(flattened_tokens)}")
    
    # Method 1: Tokens with path starting with "base"
    base_tokens = [path for path in flattened_tokens.keys() if path.startswith("base")]
    print(f"Tokens with path starting with 'base': {len(base_tokens)}")
    
    # Method 2: Tokens with 'base' in any part of the path
    base_in_path_tokens = [path for path in flattened_tokens.keys() if "base" in path.split(".")]
    print(f"Tokens with 'base' in any part of the path: {len(base_in_path_tokens)}")
    for token in base_in_path_tokens[:5]:
        print(f"  - {token}")
    if len(base_in_path_tokens) > 5:
        print(f"  - ... and {len(base_in_path_tokens) - 5} more")
    
    # Method 3: Search for radius, gap, padding, etc. in paths
    scale_keywords = ["radius", "gap", "padding", "width", "height"]
    scale_tokens = []
    for path in flattened_tokens.keys():
        if any(keyword in path for keyword in scale_keywords):
            scale_tokens.append(path)
    
    print(f"\nTokens containing scale keywords ({', '.join(scale_keywords)}):")
    print(f"Total scale-related tokens: {len(scale_tokens)}")
    
    # Group by scale keyword
    scale_by_keyword = {}
    for keyword in scale_keywords:
        matching_tokens = [path for path in scale_tokens if keyword in path]
        scale_by_keyword[keyword] = matching_tokens
        print(f"\n- {keyword}: {len(matching_tokens)} tokens")
        for token in matching_tokens[:3]:
            print(f"  * {token}: {flattened_tokens[token]['value']} ({flattened_tokens[token]['type']})")
        if len(matching_tokens) > 3:
            print(f"  * ... and {len(matching_tokens) - 3} more")

if __name__ == "__main__":
    main() 