#!/usr/bin/env python3
"""
Design Token Extractor and Organizer

This script extracts design tokens from a Token Studio tokens.json file
and organizes them into a structured format following industry best practices.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict
import re
import shutil
import hashlib
import time
import datetime

# Token caching functions
def get_file_hash(file_path):
    """
    Calculate the SHA-256 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Hash string or None if file doesn't exist
    """
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return file_hash
    except Exception as e:
        print(f"Error calculating file hash: {e}")
        return None

def get_cache_info(cache_file="token_cache.json"):
    """
    Get cached token information from previous runs.
    
    Args:
        cache_file: Path to the cache file
        
    Returns:
        Dictionary with cache info or empty dict if no cache
    """
    if not os.path.exists(cache_file):
        return {}
    
    try:
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        return cache_data
    except Exception as e:
        print(f"Error reading cache file: {e}")
        return {}

def update_cache_info(token_file, file_hash, tokens_count, cache_file="token_cache.json"):
    """
    Update the cache information with current run data.
    
    Args:
        token_file: Path to the token file
        file_hash: Hash of the token file
        tokens_count: Number of tokens processed
        cache_file: Path to the cache file
    """
    cache_data = get_cache_info(cache_file)
    
    # Update with current run information
    current_time = datetime.datetime.now().isoformat()
    
    cache_data.update({
        "last_run": current_time,
        "token_file": token_file,
        "file_hash": file_hash,
        "tokens_count": tokens_count,
        "output_files": {
            "scss": [] if not CONFIG["outputFormats"]["generateSCSS"] else [
                os.path.join(CONFIG["scssOutputPath"], "option-tokens", "_colors.scss"),
                os.path.join(CONFIG["scssOutputPath"], "option-tokens", "_scale.scss"),
                os.path.join(CONFIG["scssOutputPath"], "option-tokens", "_font.scss"),
                os.path.join(CONFIG["scssOutputPath"], "semantic-tokens", "brands", "_evyd-core.scss"),
                os.path.join(CONFIG["scssOutputPath"], "semantic-tokens", "brands", "_bruhealth.scss"),
                os.path.join(CONFIG["scssOutputPath"], "_tokens.scss")
            ],
            "js": [] if not CONFIG["outputFormats"]["generateJS"] else [
                # List JS output files here
            ]
        }
    })
    
    try:
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        print(f"Error updating cache file: {e}")

def has_tokens_changed(token_file, cache_file="token_cache.json"):
    """
    Check if the tokens file has changed since the last run.
    
    Args:
        token_file: Path to the token file
        cache_file: Path to the cache file
        
    Returns:
        (bool, str) tuple with change status and message
    """
    # Get current file hash
    current_hash = get_file_hash(token_file)
    if not current_hash:
        return True, "Token file not found or could not be read"
    
    # Get cached info
    cache_data = get_cache_info(cache_file)
    
    # If no cache or different file, tokens have changed
    if not cache_data or "file_hash" not in cache_data:
        return True, "No previous run information found"
    
    if cache_data["token_file"] != token_file:
        return True, f"Token file path changed from {cache_data['token_file']} to {token_file}"
    
    # Check if hash has changed
    if cache_data["file_hash"] != current_hash:
        return True, "Token file has been modified since last run"
    
    # Get file modification time
    try:
        mtime = os.path.getmtime(token_file)
        last_modified = datetime.datetime.fromtimestamp(mtime).isoformat()
        
        # If cache has last_run, compare with file modification time
        if "last_run" in cache_data:
            last_run = datetime.datetime.fromisoformat(cache_data["last_run"])
            file_modified = datetime.datetime.fromtimestamp(mtime)
            
            if file_modified > last_run:
                return True, f"Token file modified at {last_modified} after last run at {cache_data['last_run']}"
    except Exception as e:
        print(f"Error checking file modification time: {e}")
    
    return False, f"Token file unchanged since last run at {cache_data.get('last_run', 'unknown time')}"

def generate_token_change_report(current_tokens, cache_file="token_cache.json", format="text"):
    """
    Generate a report of changes between the current tokens and the previous run.
    
    Args:
        current_tokens: The current extracted tokens
        cache_file: Path to the cache file
        format: Report format ('text' or 'markdown')
        
    Returns:
        A report string with changes information
    """
    cache_data = get_cache_info(cache_file)
    
    # If there's no previous run data, we can't generate a change report
    if not cache_data or "tokens_count" not in cache_data:
        no_data_msg = "No previous token extraction data available for comparison."
        return no_data_msg if format == "text" else f"# Token Change Report\n\n{no_data_msg}"
    
    # Basic token count comparison
    previous_count = cache_data.get("tokens_count", 0)
    current_count = len(current_tokens)
    count_diff = current_count - previous_count
    
    # Try to load the previous tokens for detailed comparison
    detailed_comparison = False
    previous_tokens = {}
    token_cache_dir = os.path.dirname(cache_file) or "."
    tokens_backup_path = os.path.join(token_cache_dir, "tokens_backup.json")
    
    if os.path.exists(tokens_backup_path):
        try:
            with open(tokens_backup_path, 'r', encoding='utf-8') as f:
                previous_tokens = json.load(f)
                detailed_comparison = True
        except Exception as e:
            print(f"Could not load previous tokens for detailed comparison: {e}")
    
    # Generate report
    report = []
    
    # Format report based on desired output format
    if format == "markdown":
        report.append("# Token Change Report")
        report.append("")
        report.append(f"**Previous extraction:** {cache_data.get('last_run', 'unknown')}")
        report.append(f"**Previous token count:** {previous_count}")
        report.append(f"**Current token count:** {current_count}")
        report.append("")
        
        if count_diff > 0:
            report.append(f"**Added {count_diff} new tokens**")
        elif count_diff < 0:
            report.append(f"**Removed {abs(count_diff)} tokens**")
        else:
            report.append("**Token count unchanged**")
    else:
        # Plain text format
        report.append("Token Change Report")
        report.append("==================")
        report.append(f"Previous extraction: {cache_data.get('last_run', 'unknown')}")
        report.append(f"Previous token count: {previous_count}")
        report.append(f"Current token count: {current_count}")
        
        if count_diff > 0:
            report.append(f"Added {count_diff} new tokens")
        elif count_diff < 0:
            report.append(f"Removed {abs(count_diff)} tokens")
        else:
            report.append("Token count unchanged")
    
    # Detailed comparison if we have previous token data
    if detailed_comparison and previous_tokens:
        # Find added, removed, and modified tokens
        added_tokens = []
        removed_tokens = []
        modified_tokens = []
        
        # Check for added and modified tokens
        for path, token_data in current_tokens.items():
            if path not in previous_tokens:
                added_tokens.append((path, token_data))
            elif token_data["value"] != previous_tokens[path]["value"]:
                modified_tokens.append((
                    path, 
                    previous_tokens[path]["value"],
                    token_data["value"]
                ))
        
        # Check for removed tokens
        for path in previous_tokens:
            if path not in current_tokens:
                removed_tokens.append((path, previous_tokens[path]))
        
        # Add details to report
        if added_tokens:
            report.append("\nAdded Tokens:")
            report.append("------------")
            for path, token_data in added_tokens[:10]:  # Limit to first 10
                report.append(f"- {path}: {token_data['value']} ({token_data['type']})")
            if len(added_tokens) > 10:
                report.append(f"... and {len(added_tokens) - 10} more")
        
        if removed_tokens:
            report.append("\nRemoved Tokens:")
            report.append("--------------")
            for path, token_data in removed_tokens[:10]:  # Limit to first 10
                report.append(f"- {path}: {token_data['value']} ({token_data['type']})")
            if len(removed_tokens) > 10:
                report.append(f"... and {len(removed_tokens) - 10} more")
        
        if modified_tokens:
            report.append("\nModified Tokens:")
            report.append("---------------")
            for path, old_value, new_value in modified_tokens[:10]:  # Limit to first 10
                report.append(f"- {path}: {old_value} -> {new_value}")
            if len(modified_tokens) > 10:
                report.append(f"... and {len(modified_tokens) - 10} more")
        
        # Generate summary by token type
        token_types = {}
        for path, token_data in current_tokens.items():
            token_type = token_data["type"]
            if token_type not in token_types:
                token_types[token_type] = 0
            token_types[token_type] += 1
        
        report.append("\nToken Type Summary:")
        report.append("-----------------")
        for token_type, count in sorted(token_types.items()):
            report.append(f"- {token_type}: {count} tokens")
    
    # Save current tokens for future comparison
    try:
        token_cache_dir = os.path.dirname(cache_file) or "."
        os.makedirs(token_cache_dir, exist_ok=True)
        with open(os.path.join(token_cache_dir, "tokens_backup.json"), 'w', encoding='utf-8') as f:
            json.dump(current_tokens, f, indent=2)
    except Exception as e:
        print(f"Could not save token backup for future comparison: {e}")
    
    return "\n".join(report)

# Parse command-line arguments
def parse_arguments():
    """Parse command-line arguments for the script."""
    parser = argparse.ArgumentParser(
        description="Extract and organize design tokens from Token Studio JSON file"
    )
    
    parser.add_argument(
        "--token-file", 
        dest="token_file", 
        help="Path to the Token Studio tokens.json file"
    )
    
    parser.add_argument(
        "--js-output", 
        dest="js_output_path", 
        help="Path for JavaScript output"
    )
    
    parser.add_argument(
        "--scss-output", 
        dest="scss_output_path", 
        help="Path for SCSS output"
    )
    
    parser.add_argument(
        "--generate-js",
        dest="generate_js",
        action="store_true",
        help="Generate JavaScript token files"
    )
    
    parser.add_argument(
        "--generate-scss",
        dest="generate_scss",
        action="store_true",
        help="Generate SCSS token files"
    )
    
    parser.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Enable verbose output for debugging"
    )
    
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Preview what would be generated without writing files"
    )
    
    parser.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help="Force generation even if tokens haven't changed"
    )
    
    parser.add_argument(
        "--cache-file",
        dest="cache_file",
        default="token_cache.json",
        help="Path to the cache file"
    )
    
    parser.add_argument(
        "--report-file",
        dest="report_file",
        help="Path to save the token change report"
    )
    
    parser.add_argument(
        "--report-only",
        dest="report_only",
        action="store_true",
        help="Only generate the token change report without extracting tokens"
    )
    
    parser.add_argument(
        "--report-format",
        dest="report_format",
        choices=["text", "markdown"],
        default="text",
        help="Format for the token change report (default: text)"
    )
    
    return parser.parse_args()

# Configuration
CONFIG = {
    # Input/Output Paths
    "tokenStudioFile": "G:/WORKING FILES/solar-design-system/token-studio/tokens.json",
    "jsOutputPath": "G:/WORKING FILES/solar-design-system/src/tokens",
    "scssOutputPath": "G:/WORKING FILES/solar-design-system/src/styles/tokens",
    
    # Output format control
    "outputFormats": {
        "generateJS": False,  # Set to False to skip JS generation
        "generateSCSS": True  # Set to True to generate SCSS
    },
    "expectedPaths": {
        "colorLight": "color/Light",
        "colorDark": "color/Dark",
        "brandEVYDCore": "brands/EVYDCore",
        "brandBruHealth": "brands/BruHealth",
        "fontOptions": "font/option-token",
        "scaleOptions": "scale/option-token",
        "themes": "$themes",
        "metadata": "$metadata"
    },
    "outputDir": os.path.join(os.getcwd(), "src", "tokens"),
    "scssOutputDir": os.path.join(os.getcwd(), "src", "styles", "tokens"),
    "themes": ["light", "dark"],
    "fileStructure": {
        "optionTokens": {
            "colors": "option-tokens/colors.js",
            "scale": "option-tokens/scale.js",
            "font": "option-tokens/font.js"
        },
        "semanticTokens": {
            "brands": {
                "evydCore": "semantic-tokens/brands/evyd-core.js",
                "bruHealth": "semantic-tokens/brands/bruhealth.js"
            },
            "themes": "semantic-tokens/themes.js"
        },
        "index": "index.js"
    },
    "scssFileStructure": {
        "optionTokens": {
            "colors": "_colors.scss",
            "scale": "_scale.scss",
            "font": "_font.scss"
        },
        "semanticTokens": {
            "brands": {
                "evydCore": "_evyd-core.scss",
                "bruHealth": "_bruhealth.scss"
            },
            "themes": "_themes.scss"
        },
        "index": "_tokens.scss"
    },
    # Common component paths within brand tokens
    "componentPaths": [
        "color.text", "color.fill", "color.stroke", "color.icon", "color.border",
        "base.radius", "base.padding", "base.gap",
        "font", "typography"
    ]
}

# Define component types for identifying token groups
COMPONENT_TYPES = [
    "avatar", "badge", "button", "card", "checkbox", "dialog", "drawer",
    "dropdown", "form", "header", "icon", "input", "link", "menu",
    "navbar", "notification", "pill", "progress", "radio", "select",
    "sidebar", "switch", "table", "tabs", "tag", "toast", "tooltip"
]

# Define system groups for non-component tokens
SYSTEM_GROUPS = [
    "layout", "background", "text", "border", "icon", "interactive", "feedback", "other"
]

def ensure_directory_exists(directory):
    """Ensure the output directory exists, create it if it doesn't."""
    os.makedirs(directory, exist_ok=True)
    print(f"Directory ensured: {directory}")

def clean_scss_output_directory():
    """Clean the SCSS output directory to ensure a fresh start."""
    scss_output_dir = CONFIG["scssOutputPath"]
    if os.path.exists(scss_output_dir):
        print(f"Cleaning SCSS output directory: {scss_output_dir}")
        # Instead of removing the entire directory, we'll remove individual files
        for root, dirs, files in os.walk(scss_output_dir):
            for file in files:
                if file.endswith('.scss'):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"  Removed: {file_path}")
    
    # Recreate the directory structure
    ensure_directory_exists(scss_output_dir)
    ensure_directory_exists(os.path.join(scss_output_dir, "option-tokens"))
    ensure_directory_exists(os.path.join(scss_output_dir, "semantic-tokens"))
    ensure_directory_exists(os.path.join(scss_output_dir, "semantic-tokens", "brands"))

def process_tokens(tokens):
    """
    Process and categorize tokens into option tokens and semantic tokens.
    """
    result = {
        "optionTokens": {
            "colors": {},
            "scale": {},
            "font": {}
        },
        "semanticTokens": {
            "brands": {
                "evydcore": {},
                "bruhealth": {}
            },
            "themes": {
                "light": {},
                "dark": {}
            }
        }
    }

    # Scale-related terms for categorization
    scale_terms = ["spacing", "sizing", "radius", "border", "scale", "base", "gap", "padding", "width", "height"]

    # Detailed debug counters for each category
    debug_counters = {
        "colors": 0,
        "scale": 0,
        "scale_by_term": {"radius": 0, "gap": 0, "padding": 0, "width": 0, "height": 0, "base": 0},
        "font": 0,
        "brands": {"evydcore": 0, "bruhealth": 0},
    }

    # Debug print for token count
    print(f"Total tokens for processing: {len(tokens)}")
    print("Processing tokens and categorizing them...\n")

    # Process each token and categorize it
    for token_path, token_data in tokens.items():
        # Debug for base tokens
        if "base" in token_path:
            if debug_counters["scale_by_term"]["base"] < 5:  # Limit the output to first 5
                print(f"Found base token: {token_path}")
            debug_counters["scale_by_term"]["base"] += 1

        # Check for expected paths based on the TOKEN STUDIO structure
        if token_path.startswith("color/Light") or token_path.startswith("color/Dark"):
            result["optionTokens"]["colors"][token_path] = token_data
            debug_counters["colors"] += 1
        
        # Option tokens - Scale
        elif token_path.startswith("scale/option-token"):
            result["optionTokens"]["scale"][token_path] = token_data
            debug_counters["scale"] += 1
        
        # Option tokens - Font
        elif token_path.startswith("font/option-token"):
            result["optionTokens"]["font"][token_path] = token_data
            debug_counters["font"] += 1
        
        # Semantic tokens - EVYDCore
        elif token_path.startswith("brands/EVYDCore"):
            # Special handling for base scale tokens referenced by EVYD Core
            if ".base.radius." in token_path or ".base.gap." in token_path or ".base.padding." in token_path or ".base.width." in token_path or ".base.height." in token_path:
                result["optionTokens"]["scale"][token_path] = token_data
                if ".base.radius." in token_path:
                    debug_counters["scale_by_term"]["radius"] += 1
                elif ".base.gap." in token_path:
                    debug_counters["scale_by_term"]["gap"] += 1
                elif ".base.padding." in token_path:
                    debug_counters["scale_by_term"]["padding"] += 1
                elif ".base.width." in token_path:
                    debug_counters["scale_by_term"]["width"] += 1
                elif ".base.height." in token_path:
                    debug_counters["scale_by_term"]["height"] += 1
                debug_counters["scale"] += 1
            else:
                result["semanticTokens"]["brands"]["evydcore"][token_path] = token_data
                debug_counters["brands"]["evydcore"] += 1
        
        # Semantic tokens - BruHealth
        elif token_path.startswith("brands/BruHealth"):
            # Special handling for base scale tokens referenced by BruHealth
            if ".base.radius." in token_path or ".base.gap." in token_path or ".base.padding." in token_path or ".base.width." in token_path or ".base.height." in token_path:
                result["optionTokens"]["scale"][token_path] = token_data
                if ".base.radius." in token_path:
                    debug_counters["scale_by_term"]["radius"] += 1
                elif ".base.gap." in token_path:
                    debug_counters["scale_by_term"]["gap"] += 1
                elif ".base.padding." in token_path:
                    debug_counters["scale_by_term"]["padding"] += 1
                elif ".base.width." in token_path:
                    debug_counters["scale_by_term"]["width"] += 1
                elif ".base.height." in token_path:
                    debug_counters["scale_by_term"]["height"] += 1
                debug_counters["scale"] += 1
            else:
                result["semanticTokens"]["brands"]["bruhealth"][token_path] = token_data
                debug_counters["brands"]["bruhealth"] += 1
        
        # If none of the above, try to categorize based on the token path
        else:
            parts = token_path.split(".")
            
            # Attempt to categorize by looking at the token path components
            if "color" in parts:
                result["optionTokens"]["colors"][token_path] = token_data
                debug_counters["colors"] += 1
            elif any(scale_term in parts for scale_term in scale_terms):
                result["optionTokens"]["scale"][token_path] = token_data
                debug_counters["scale"] += 1
                
                # Track which scale term was used for categorization
                for term in ["radius", "gap", "padding", "width", "height"]:
                    if term in parts:
                        debug_counters["scale_by_term"][term] += 1
            elif any(font_term in parts for font_term in ["font", "typography", "fontFamily", "fontSize", "fontWeight"]):
                result["optionTokens"]["font"][token_path] = token_data
                debug_counters["font"] += 1

    # Print debug information
    print("\nToken Categorization Summary:")
    print(f"- Option Tokens (Colors): {debug_counters['colors']}")
    print(f"- Option Tokens (Scale): {debug_counters['scale']}")
    print("  Scale tokens by term:")
    for term, count in debug_counters["scale_by_term"].items():
        print(f"  - {term}: {count}")
    print(f"- Option Tokens (Font): {debug_counters['font']}")
    print(f"- Semantic Tokens (EVYDCore): {debug_counters['brands']['evydcore']}")
    print(f"- Semantic Tokens (BruHealth): {debug_counters['brands']['bruhealth']}")

    # Print totals for each main category
    print("\nTotal Option Tokens:", 
          debug_counters["colors"] + debug_counters["scale"] + debug_counters["font"])
    print("Total Semantic Tokens:", 
          debug_counters["brands"]["evydcore"] + debug_counters["brands"]["bruhealth"])
    print("Grand Total:", len(tokens))
    
    return result

def extract_component_name(path):
    """
    Extract component name from a token path.
    E.g. "brands.evydCore.color.text.button-primary" -> "button"
    """
    path_parts = path.split('.')
    
    # Expanded list of component keywords with more UI elements
    component_keywords = [
        # Basic components
        'button', 'input', 'card', 'toggle', 'checkbox', 'radio', 'dropdown',
        'slider', 'tooltip', 'modal', 'tab', 'accordion', 'table', 'avatar',
        'badge', 'banner', 'toast', 'alert', 'progress', 'spinner', 'menu',
        
        # Layout components
        'form', 'header', 'footer', 'sidebar', 'navigation', 'pagination',
        'breadcrumb', 'dialog', 'popover', 'tag', 'chip', 'layout', 'grid',
        'container', 'divider', 'section',
        
        # Specialized components
        'datepicker', 'timepicker', 'calendar', 'carousel', 'drawer', 'stepper',
        'panel', 'list', 'listitem', 'treeview', 'combobox', 'textarea',
        'select', 'switch', 'skeleton', 'link', 'icon', 'separator', 'field',
        'pill', 'notification', 'snackbar'
    ]
    
    # Check each part of the path for component names
    for part in path_parts:
        # Check if any component keyword is in this part
        part_lower = part.lower()
        for keyword in component_keywords:
            if keyword in part_lower:
                return keyword
    
    # For paths that don't match explicit component names
    # Look for component context patterns
    for i, part in enumerate(path_parts):
        part_lower = part.lower()
        
        # Check for state indicators that imply a component
        if i > 0 and any(pattern in part_lower for pattern in [
            '-rest', '-hover', '-active', '-press', '-disabled', 
            '-focus', '-selected', '-error'
        ]):
            # This looks like a component state, get the component name from previous part
            return path_parts[i-1].lower()
            
        # Check for element/purpose indicators that imply a component
        if part_lower in ['title', 'subtitle', 'heading', 'label', 'caption', 'body', 'container']:
            # These are likely UI elements - check previous part for context
            if i > 0 and path_parts[i-1].lower() not in ['color', 'font', 'typography', 'scale']:
                return path_parts[i-1].lower()
    
    # Additional heuristic: check if the description indicates a component
    # (This would be implemented in the categorize_tokens function)
    
    return None

def identify_property_type(token_path, token_name):
    """
    Identify the property type of a token (color, background, etc).
    
    Args:
        token_path: The token path
        token_name: The token name
        
    Returns:
        Property type string
    """
    # Check for common property types in token path or name
    path_and_name = (token_path + "." + token_name).lower()
    
    if any(term in path_and_name for term in ["background", "bg-", "bg_", "-bg", "_bg"]):
        return "background"
    
    if any(term in path_and_name for term in ["color", "text-color", "text-style"]):
        return "text"
    
    if any(term in path_and_name for term in ["border", "outline", "stroke"]):
        return "border"
    
    if any(term in path_and_name for term in ["shadow", "elevation"]):
        return "shadow"
    
    if any(term in path_and_name for term in ["radius", "corner", "round"]):
        return "radius"
    
    if any(term in path_and_name for term in ["spacing", "padding", "margin", "gap"]):
        return "spacing"
    
    if any(term in path_and_name for term in ["size", "width", "height", "dimension"]):
        return "size"
    
    if any(term in path_and_name for term in ["font", "text", "typography"]):
        return "typography"
    
    if any(term in path_and_name for term in ["icon"]):
        return "icon"
    
    # Default to base if no specific property type is found
    return "base"

def identify_state(token_path, token_name):
    """
    Identify if a token represents a particular state.
    
    Args:
        token_path: The token path
        token_name: The token name
        
    Returns:
        State string if identified, None otherwise
    """
    # Common states in UI
    states = ["hover", "active", "focus", "disabled", "pressed", "selected", "error", "loading"]
    
    # Check token path and name for state indicators
    path_and_name = (token_path + "." + token_name).lower()
    
    for state in states:
        if state in path_and_name:
            return state
    
    # Default state is 'default' or None
    return None

def identify_variant(token_path, token_name):
    """
    Identify if a token represents a particular variant.
    
    Args:
        token_path: The token path
        token_name: The token name
        
    Returns:
        Variant string if identified, None otherwise
    """
    # Common variants in UI
    variants = ["primary", "secondary", "tertiary", "success", "warning", "error", "info", "subtle", "outline", "ghost"]
    
    # Check token path and name for variant indicators
    path_and_name = (token_path + "." + token_name).lower()
    
    for variant in variants:
        if variant in path_and_name:
            return variant
    
    # Default variant is 'default' or None
    return None

def format_semantic_token_name(component, token_path, original_name):
    """
    Format a semantic token name following component-property-state-variant pattern.
    
    Args:
        component: The component name
        token_path: The token path
        original_name: The original token name
        
    Returns:
        Formatted semantic token name with a consistent naming pattern
    """
    # Identify key parts
    property_type = identify_property_type(token_path, original_name)
    state = identify_state(token_path, original_name)
    variant = identify_variant(token_path, original_name)
    
    # Clean the component name
    component = component.lower().replace(" ", "-")
    
    # Start building the token name with component
    parts = ["component", component]
    
    # Add property type (e.g., background, text)
    if property_type != "base":
        parts.append(property_type)
    
    # Add variant if present (e.g., primary, secondary)
    if variant:
        parts.append(variant)
    
    # Add state if present (e.g., hover, disabled)
    if state:
        parts.append(state)
    
    # Join parts with hyphens
    token_name = "-".join(parts)
    
    # Clean up any duplicate parts
    token_name = re.sub(r'([a-z-]+)-\1', r'\1', token_name)
    token_name = re.sub(r'-+', '-', token_name)
    
    return token_name

def categorize_tokens(flattened_tokens):
    """Categorize tokens based on their paths and expected locations."""
    token_sets = {
        "optionTokens": {
        "colors": {},
            "scale": {},
            "font": {}
        },
        "semanticTokens": {
            "brands": {
                "evydCore": {},
                "bruHealth": {}
            },
            "themes": {}
        }
    }
    
    # Add component grouping dictionaries
    component_groups = {
        "evydCore": defaultdict(list),
        "bruHealth": defaultdict(list)
    }
    
    # Add system-level token groups for global tokens
    system_groups = {
        "evydCore": {
            "surface": [],       # Background surfaces
            "text": [],          # Text/typography
            "border": [],        # Border/outline
            "interactive": [],   # Interactive elements
            "feedback": [],      # Feedback/status indicators
            "layout": [],        # Layout-related
            "elevation": [],     # Shadow/elevation
            "other": []          # Other system-level tokens
        },
        "bruHealth": {
            "surface": [],
            "text": [],
            "border": [],
            "interactive": [],
            "feedback": [],
            "layout": [],
            "elevation": [],
            "other": []
        }
    }
    
    colors_count = 0
    scale_count = 0
    font_count = 0
    evyd_count = 0
    bruhealth_count = 0
    themes_count = 0
    other_count = 0
    
    # Helper function to find the root path of a token
    def find_root_path(path):
        for expected_path in CONFIG["expectedPaths"].values():
            if path.startswith(expected_path):
                return expected_path
        return None
    
    # Helper function to identify system-level tokens
    def identify_system_group(path, description):
        path_lower = path.lower()
        description_lower = description.lower() if description else ""
        
        # Surface tokens
        if any(term in path_lower for term in ["background", "bg", "surface", "fill"]) or \
           any(term in description_lower for term in ["background", "surface", "container"]):
            return "surface"
            
        # Text tokens
        elif any(term in path_lower for term in ["text", "font", "typography", "label"]) or \
             any(term in description_lower for term in ["text", "font", "typography"]):
            return "text"
            
        # Border tokens
        elif any(term in path_lower for term in ["border", "outline", "stroke"]) or \
             any(term in description_lower for term in ["border", "outline", "stroke"]):
            return "border"
            
        # Interactive tokens
        elif any(term in path_lower for term in ["hover", "active", "focus", "press", "click"]) or \
             any(term in description_lower for term in ["interaction", "clickable", "selectable"]):
            return "interactive"
            
        # Feedback tokens
        elif any(term in path_lower for term in ["error", "warning", "success", "info", "alert", "notification"]) or \
             any(term in description_lower for term in ["error", "warning", "success", "alert", "status"]):
            return "feedback"
            
        # Layout tokens
        elif any(term in path_lower for term in ["spacing", "gap", "margin", "padding", "layout", "grid"]) or \
             any(term in description_lower for term in ["spacing", "layout", "position", "alignment"]):
            return "layout"
            
        # Elevation tokens
        elif any(term in path_lower for term in ["shadow", "elevation", "depth", "layer"]) or \
             any(term in description_lower for term in ["shadow", "elevation", "layer", "z-index"]):
            return "elevation"
            
        # Default to other
        return "other"
    
    print("\nAnalyzing token paths for categorization and component grouping...")
    
    for token_path, token_data in flattened_tokens.items():
        value = token_data["value"]
        token_type = token_data["type"]
        original_path = token_data["originalPath"]
        description = token_data.get("description", "")
        root_path = find_root_path(token_path)
        
        # Option Tokens - Colors
        if token_path.startswith(CONFIG["expectedPaths"]["colorLight"]):
            # For color/Light tokens, we will create a prefix based on the structure
            # e.g., color/Light.color.neutral-depr.25 -> color.light.neutral-depr.25
            parts = token_path.split('.')
            modified_path = '.'.join(['color.light'] + parts[1:])
            token_sets["optionTokens"]["colors"][modified_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            colors_count += 1
        elif token_path.startswith(CONFIG["expectedPaths"]["colorDark"]):
            parts = token_path.split('.')
            modified_path = '.'.join(['color.dark'] + parts[1:])
            token_sets["optionTokens"]["colors"][modified_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            colors_count += 1
        
        # Option Tokens - Scale
        elif token_path.startswith(CONFIG["expectedPaths"]["scaleOptions"]):
            parts = token_path.split('.')
            modified_path = '.'.join(['scale'] + parts[1:])
            token_sets["optionTokens"]["scale"][modified_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            scale_count += 1
        
        # Option Tokens - Font
        elif token_path.startswith(CONFIG["expectedPaths"]["fontOptions"]):
            parts = token_path.split('.')
            modified_path = '.'.join(['font'] + parts[1:])
            token_sets["optionTokens"]["font"][modified_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            font_count += 1
        
        # Semantic Tokens - Brands
        elif token_path.startswith(CONFIG["expectedPaths"]["brandEVYDCore"]):
            parts = token_path.split('.')
            modified_path = '.'.join(['brands.evydCore'] + parts[1:])
            token_sets["semanticTokens"]["brands"]["evydCore"][modified_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            
            # Identify and categorize component tokens for EVYDCore
            component_name = extract_component_name(modified_path)
            if component_name:
                component_groups["evydCore"][component_name].append(modified_path)
            else:
                # If not a component token, add to system groups
                system_group = identify_system_group(modified_path, description)
                system_groups["evydCore"][system_group].append(modified_path)
            
            evyd_count += 1
        
        # Semantic Tokens - BruHealth Brand
        elif token_path.startswith(CONFIG["expectedPaths"]["brandBruHealth"]):
            parts = token_path.split('.')
            modified_path = '.'.join(['brands.bruHealth'] + parts[1:])
            token_sets["semanticTokens"]["brands"]["bruHealth"][modified_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            
            # Identify and categorize component tokens for BruHealth
            component_name = extract_component_name(modified_path)
            if component_name:
                component_groups["bruHealth"][component_name].append(modified_path)
            else:
                # If not a component token, add to system groups
                system_group = identify_system_group(modified_path, description)
                system_groups["bruHealth"][system_group].append(modified_path)
            
            bruhealth_count += 1
        
        # Semantic Tokens - Themes
        elif token_path.startswith(CONFIG["expectedPaths"]["themes"]):
            parts = token_path.split('.')
            modified_path = '.'.join(['themes'] + parts[1:])
            token_sets["semanticTokens"]["themes"][modified_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            themes_count += 1
        
        # If none of the above match but contains certain patterns, try to assign appropriately
        elif token_type == "color":
            # Default to colors if not matched but is a color
            token_sets["optionTokens"]["colors"][token_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            colors_count += 1
        elif any(pattern in token_path.lower() for pattern in ["size", "spacing", "gap", "radius"]):
            # Likely a scale token
            token_sets["optionTokens"]["scale"][token_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            scale_count += 1
        elif any(pattern in token_path.lower() for pattern in ["font", "text", "typography"]):
            # Likely a font token
            token_sets["optionTokens"]["font"][token_path] = {
                "value": value,
                "type": token_type,
                "originalPath": original_path,
                "description": description
            }
            font_count += 1
        else:
            # Unmatched token
            other_count += 1
    
    print("\nToken categorization summary:")
    print(f"- Colors: {colors_count} tokens")
    print(f"- Scale: {scale_count} tokens")
    print(f"- Font: {font_count} tokens")
    print(f"- EVYD Core: {evyd_count} tokens")
    print(f"- BruHealth: {bruhealth_count} tokens")
    print(f"- Themes: {themes_count} tokens")
    print(f"- Uncategorized: {other_count} tokens")
    
    # Print component group summary
    print("\nComponent groups found:")
    for brand, components in component_groups.items():
        if components:
            print(f"- {brand}: {len(components)} components")
            for comp_name, tokens in sorted(components.items()):
                print(f"  - {comp_name}: {len(tokens)} tokens")
                # Print a sample of the tokens for this component (up to 3)
                sample_size = min(3, len(tokens))
                for i in range(sample_size):
                    path_parts = tokens[i].split('.')
                    last_part = path_parts[-1]
                    print(f"    • {last_part}")
    
    # Print system group summary
    print("\nSystem-level token groups found:")
    for brand, groups in system_groups.items():
        print(f"- {brand}:")
        for group_name, tokens in sorted(groups.items()):
            if tokens:
                print(f"  - {group_name}: {len(tokens)} tokens")
                # Print a sample of the tokens for this group (up to 2)
                sample_size = min(2, len(tokens))
                for i in range(sample_size):
                    path_parts = tokens[i].split('.')
                    last_part = path_parts[-1]
                    print(f"    • {last_part}")
    
    return token_sets, component_groups, system_groups

def format_token_value(value, token_type, is_brand_file=False):
    """
    Format a token value for JavaScript.
    
    Args:
        value: The token value to format
        token_type: The type of token
        is_brand_file: Flag to indicate if in a brand file (for references)
    
    Returns:
        Formatted JS value
    """
    # Handle token references
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        # Get the token path from the reference
        token_path = value[1:-1]
        parts = token_path.split(".")
        
        # Check for specific reference types in brand files
        if is_brand_file:
            # Reference to an option token
            if parts[0] == "color":
                # Return format: optionColors.red500
                token_name = parts[-1].lower()
                return f"optionColors.{token_name}"
            elif parts[0] in ["spacing", "sizing", "radius", "border"]:
                # Return format: optionScale.spacingMd
                token_name = parts[-1].lower()
                return f"optionScale.{token_name}"
            elif parts[0] in ["font", "typography", "fontFamily", "fontSize", "fontWeight"]:
                # Return format: optionFont.fontFamilyPrimary
                token_name = parts[-1].lower()
                return f"optionFont.{token_name}"
        
        # For other references, use direct string format
        return f"'{token_path}'"
    
    # Handle basic types
    if token_type == "color":
        if isinstance(value, str):
            return f"'{value}'"
        return str(value)
    
    if isinstance(value, (int, float)):
        return str(value)
    
    if isinstance(value, str):
        return f"'{value}'"
    
    return str(value)

def format_scss_token_value(value, token_type, token_sets=None):
    """
    Format a token value for SCSS.
    
    Args:
        value: The token value to format
        token_type: The type of token
        token_sets: Optional - the full token sets for resolving token references
    
    Returns:
        Formatted SCSS value
    """
    # Handle token references
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        # Get the token path from the reference
        token_path = value[1:-1]
        
        # If token_sets is provided, try to resolve the reference directly
        if token_sets:
            # Extract parts to determine token category
            parts = token_path.split(".")
            referenced_token = None
            
            # Search through option tokens
            for category in ["colors", "scale", "font"]:
                if token_path in token_sets["optionTokens"][category]:
                    referenced_token = token_sets["optionTokens"][category][token_path]
                    break
            
            # If not found in option tokens, search semantic tokens
            if not referenced_token:
                for brand in ["evydcore", "bruhealth"]:
                    if token_path in token_sets["semanticTokens"]["brands"][brand]:
                        referenced_token = token_sets["semanticTokens"]["brands"][brand][token_path]
                        break
                
                if not referenced_token and token_path in token_sets["semanticTokens"]["themes"]:
                    referenced_token = token_sets["semanticTokens"]["themes"][token_path]
            
            # If we found the referenced token, return its value (recursively resolving if needed)
            if referenced_token:
                referenced_value = referenced_token["value"]
                if isinstance(referenced_value, str) and referenced_value.startswith("{") and referenced_value.endswith("}"):
                    # Recursive reference, resolve it
                    return format_scss_token_value(referenced_value, referenced_token["type"], token_sets)
                else:
                    # Direct value
                    return format_scss_token_value(referenced_value, referenced_token["type"])
        
        # If we couldn't resolve the reference, convert to SCSS variable
        token_var = token_path.replace(".", "-").lower()
        return f"${token_var}"
    
    # Handle basic types based on token_type
    if token_type == "color":
        return value  # Colors can be returned as-is in SCSS
    
    if isinstance(value, (int, float)) and token_type in ["dimension", "fontSize", "lineHeight", "letterSpacing", "spacing", "sizing", "radius", "borderWidth"]:
        # Add "px" for dimension values that are numbers
        if value == 0:
            return "0"  # No need for unit when value is 0
        else:
            return f"{value}px"
    
    # For string values or other types
    if isinstance(value, str):
        # Check if it's already quoted
        if value.startswith('"') and value.endswith('"'):
            return value
        elif value.startswith("'") and value.endswith("'"):
            return value
        else:
            # Quote string values
            return f'"{value}"'
    
    # Default case
    return str(value)

def generate_js_module(tokens, name, description, component_groups=None, system_groups=None):
    """
    Generate a JavaScript module from token data.
    
    Args:
        tokens: The tokens to generate a module for
        name: The module name
        description: Description of the module
        component_groups: Optional component groupings
        system_groups: Optional system-level groups
    
    Returns:
        String content of the JavaScript module
    """
    is_brand = name in ["evydcore", "bruhealth"]
    normalized_name = name.replace("-", "")
    
    output = []
    output.append("/**")
    output.append(f" * {description}")
    output.append(f" * @module tokens/{name}")
    output.append(" */")
    output.append("")
    
    # For brand tokens, add imports for option tokens
    if is_brand:
        output.append("// Import option tokens for reference")
        output.append("import optionColors from '../../option-tokens/colors';")
        output.append("import optionScale from '../../option-tokens/scale';")
        output.append("import optionFont from '../../option-tokens/font';")
        output.append("")
    
    output.append("const tokens = {")
    
    # For brand tokens, handle components and system tokens
    if is_brand:
        if component_groups and normalized_name in component_groups:
            # Process component tokens
            for comp_name, tokens_list in sorted(component_groups[normalized_name].items()):
                # Create a section for each component
                output.append("")
                output.append(f"  /* ================ {comp_name.upper()} COMPONENT TOKENS ================ */")
                output.append("")
                
                # Process tokens for this component
                for token_path in tokens_list:
                    if token_path in tokens:
                        token_data = tokens[token_path]
                        value = token_data["value"]
                        token_type = token_data["type"]
                        
                        # Format semantic name similar to JS version
                        parts = token_path.split(".")
                        original_name = parts[-1].lower()
                        formatted_name = format_semantic_token_name(comp_name, token_path, original_name)
                        
                        # Format the value for JS
                        formatted_value = format_token_value(value, token_type, is_brand_file=True)
                        
                        output.append(f"  '{formatted_name}': {formatted_value},")
                
                output.append("")
        
        # Process system tokens
        if system_groups and normalized_name in system_groups:
            for system_name, tokens_list in sorted(system_groups[normalized_name].items()):
                if tokens_list:
                    output.append(f"// ================ SYSTEM: {system_name.upper()} TOKENS ================")
                    output.append("")
                    
                    for token_path in tokens_list:
                        if token_path in tokens:
                            token_data = tokens[token_path]
                            value = token_data["value"]
                            token_type = token_data["type"]
                            
                            # Create system token name
                            parts = token_path.split(".")
                            original_name = parts[-1].lower()
                            
                            # Determine property type
                            property_type = identify_property_type(token_path, original_name)
                            
                            # Get state/variant
                            state = identify_state(token_path, original_name)
                            variant = identify_variant(token_path, original_name)
                            
                            # Clean token name
                            token_name = re.sub(r'[^\w-]', '-', original_name)
                            token_name = re.sub(r'-+', '-', token_name)
                            token_name = re.sub(r'^-|-$', '', token_name)
                            
                            # Format system token name
                            if system_name != "other":
                                system_token_name = f"system-{system_name}-{token_name}"
                            else:
                                # More specific naming for "other" category
                                if property_type != "base":
                                    system_token_name = f"system-{property_type}-{token_name}"
                                else:
                                    system_token_name = f"system-{token_name}"
                            
                            # Clean up any duplicate parts in the name
                            system_token_name = re.sub(r'([a-z-]+)-\1', r'\1', system_token_name)
                            system_token_name = re.sub(r'-+', '-', system_token_name)
                            
                            # Format the value for SCSS with direct token resolution
                            scss_value = format_scss_token_value(value, token_type, token_sets)
                            
                            output.append(f"${system_token_name}: {scss_value};")
                    
                    output.append("")
    
    # Add SCSS mixins to make token usage easier
    if is_brand:
        brand_prefix = name.replace("-", "")
        output.append("// Mixins for easy token access")
        output.append("@mixin brand-tokens() {")
        output.append("  // Include all brand tokens as CSS custom properties")
        output.append("  @each $name, $value in $brand-tokens {")
        output.append("    --#{$name}: #{$value};")
        output.append("  }")
        output.append("}")
        output.append("")
    
    return "\n".join(output)

def generate_scss_index_file():
    """Generate the main SCSS file that imports all token files."""
    output = []
    output.append("// Design Token System")
    output.append("// Generated by token-extractor.py")
    output.append("")
    output.append("// Option Tokens")
    output.append(f"@import './option-tokens/{CONFIG['scssFileStructure']['optionTokens']['colors']}';")
    output.append(f"@import './option-tokens/{CONFIG['scssFileStructure']['optionTokens']['scale']}';")
    output.append(f"@import './option-tokens/{CONFIG['scssFileStructure']['optionTokens']['font']}';")
    output.append("")
    output.append("// Semantic Tokens")
    output.append(f"@import './semantic-tokens/brands/{CONFIG['scssFileStructure']['semanticTokens']['brands']['evydCore']}';")
    output.append(f"@import './semantic-tokens/brands/{CONFIG['scssFileStructure']['semanticTokens']['brands']['bruHealth']}';")
    output.append(f"@import './semantic-tokens/{CONFIG['scssFileStructure']['semanticTokens']['themes']}';")
    output.append("")
    output.append("// Usage Example:")
    output.append("// .my-component {")
    output.append("//   background-color: $card-background-default;")
    output.append("//   color: $button-text-primary;")
    output.append("//   padding: $scale-spacing-md;")
    output.append("//   font-family: $font-family-base;")
    output.append("// }")
    output.append("")
    
    return "\n".join(output)

def validate_token_structure(tokens_data):
    """
    Validate that the token file has the expected structure.
    
    Args:
        tokens_data: The raw JSON data from the token file
        
    Returns:
        (bool, str) tuple with validation result and error message
    """
    # Check if the data is a dictionary
    if not isinstance(tokens_data, dict):
        return False, "Token data is not a dictionary"
    
    # Basic validation of expected top-level keys
    required_sections = ["color", "scale", "font"]
    missing_sections = [section for section in required_sections if section not in tokens_data]
    
    if missing_sections:
        return False, f"Missing required token sections: {', '.join(missing_sections)}"
    
    # Check if brands exist
    brands_found = []
    if "brands" in tokens_data:
        for brand in ["EVYDCore", "BruHealth"]:
            if brand in tokens_data["brands"]:
                brands_found.append(brand)
    
    if not brands_found:
        return True, "Warning: No brand tokens found. This may be expected if only option tokens are used."
    
    return True, f"Token structure validated. Found brands: {', '.join(brands_found)}"

def read_tokens(file_path):
    """
    Read and parse a token studio JSON file.
    
    Args:
        file_path: Path to the token file
        
    Returns:
        Dictionary of parsed tokens
    """
    print(f"Reading tokens from: {file_path}")
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Token file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tokens_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON file: {e}")
                print(f"The file {file_path} does not contain valid JSON")
                raise
        
        # Validate token structure
        is_valid, message = validate_token_structure(tokens_data)
        if not is_valid:
            print(f"WARNING: {message}")
            print("Continuing with processing, but output may be incomplete")
        else:
            print(message)
        
        # Flatten the token structure for easier processing
        flattened_tokens = {}
        
        def flatten_tokens(data, prefix=""):
            if not isinstance(data, dict):
                print(f"WARNING: Expected dictionary but got {type(data)} at {prefix}")
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
                        "originalPath": token_path,
                        "description": value.get("description", "")
                    }
                else:
                    # This might be a malformed token
                    token_path = f"{prefix}.{key}" if prefix else key
                    print(f"WARNING: Unexpected token structure at {token_path}")
        
        flatten_tokens(tokens_data)
        
        if not flattened_tokens:
            print("WARNING: No tokens found after flattening. Check the token file structure.")
        else:
            print(f"Processed {len(flattened_tokens)} tokens")
            
        return flattened_tokens
    
    except Exception as e:
        print(f"Error reading token file: {e}")
        print("This might indicate an issue with the token file format or location.")
        print("Please check the token file path and ensure it follows the expected structure.")
        raise

def identify_component(token_path):
    """
    Identify if a token belongs to a component based on its path.
    
    Args:
        token_path: The token path to analyze
        
    Returns:
        Component name if identified, None otherwise
    """
    # Extract parts of the path
    parts = token_path.lower().split(".")
    token_name = parts[-1].lower()
    
    # Direct component reference in path
    for comp in COMPONENT_TYPES:
        if comp in parts or comp in token_name:
            return comp
    
    # Checking combined terms
    path_string = token_path.lower()
    for comp in COMPONENT_TYPES:
        if comp + "-" in path_string or comp + "_" in path_string:
            return comp
    
    # Additional checks for special cases
    if "btn" in parts or "btn-" in path_string or "btn_" in path_string:
        return "button"
    
    # No component identified
    return None

def identify_system_group(token_path):
    """
    Identify the system group for non-component tokens.
    
    Args:
        token_path: The token path to analyze
        
    Returns:
        System group name
    """
    # Extract parts of the path
    parts = token_path.lower().split(".")
    token_name = parts[-1].lower()
    path_string = token_path.lower()
    
    # Check for layout tokens
    if any(term in path_string for term in ["layout", "grid", "container", "spacing"]):
        return "layout"
    
    # Check for background tokens
    if any(term in path_string for term in ["background", "bg-", "bg_", "-bg", "_bg"]):
        return "background"
    
    # Check for text tokens
    if any(term in path_string for term in ["text", "font", "typography", "label"]):
        return "text"
    
    # Check for border tokens
    if any(term in path_string for term in ["border", "outline", "stroke"]):
        return "border"
    
    # Check for icon tokens
    if "icon" in path_string:
        return "icon"
    
    # Check for interactive tokens
    if any(term in path_string for term in ["hover", "active", "focus", "disabled", "pressed"]):
        return "interactive"
    
    # Check for feedback tokens
    if any(term in path_string for term in ["success", "error", "warning", "info", "alert"]):
        return "feedback"
    
    # Default to other
    return "other"

def write_to_file(content, directory, filename):
    """
    Write content to a file in the specified directory.
    
    Args:
        content: The content to write
        directory: The directory to write to
        filename: The filename to use
    """
    # Ensure the directory exists
    ensure_directory_exists(directory)
    
    # Full file path
    file_path = os.path.join(directory, filename)
    
    # Write the content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created file: {file_path}")

def create_scss_index():
    """
    Create the main SCSS index file that imports all token modules.
    """
    output = []
    output.append("/**")
    output.append(" * Design Tokens - Main SCSS Entry Point")
    output.append(" * Auto-generated by token-extractor.py")
    output.append(" */")
    output.append("")
    output.append("// Option Tokens")
    output.append("@import 'option-tokens/colors';")
    output.append("@import 'option-tokens/scale';")
    output.append("@import 'option-tokens/font';")
    output.append("")
    output.append("// Semantic Tokens - Brands")
    output.append("@import 'semantic-tokens/brands/evyd-core';")
    output.append("@import 'semantic-tokens/brands/bruhealth';")
    output.append("")
    output.append("// Usage Example:")
    output.append("//")
    output.append("// .my-component {")
    output.append("//   background-color: $button-background-primary;")
    output.append("//   color: $button-text-primary;")
    output.append("//   padding: $scale-spacing-md;")
    output.append("//   border-radius: $button-radius;")
    output.append("// }")
    
    # Write the index file
    write_to_file('\n'.join(output), CONFIG["scssOutputPath"], "_tokens.scss")

def organize_option_colors(tokens):
    """
    Organize color option tokens into logical categories with improved naming conventions.
    
    Returns a dictionary with the following categories:
    - brand: Brand-specific colors
    - neutral: Neutral/gray colors
    - semantic: Colors with functional meaning (success, warning, error, info)
    - palette: Full color spectrum organized by hue
    - other: Uncategorized colors
    """
    categories = {
        "brand": {
            "primary": {},
            "secondary": {},
            "accent": {},
            "other": {}
        },
        "neutral": {},
        "semantic": {
            "success": {},
            "warning": {},
            "error": {},
            "info": {}
        },
        "palette": {
            "red": {},
            "orange": {},
            "yellow": {},
            "green": {},
            "blue": {},
            "purple": {},
            "pink": {},
            "teal": {},
            "brown": {},
            "gray": {}
        },
        "other": {}
    }
    
    # Define regex patterns for each category
    patterns = {
        "brand": {
            "primary": [r'primary', r'main', r'brand\-?main', r'principal'],
            "secondary": [r'secondary', r'brand\-?secondary'],
            "accent": [r'accent', r'highlight']
        },
        "neutral": [r'neutral', r'gray', r'grey', r'white', r'black', r'stone'],
        "semantic": {
            "success": [r'success', r'valid', r'positive', r'confirm', r'green'],
            "warning": [r'warning', r'caution', r'alert', r'attention', r'yellow', r'amber', r'orange'],
            "error": [r'error', r'danger', r'invalid', r'negative', r'failure', r'red'],
            "info": [r'info', r'notification', r'note', r'blue']
        },
        "palette": {
            "red": [r'red', r'crimson', r'ruby', r'maroon'],
            "orange": [r'orange', r'tangerine', r'amber'],
            "yellow": [r'yellow', r'gold', r'lemon'],
            "green": [r'green', r'emerald', r'lime', r'jade'],
            "blue": [r'blue', r'azure', r'cerulean', r'sapphire'],
            "purple": [r'purple', r'violet', r'lavender', r'indigo'],
            "pink": [r'pink', r'magenta', r'fuchsia', r'rose'],
            "teal": [r'teal', r'turquoise', r'aqua', r'cyan'],
            "brown": [r'brown', r'chocolate', r'coffee', r'tan'],
            "gray": [r'gray', r'grey']
        }
    }
    
    # Parse hex values to categorize by hue analysis for undefined colors
    def categorize_by_hex(hex_value):
        if not isinstance(hex_value, str) or not hex_value.startswith('#'):
            return None
        
        try:
            # Basic hue categorization based on hex values
            r = int(hex_value[1:3], 16)
            g = int(hex_value[3:5], 16)
            b = int(hex_value[5:7], 16)
            
            # Calculate lightness - used for neutral detection
            lightness = (r + g + b) / (3 * 255)
            
            # Detect if it's a neutral/gray color (all channels close to each other)
            max_diff = max(abs(r - g), abs(r - b), abs(g - b))
            if max_diff < 20:
                return "neutral"
            
            # Find dominant color by hue
            if r > g and r > b:
                if g > b * 1.5:
                    return "orange" if g > r * 0.65 else "red"
                return "red"
            elif g > r and g > b:
                if r > b * 1.5:
                    return "yellow" if r > g * 0.65 else "green"
                return "green"
            elif b > r and b > g:
                if r > g * 1.5:
                    return "purple" if r > b * 0.5 else "blue"
                return "blue"
            else:
                return "other"
        except:
            return "other"
    
    # Function to standardize token naming
    def standardize_name(token_path, category, subcategory=None):
        # Extract name parts
        parts = token_path.split('/')[-1].split('.')
        original_name = parts[-1]
        
        # Skip deprecated tokens
        if "-depr" in original_name.lower():
            return None
        
        # Basic naming standardization
        if category == "brand":
            if subcategory:
                prefix = f"color-brand-{subcategory}"
            else:
                prefix = "color-brand"
        elif category == "neutral":
            prefix = "color-neutral"
        elif category == "semantic":
            if subcategory:
                prefix = f"color-{subcategory}"
            else:
                prefix = "color-semantic"
        elif category == "palette":
            if subcategory:
                prefix = f"color-{subcategory}"
            else:
                prefix = "color-palette"
        else:
            prefix = "color"
        
        # Keep original color name but clean it
        cleaned_name = re.sub(r'[^a-zA-Z0-9\-]', '', original_name)
        # Remove any -depr suffix if it exists
        cleaned_name = re.sub(r'-depr.*$', '', cleaned_name)
        return f"{prefix}-{cleaned_name}"
    
    # Process each token
    for token_path, token_data in tokens.items():
        value = token_data.get("value", "")
        
        # Skip deprecated tokens
        if "-depr" in token_path.lower():
            continue
            
        categorized = False
        
        # Get the last part of the path for easier matching
        path_parts = token_path.split('/')
        token_name = path_parts[-1].lower()
        
        # Check brand colors first
        for brand_type, patterns_list in patterns["brand"].items():
            if any(re.search(pattern, token_name, re.IGNORECASE) for pattern in patterns_list):
                categories["brand"][brand_type][standardize_name(token_path, "brand", brand_type)] = value
                categorized = True
                break
        
        if not categorized:
            # Check neutral colors
            if any(re.search(pattern, token_name, re.IGNORECASE) for pattern in patterns["neutral"]):
                categories["neutral"][standardize_name(token_path, "neutral")] = value
                categorized = True
        
        if not categorized:
            # Check semantic colors
            for semantic_type, patterns_list in patterns["semantic"].items():
                if any(re.search(pattern, token_name, re.IGNORECASE) for pattern in patterns_list):
                    categories["semantic"][semantic_type][standardize_name(token_path, "semantic", semantic_type)] = value
                    categorized = True
                    break
        
        if not categorized:
            # Check palette colors
            for palette_type, patterns_list in patterns["palette"].items():
                if any(re.search(pattern, token_name, re.IGNORECASE) for pattern in patterns_list):
                    categories["palette"][palette_type][standardize_name(token_path, "palette", palette_type)] = value
                    categorized = True
                    break
        
        if not categorized:
            # Try to categorize by hex value if not already categorized
            if isinstance(value, str) and value.startswith('#'):
                color_type = categorize_by_hex(value)
                if color_type == "neutral":
                    categories["neutral"][standardize_name(token_path, "neutral")] = value
                elif color_type in categories["palette"]:
                    categories["palette"][color_type][standardize_name(token_path, "palette", color_type)] = value
                else:
                    categories["other"][standardize_name(token_path, "other")] = value
            else:
                categories["other"][standardize_name(token_path, "other")] = value
    
    return categories

def organize_option_scale(tokens):
    """
    Organize scale option tokens into logical categories with improved naming conventions.
    
    Returns a dictionary with the following categories:
    - spacing: Tokens related to spacing, gaps, margins and padding
    - sizing: Tokens related to component sizes and dimensions
    - radius: Tokens related to border-radius values
    - borders: Tokens related to border widths and strokes
    - elevation: Tokens related to z-index and elevation
    - other: Uncategorized scale tokens
    """
    categories = {
        "spacing": {},
        "sizing": {},
        "radius": {},
        "borders": {},
        "elevation": {},
        "other": {}
    }
    
    # Pattern matching for categorization with regex for better accuracy
    patterns = {
        "spacing": [r'spacing', r'space', r'gap', r'margin', r'padding', r'indent', r'inset'],
        "sizing": [r'size', r'width', r'height', r'scale', r'dimension'],
        "radius": [r'radius', r'corner', r'rounded', r'pill'],
        "borders": [r'border', r'stroke', r'outline', r'thickness'],
        "elevation": [r'elevation', r'z-?index', r'layer', r'level']
    }
    
    # Predefined size names for standardization
    size_names = {
        "none": 0,  # Mapping "none" to 0 for sorting purposes
        "2xs": 10,
        "xs": 20,
        "sm": 30,
        "md": 40,
        "lg": 50,
        "xl": 60,
        "2xl": 70,
        "3xl": 80,
        "4xl": 90,
        "pill": 100,  # Special case for border-radius
    }
    
    # Function to standardize token naming
    def standardize_name(token_path, category):
        # Extract name parts
        parts = token_path.split('/')[-1].split('.')
        original_name = parts[-1].lower()
        
        # Basic naming standardization
        prefix = f"scale-{category}"
        
        # Check if this matches a predefined size name
        for size_name in size_names.keys():
            if size_name in original_name:
                return f"{prefix}-{size_name}"
        
        # Check for numeric sizes
        numeric_match = re.search(r'(\d+)', original_name)
        if numeric_match:
            size_value = numeric_match.group(1)
            # Convert to closest t-shirt size if applicable
            if int(size_value) <= 1:
                return f"{prefix}-2xs"
            elif int(size_value) <= 2:
                return f"{prefix}-xs"
            elif int(size_value) <= 4:
                return f"{prefix}-sm"
            elif int(size_value) <= 8:
                return f"{prefix}-md"
            elif int(size_value) <= 16:
                return f"{prefix}-lg"
            elif int(size_value) <= 24:
                return f"{prefix}-xl"
            elif int(size_value) <= 32:
                return f"{prefix}-2xl"
            elif int(size_value) <= 48:
                return f"{prefix}-3xl"
            else:
                return f"{prefix}-4xl"
        
        # Default to cleaned original name
        clean_name = re.sub(r'[^a-zA-Z0-9\-]', '', original_name)
        return f"{prefix}-{clean_name}"
    
    # Helper function to sort tokens by size
    def sort_key_for_token(token_name):
        # Extract the size suffix
        for size_name, order in size_names.items():
            if size_name in token_name:
                return order
        
        # Extract numeric value if present
        match = re.search(r'(\d+)', token_name)
        if match:
            return int(match.group(1))
        
        # Default sort value
        return 1000  # Place at the end
    
    # Process each token
    for token_path, token_data in tokens.items():
        value = token_data.get("value", "")
        categorized = False
        
        # Get the last part of the path for easier matching
        path_parts = token_path.split('/')
        token_name = path_parts[-1].lower()
        
        # Check each category
        for category, patterns_list in patterns.items():
            if any(re.search(pattern, token_path.lower(), re.IGNORECASE) for pattern in patterns_list):
                standard_name = standardize_name(token_path, category)
                categories[category][standard_name] = value
                categorized = True
                break
        
        # Special handling for base tokens (from our previous work)
        if not categorized and "base" in token_path.lower():
            if "radius" in token_path.lower():
                standard_name = standardize_name(token_path, "radius")
                categories["radius"][standard_name] = value
                categorized = True
            elif "gap" in token_path.lower() or "padding" in token_path.lower():
                standard_name = standardize_name(token_path, "spacing")
                categories["spacing"][standard_name] = value
                categorized = True
            elif "width" in token_path.lower() or "height" in token_path.lower():
                standard_name = standardize_name(token_path, "sizing")
                categories["sizing"][standard_name] = value
                categorized = True
            elif not categorized:
                # Generic base token not further specified
                categories["other"][f"scale-base-{token_name}"] = value
                categorized = True
        
        # If not categorized, put in other
        if not categorized:
            clean_name = re.sub(r'[^a-zA-Z0-9\-]', '', token_name)
            categories["other"][f"scale-{clean_name}"] = value
    
    # Sort each category by standardized size order
    for category in categories:
        sorted_dict = {}
        for token_name in sorted(categories[category].keys(), key=sort_key_for_token):
            sorted_dict[token_name] = categories[category][token_name]
        categories[category] = sorted_dict
    
    return categories

def organize_option_font(tokens):
    """
    Organize font option tokens into logical categories with improved naming conventions.
    
    Returns a dictionary with the following categories:
    - family: Font family tokens
    - weight: Font weight tokens
    - size: Font size tokens
    - line-height: Line height tokens
    - letter-spacing: Letter spacing tokens
    - style: Font style tokens
    - system: System/composite typography tokens
    - other: Uncategorized typography tokens
    """
    categories = {
        "family": {},
        "weight": {},
        "size": {},
        "line-height": {},
        "letter-spacing": {},
        "style": {},
        "system": {},
        "other": {}
    }
    
    # Pattern matching for categorization
    patterns = {
        "family": [r'family', r'face', r'font-family', r'typeface'],
        "weight": [r'weight', r'bold', r'regular', r'medium', r'light', r'thin', r'thick', r'heavy', r'black', r'semibold'],
        "size": [r'size', r'font-size'],
        "line-height": [r'line-height', r'leading'],
        "letter-spacing": [r'letter-spacing', r'tracking', r'kerning'],
        "style": [r'style', r'italic', r'oblique', r'normal', r'decoration'],
        "system": [r'system', r'heading', r'body', r'caption', r'label', r'display', r'title', r'paragraph', r'text']
    }
    
    # Predefined font size names for standardization
    size_names = {
        "2xs": 10,
        "xs": 20,
        "sm": 30,
        "md": 40,
        "lg": 50,
        "xl": 60,
        "2xl": 70,
        "3xl": 80,
        "4xl": 90,
        "5xl": 100,
        "6xl": 110
    }
    
    # Font weights map for standardization
    weight_map = {
        "thin": 100,
        "extra-light": 200,
        "light": 300,
        "regular": 400,
        "normal": 400,
        "medium": 500,
        "semibold": 600,
        "semi-bold": 600,
        "bold": 700,
        "extra-bold": 800,
        "extrabold": 800,
        "black": 900,
        "heavy": 900
    }
    
    # Function to standardize token naming
    def standardize_name(token_path, category):
        # Extract name parts
        parts = token_path.split('/')[-1].split('.')
        original_name = parts[-1].lower()
        
        # Basic naming standardization
        prefix = f"font-{category}"
        
        # Special handling for different categories
        if category == "family":
            # For font families, use a simplified name
            family_name = re.sub(r'[^a-zA-Z0-9\-]', '', original_name)
            return f"{prefix}-{family_name}"
            
        elif category == "weight":
            # Check if it matches a standard weight name
            for weight_name in weight_map.keys():
                if weight_name in original_name:
                    return f"{prefix}-{weight_name}"
            
            # Check for numeric weights
            numeric_match = re.search(r'(\d+)', original_name)
            if numeric_match:
                weight_value = int(numeric_match.group(1))
                if weight_value <= 100:
                    return f"{prefix}-thin"
                elif weight_value <= 200:
                    return f"{prefix}-extra-light"
                elif weight_value <= 300:
                    return f"{prefix}-light"
                elif weight_value <= 400:
                    return f"{prefix}-regular"
                elif weight_value <= 500:
                    return f"{prefix}-medium"
                elif weight_value <= 600:
                    return f"{prefix}-semibold"
                elif weight_value <= 700:
                    return f"{prefix}-bold"
                elif weight_value <= 800:
                    return f"{prefix}-extra-bold"
                else:
                    return f"{prefix}-black"
            
            # Default
            return f"{prefix}-{original_name}"
            
        elif category == "size":
            # Check if it matches a standard size name
            for size_name in size_names.keys():
                if size_name in original_name:
                    return f"{prefix}-{size_name}"
            
            # Check for numeric sizes
            numeric_match = re.search(r'(\d+)', original_name)
            if numeric_match:
                size_value = float(numeric_match.group(1))
                # Map pixel values to t-shirt sizes
                if size_value <= 10:
                    return f"{prefix}-2xs"
                elif size_value <= 12:
                    return f"{prefix}-xs"
                elif size_value <= 14:
                    return f"{prefix}-sm"
                elif size_value <= 16:
                    return f"{prefix}-md"
                elif size_value <= 18:
                    return f"{prefix}-lg"
                elif size_value <= 20:
                    return f"{prefix}-xl"
                elif size_value <= 24:
                    return f"{prefix}-2xl"
                elif size_value <= 30:
                    return f"{prefix}-3xl"
                elif size_value <= 36:
                    return f"{prefix}-4xl"
                elif size_value <= 48:
                    return f"{prefix}-5xl"
                else:
                    return f"{prefix}-6xl"
            
            return f"{prefix}-{original_name}"
            
        elif category == "system":
            # For system typography, preserve semantic meaning
            system_type = ""
            for system_term in ["heading", "body", "caption", "label", "display", "title", "paragraph"]:
                if system_term in original_name:
                    system_type = system_term
                    break
            
            if system_type:
                # Check for level indicator
                level_match = re.search(r'(\d+)', original_name)
                if level_match:
                    return f"{prefix}-{system_type}-{level_match.group(1)}"
                else:
                    return f"{prefix}-{system_type}"
            else:
                return f"{prefix}-{original_name}"
        
        # Default: clean the original name and use it
        clean_name = re.sub(r'[^a-zA-Z0-9\-]', '', original_name)
        return f"{prefix}-{clean_name}"
    
    # Helper function to sort tokens
    def sort_key_for_token(token_name, category):
        if category == "size":
            # Sort by t-shirt size or numeric value
            for size_name, order in size_names.items():
                if size_name in token_name:
                    return order
                    
            # Extract numeric value if present
            match = re.search(r'(\d+)', token_name)
            if match:
                return int(match.group(1))
        
        elif category == "weight":
            # Sort by weight value
            for weight_name, order in weight_map.items():
                if weight_name in token_name:
                    return order
                    
            # Extract numeric value if present
            match = re.search(r'(\d+)', token_name)
            if match:
                return int(match.group(1))
        
        elif category == "system":
            # Sort system typography by type and level
            order = 1000
            
            # Basic order by type
            if "display" in token_name:
                order = 100
            elif "heading" in token_name:
                order = 200
            elif "title" in token_name:
                order = 300
            elif "body" in token_name:
                order = 400
            elif "paragraph" in token_name:
                order = 500
            elif "label" in token_name:
                order = 600
            elif "caption" in token_name:
                order = 700
            
            # Adjust by level if present
            level_match = re.search(r'(\d+)', token_name)
            if level_match:
                order += int(level_match.group(1))
                
            return order
        
        # Default sort alphabetically
        return token_name
    
    # Process each token
    for token_path, token_data in tokens.items():
        value = token_data.get("value", "")
        categorized = False
        
        # Get the last part of the path for easier matching
        path_parts = token_path.split('/')
        token_name = '/'.join(path_parts).lower()  # Use full path for better matching
        
        # Check each category
        for category, patterns_list in patterns.items():
            if any(re.search(pattern, token_name, re.IGNORECASE) for pattern in patterns_list):
                standard_name = standardize_name(token_path, category)
                categories[category][standard_name] = value
                categorized = True
                break
        
        # If not categorized, put in other
        if not categorized:
            original_name = path_parts[-1].lower()
            clean_name = re.sub(r'[^a-zA-Z0-9\-]', '', original_name)
            categories["other"][f"font-{clean_name}"] = value
    
    # Sort each category
    for category, tokens_dict in categories.items():
        sorted_dict = {}
        for token_name in sorted(tokens_dict.keys(), 
                                key=lambda x: sort_key_for_token(x, category)):
            sorted_dict[token_name] = tokens_dict[token_name]
        categories[category] = sorted_dict
    
    return categories

def generate_scss_module(tokens, name, description, component_groups=None, system_groups=None, token_sets=None):
    """
    Generate SCSS variables from token data with improved documentation and organization.
    
    Args:
        tokens: The tokens to generate SCSS for
        name: The name of the module
        description: Description of the module
        component_groups: Optional component groupings
        system_groups: Optional system-level groups
        token_sets: Optional full token set for resolving token references
    """
    is_brand = name in ["evydcore", "bruhealth"]
    is_option = name in ["colors", "scale", "font"]
    normalized_name = name.replace("-", "")
    
    # Print some debug info
    print(f"\nDEBUG: Generate_scss_module for {name}")
    print(f"  is_brand: {is_brand}, normalized_name: {normalized_name}")
    print(f"  Number of tokens: {len(tokens)}")
    if is_brand and component_groups and normalized_name in component_groups:
        print(f"  Component groups: {len(component_groups[normalized_name])}")
    
    output = []
    
    # Add comprehensive documentation
    if is_option:
        output.append(f"/**")
        output.append(f" * Design Tokens - {description}")
        output.append(f" * ")
        output.append(f" * This file contains {name} tokens for the design system.")
        output.append(f" * Generated automatically - DO NOT EDIT DIRECTLY")
        output.append(f" *")
        
        if name == "colors":
            output.append(f" * Naming convention:")
            output.append(f" * $color-[category]-[variant]: Where category is brand, neutral, semantic, etc., and variant is the color variation")
            output.append(f" * ")
            output.append(f" * Example usage:")
            output.append(f" * .element {{")
            output.append(f" *   background-color: $color-brand-primary;")
            output.append(f" *   color: $color-text-primary;")
            output.append(f" * }}")
        elif name == "scale":
            output.append(f" * Naming convention:")
            output.append(f" * $scale-[category]-[size]: Where category is spacing, sizing, radius, etc., and size is based on t-shirt sizing")
            output.append(f" * ")
            output.append(f" * Size scale: none < 2xs < xs < sm < md < lg < xl < 2xl < 3xl < 4xl")
            output.append(f" * ")
            output.append(f" * Example usage:")
            output.append(f" * .element {{")
            output.append(f" *   margin: $scale-spacing-md;")
            output.append(f" *   padding: $scale-spacing-sm $scale-spacing-md;")
            output.append(f" *   border-radius: $scale-radius-sm;")
            output.append(f" * }}")
        elif name == "font":
            output.append(f" * Naming convention:")
            output.append(f" * $font-[category]-[variant]: Where category is family, weight, size, etc., and variant is the specific value")
            output.append(f" * ")
            output.append(f" * Example usage:")
            output.append(f" * .element {{")
            output.append(f" *   font-family: $font-family-primary;")
            output.append(f" *   font-size: $font-size-md;")
            output.append(f" *   font-weight: $font-weight-bold;")
            output.append(f" * }}")
            
        output.append(f" */")
    else:
        # Brand/semantic tokens documentation
        output.append(f"/**")
        output.append(f" * {description}")
        output.append(f" * ")
        output.append(f" * This file contains component-specific design tokens for the {name} brand.")
        output.append(f" * Generated automatically - DO NOT EDIT DIRECTLY")
        output.append(f" *")
        output.append(f" * Naming convention:")
        output.append(f" * $component-[name]-[property]-[variant]-[state]: Structured component tokens")
        output.append(f" * ")
        output.append(f" * Example usage:")
        output.append(f" * .button {{")
        output.append(f" *   background-color: $component-button-background;")
        output.append(f" *   color: $component-button-text;")
        output.append(f" *   border-radius: $component-button-radius;")
        output.append(f" * }}")
        output.append(f" */")
    
    output.append("")
    
    # For option tokens, use our specialized organization
    if is_option:
        if name == "colors":
            categories = organize_option_colors(tokens)
            
            # Brand colors section
            if any(categories["brand"].values()):
                output.append("/* ================================================")
                output.append("   BRAND COLORS")
                output.append("   ================================================ */")
                output.append("")

                # Organize by primary, secondary, accent
                for brand_category, brand_tokens in categories["brand"].items():
                    if brand_tokens:
                        output.append(f"/* {brand_category.capitalize()} Brand Colors */")
                        for key, value in sorted(brand_tokens.items()):
                            scss_value = format_scss_token_value(value, "color", token_sets)
                            output.append(f"${key}: {scss_value};")
                        output.append("")
            
            # Semantic colors section
            if any(categories["semantic"].values()):
                output.append("/* ================================================")
                output.append("   SEMANTIC COLORS")
                output.append("   ================================================ */")
                output.append("")
                
                # Success colors
                if categories["semantic"]["success"]:
                    output.append("/* Success Colors */")
                    for key, value in sorted(categories["semantic"]["success"].items()):
                        scss_value = format_scss_token_value(value, "color", token_sets)
                        output.append(f"${key}: {scss_value};")
                    output.append("")
                
                # Warning colors
                if categories["semantic"]["warning"]:
                    output.append("/* Warning Colors */")
                    for key, value in sorted(categories["semantic"]["warning"].items()):
                        scss_value = format_scss_token_value(value, "color", token_sets)
                        output.append(f"${key}: {scss_value};")
                    output.append("")
                
                # Error colors
                if categories["semantic"]["error"]:
                    output.append("/* Error Colors */")
                    for key, value in sorted(categories["semantic"]["error"].items()):
                        scss_value = format_scss_token_value(value, "color", token_sets)
                        output.append(f"${key}: {scss_value};")
                    output.append("")
                
                # Info colors
                if categories["semantic"]["info"]:
                    output.append("/* Info Colors */")
                    for key, value in sorted(categories["semantic"]["info"].items()):
                        scss_value = format_scss_token_value(value, "color", token_sets)
                        output.append(f"${key}: {scss_value};")
                    output.append("")
            
            # Neutral colors section
            if categories["neutral"]:
                output.append("/* ================================================")
                output.append("   NEUTRAL COLORS")
                output.append("   ================================================ */")
                output.append("")
                for key, value in sorted(categories["neutral"].items()):
                    scss_value = format_scss_token_value(value, "color", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Color palettes section
            if any(categories["palette"].values()):
                output.append("/* ================================================")
                output.append("   COLOR PALETTES")
                output.append("   ================================================ */")
                output.append("")
                
                for palette, tokens in categories["palette"].items():
                    if tokens:
                        output.append(f"/* {palette.capitalize()} Palette */")
                        for key, value in sorted(tokens.items()):
                            scss_value = format_scss_token_value(value, "color", token_sets)
                            output.append(f"${key}: {scss_value};")
                        output.append("")
            
            # Other colors
            if categories["other"]:
                output.append("/* ================================================")
                output.append("   OTHER COLORS")
                output.append("   ================================================ */")
                output.append("")
                for key, value in sorted(categories["other"].items()):
                    scss_value = format_scss_token_value(value, "color", token_sets)
                    output.append(f"${key}: {scss_value};")
        
        elif name == "scale":
            categories = organize_option_scale(tokens)
            
            # Spacing section
            if categories["spacing"]:
                output.append("// ================ SPACING ================")
                output.append("")
                for key, value in sorted(categories["spacing"].items()):
                    scss_value = format_scss_token_value(value, "dimension", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Sizing section
            if categories["sizing"]:
                output.append("// ================ SIZING ================")
                output.append("")
                for key, value in sorted(categories["sizing"].items()):
                    scss_value = format_scss_token_value(value, "dimension", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Radius section
            if categories["radius"]:
                output.append("// ================ RADIUS ================")
                output.append("")
                for key, value in sorted(categories["radius"].items()):
                    scss_value = format_scss_token_value(value, "dimension", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Borders section
            if categories["borders"]:
                output.append("// ================ BORDERS ================")
                output.append("")
                for key, value in sorted(categories["borders"].items()):
                    scss_value = format_scss_token_value(value, "dimension", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Other scale tokens
            if categories["other"]:
                output.append("// ================ OTHER SCALE TOKENS ================")
                output.append("")
                for key, value in sorted(categories["other"].items()):
                    scss_value = format_scss_token_value(value, "dimension", token_sets)
                    output.append(f"${key}: {scss_value};")
        
        elif name == "font":
            categories = organize_option_font(tokens)
            
            # Font family section
            if categories["family"]:
                output.append("// ================ FONT FAMILIES ================")
                output.append("")
                for key, value in sorted(categories["family"].items()):
                    scss_value = format_scss_token_value(value, "fontFamily", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Font weight section
            if categories["weight"]:
                output.append("// ================ FONT WEIGHTS ================")
                output.append("")
                for key, value in sorted(categories["weight"].items()):
                    scss_value = format_scss_token_value(value, "fontWeight", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Font size section
            if categories["size"]:
                output.append("// ================ FONT SIZES ================")
                output.append("")
                for key, value in sorted(categories["size"].items()):
                    scss_value = format_scss_token_value(value, "dimension", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Line height section
            if categories["line-height"]:
                output.append("// ================ LINE HEIGHTS ================")
                output.append("")
                for key, value in sorted(categories["line-height"].items()):
                    scss_value = format_scss_token_value(value, "dimension", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Letter spacing section
            if categories["letter-spacing"]:
                output.append("// ================ LETTER SPACING ================")
                output.append("")
                for key, value in sorted(categories["letter-spacing"].items()):
                    scss_value = format_scss_token_value(value, "dimension", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Font style section
            if categories["style"]:
                output.append("// ================ FONT STYLES ================")
                output.append("")
                for key, value in sorted(categories["style"].items()):
                    scss_value = format_scss_token_value(value, "string", token_sets)
                    output.append(f"${key}: {scss_value};")
                output.append("")
            
            # Other font tokens
            if categories["other"]:
                output.append("// ================ OTHER TYPOGRAPHY TOKENS ================")
                output.append("")
                for key, value in sorted(categories["other"].items()):
                    scss_value = format_scss_token_value(value, "string", token_sets)
                    output.append(f"${key}: {scss_value};")
    
    # For brand tokens, handle components and system tokens
    elif is_brand:
        output.append("// Brand-specific tokens")
        output.append("")
        # Debug count of processed tokens
        processed_tokens_count = 0
        
        # Make sure we have component groups for this brand
        brand_comp_groups = component_groups.get(normalized_name, {}) if component_groups else {}
        brand_sys_groups = system_groups.get(normalized_name, {}) if system_groups else {}
        
        print(f"  Using component_groups[{normalized_name}]: {len(brand_comp_groups)} components")
        
        # Process component tokens
        if brand_comp_groups:
            for comp_name, tokens_list in sorted(brand_comp_groups.items()):
                if not tokens_list:
                    continue
                
                # Create a section for each component
                output.append(f"// ================ {comp_name.upper()} COMPONENT TOKENS ================")
                output.append("")
                
                # Process tokens for this component
                tokens_processed = 0
                for token_path in tokens_list:
                    # Debug for the first one
                    if tokens_processed < 1:
                        print(f"  Processing token: {token_path}")
                        print(f"  Token exists in tokens dict: {token_path in tokens}")
                    
                    # Check if this token exists in the tokens dictionary
                    if token_path in tokens:
                        token_data = tokens[token_path]
                        tokens_processed += 1
                        value = token_data["value"]
                        token_type = token_data["type"]
                        
                        # Debug only for the first token
                        if tokens_processed < 2:
                            print(f"  Token found with value: {value}, type: {token_type}")
                        
                        # Format semantic name similar to JS version
                        parts = token_path.split(".")
                        original_name = parts[-1].lower()
                        formatted_name = format_semantic_token_name(comp_name, token_path, original_name)
                        
                        # Format the value for SCSS
                        scss_value = format_scss_token_value(value, token_type, token_sets)
                        
                        output.append(f"${formatted_name}: {scss_value};")
                
                # Only add section if we processed tokens
                if tokens_processed > 0:
                    output.append(f"// {tokens_processed} tokens processed for {comp_name}")
                    output.append("")
                    processed_tokens_count += tokens_processed
        
        # Process system tokens
        if brand_sys_groups:
            for system_name, tokens_list in sorted(brand_sys_groups.items()):
                if not tokens_list:
                    continue
                
                # System header
                output.append(f"// ================ SYSTEM: {system_name.upper()} TOKENS ================")
                output.append("")
                
                # Process tokens for this system
                tokens_processed = 0
                for token_path in tokens_list:
                    # Check if this token exists in the tokens dictionary
                    if token_path in tokens:
                        token_data = tokens[token_path]
                        tokens_processed += 1
                        value = token_data["value"]
                        token_type = token_data["type"]
                        
                        # Create system token name
                        parts = token_path.split(".")
                        original_name = parts[-1].lower()
                        
                        # Determine property type
                        property_type = identify_property_type(token_path, original_name)
                        
                        # Get state/variant
                        state = identify_state(token_path, original_name)
                        variant = identify_variant(token_path, original_name)
                        
                        # Clean token name
                        token_name = re.sub(r'[^\w-]', '-', original_name)
                        token_name = re.sub(r'-+', '-', token_name)
                        token_name = re.sub(r'^-|-$', '', token_name)
                        
                        # Format system token name
                        if system_name != "other":
                            system_token_name = f"system-{system_name}-{token_name}"
                        else:
                            # More specific naming for "other" category
                            if property_type != "base":
                                system_token_name = f"system-{property_type}-{token_name}"
                            else:
                                system_token_name = f"system-{token_name}"
                        
                        # Clean up any duplicate parts in the name
                        system_token_name = re.sub(r'([a-z-]+)-\1', r'\1', system_token_name)
                        system_token_name = re.sub(r'-+', '-', system_token_name)
                        
                        # Format the value for SCSS with direct token resolution
                        scss_value = format_scss_token_value(value, token_type, token_sets)
                        
                        output.append(f"${system_token_name}: {scss_value};")
                
                # Only add section if we processed tokens
                if tokens_processed > 0:
                    output.append(f"// {tokens_processed} tokens processed for {system_name}")
                    output.append("")
                    processed_tokens_count += tokens_processed
        
        # Print debug info
        print(f"  Total tokens processed: {processed_tokens_count}")
        
        # Add total processed tokens for debugging
        output.append(f"// Total: {processed_tokens_count} tokens processed for {name}")
        output.append("")
        
        # Add SCSS mixins to make token usage easier
        output.append("// Mixins for easy token access")
        output.append("@mixin brand-tokens() {")
        output.append("  // Include all brand tokens as CSS custom properties")
        output.append("  @each $name, $value in $brand-tokens {")
        output.append("    --#{$name}: #{$value};")
        output.append("  }")
        output.append("}")
        output.append("")
    
    return "\n".join(output)

def main():
    """Main function to extract tokens and generate SCSS modules."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Update CONFIG with command-line arguments if provided
    if args.token_file:
        CONFIG["tokenStudioFile"] = args.token_file
    
    if args.js_output_path:
        CONFIG["jsOutputPath"] = args.js_output_path
    
    if args.scss_output_path:
        CONFIG["scssOutputPath"] = args.scss_output_path
    
    if args.generate_js:
        CONFIG["outputFormats"]["generateJS"] = True
    
    if args.generate_scss:
        CONFIG["outputFormats"]["generateSCSS"] = True
    
    # Set verbose mode
    verbose = args.verbose
    
    print("Starting token extraction process...")
    
    # Read the JSON token file for report-only mode
    if args.report_only:
        tokens = read_tokens(CONFIG["tokenStudioFile"])
        report = generate_token_change_report(tokens, args.cache_file, format=args.report_format)
        
        print("\nToken Change Report (Report-Only Mode):")
        print(report)
        
        # Save report to file if specified
        if args.report_file:
            try:
                with open(args.report_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"\nToken change report saved to: {args.report_file}")
            except Exception as e:
                print(f"Error saving token change report: {e}")
        
        return
    
    # Check if tokens have changed since last run
    token_file = CONFIG["tokenStudioFile"]
    tokens_changed, change_message = has_tokens_changed(token_file, args.cache_file)
    
    if not tokens_changed and not args.force:
        print(f"Tokens unchanged: {change_message}")
        print("Use --force to regenerate tokens anyway")
        return
    elif not tokens_changed and args.force:
        print(f"Tokens unchanged: {change_message}")
        print("Forcing regeneration due to --force flag")
    else:
        print(f"Tokens have changed: {change_message}")
    
    # Calculate file hash for caching
    current_hash = get_file_hash(token_file)
    
    # Clean SCSS output directory if we're generating SCSS files
    if CONFIG["outputFormats"]["generateSCSS"] and not args.dry_run:
        clean_scss_output_directory()
    
    # Read the JSON token file
    tokens = read_tokens(CONFIG["tokenStudioFile"])
    total_token_count = len(tokens)
    
    # Generate token change report
    report = generate_token_change_report(tokens, args.cache_file, format=args.report_format)
    print("\nToken Change Report:")
    print(report)
    
    # Save report to file if specified
    if args.report_file:
        try:
            with open(args.report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\nToken change report saved to: {args.report_file}")
        except Exception as e:
            print(f"Error saving token change report: {e}")
    
    print(f"\nProcessing {total_token_count} tokens...")
    
    # Extract and categorize all tokens
    extracted_tokens = process_tokens(tokens)
    option_tokens = extracted_tokens["optionTokens"]
    semantic_tokens = extracted_tokens["semanticTokens"]
    
    # Print detailed path information if verbose mode is on
    if verbose:
        print("\nDEBUG: Path format comparison")
    
    # Initialize component and system groups
    component_groups = {
        "evydcore": {},
        "bruhealth": {}
    }
    
    system_groups = {
        "evydcore": {},
        "bruhealth": {}
    }
    
    # Create token groups for brand-specific tokens
    for brand in semantic_tokens["brands"]:
        if brand in ["evydcore", "bruhealth"]:
            # Normalize brand name
            normalized_brand = brand.lower().replace("-", "")
            
            # Initialize system groups
            for system_name in SYSTEM_GROUPS:
                system_groups[normalized_brand][system_name] = []
            
            # Organize tokens by component
            for token_path, token_data in semantic_tokens["brands"][brand].items():
                # Try to identify the component from token path
                comp_name = identify_component(token_path)
                
                if comp_name:
                    # Add to component group
                    if comp_name not in component_groups[normalized_brand]:
                        component_groups[normalized_brand][comp_name] = []
                    
                    component_groups[normalized_brand][comp_name].append(token_path)
                else:
                    # Not a component token, add to system tokens
                    system_name = identify_system_group(token_path)
                    system_groups[normalized_brand][system_name].append(token_path)
    
    # Print component groups if verbose mode is on
    if verbose:
        print("\nDEBUG: Main function - Tokens in component groups:")
        for brand in ["evydcore", "bruhealth"]:
            print(f"\nBrand: {brand}")
            if brand in component_groups and component_groups[brand]:
                total_token_count = 0
                for comp_name, tokens_list in component_groups[brand].items():
                    if tokens_list:
                        total_token_count += len(tokens_list)
                        print(f"Component {comp_name}: {len(tokens_list)} tokens")
                        # Print a token path sample
                        if len(tokens_list) > 0:
                            sample_path = tokens_list[0]
                            print(f"  Sample path: {sample_path}")
                            semantic_tokens_for_brand = semantic_tokens["brands"][brand]
                            # Check if this token exists in semantic tokens
                            exists = sample_path in semantic_tokens_for_brand
                            print(f"  Exists in semantic tokens: {exists}")
                            
                            # Check path formats
                            if not exists:
                                # Try to find a matching token
                                for token_path in semantic_tokens_for_brand.keys():
                                    if token_path.endswith(sample_path.split(".")[-1]):
                                        print(f"  Found similar token: {token_path}")
                                        break
                print(f"Total token paths in component groups: {total_token_count}")
            else:
                print(f"No component groups for {brand}")
    
    # Create a token_sets dictionary for resolving token references
    token_sets = {
        "optionTokens": option_tokens,
        "semanticTokens": semantic_tokens
    }
    
    # Generate tokens based on configured output formats
    
    # Only print debug info in verbose mode
    if verbose:
        print("\nDEBUG: Before generate_scss_module for brands")
        for brand in ["evydcore", "bruhealth"]:
            brand_tokens = semantic_tokens["brands"][brand]
            if brand_tokens:
                print(f"Brand: {brand}, Tokens: {len(brand_tokens)}")
                
                # First check if component groups exist for this brand
                if brand in component_groups and component_groups[brand]:
                    print(f"  Component groups for {brand}: {len(component_groups[brand])}")
                    
                    # Check a sample component
                    sample_comp = next(iter(component_groups[brand].keys()))
                    if sample_comp and component_groups[brand][sample_comp]:
                        sample_path = component_groups[brand][sample_comp][0]
                        print(f"  Sample component path: {sample_path}")
                        print(f"  Path in brand tokens: {sample_path in brand_tokens}")
                        
                        # Manually check a few tokens
                        for i, token_path in enumerate(brand_tokens.keys()):
                            if i < 3:  # Just check the first 3
                                print(f"  Brand token path {i}: {token_path}")
    
    # Generate SCSS if configured
    if CONFIG["outputFormats"]["generateSCSS"]:
        print("\nGenerating SCSS variables...")
        
        # Skip file writing if in dry-run mode
        if not args.dry_run:
            # Ensure SCSS directories exist
            ensure_directory_exists(CONFIG["scssOutputPath"] + "/option-tokens")
            ensure_directory_exists(CONFIG["scssOutputPath"] + "/semantic-tokens/brands")
            
            # Generate SCSS for option tokens
            if option_tokens["colors"]:
                output_scss = generate_scss_module(
                    option_tokens["colors"], 
                    "colors", 
                    "Color token definitions",
                    token_sets=token_sets
                )
                write_to_file(output_scss, CONFIG["scssOutputPath"] + "/option-tokens", "_colors.scss")
            
            if option_tokens["scale"]:
                output_scss = generate_scss_module(
                    option_tokens["scale"], 
                    "scale", 
                    "Scale token definitions (spacing, sizing)",
                    token_sets=token_sets
                )
                write_to_file(output_scss, CONFIG["scssOutputPath"] + "/option-tokens", "_scale.scss")
            
            if option_tokens["font"]:
                output_scss = generate_scss_module(
                    option_tokens["font"], 
                    "font", 
                    "Typography token definitions",
                    token_sets=token_sets
                )
                write_to_file(output_scss, CONFIG["scssOutputPath"] + "/option-tokens", "_font.scss")
            
            # Debug brand info if in verbose mode
            if verbose:
                print("\nDEBUG: Before generating brand SCSS:")
                for brand_name in ["evydcore", "bruhealth"]:
                    brand_tokens = semantic_tokens["brands"][brand_name]
                    print(f"Brand: {brand_name}, Number of tokens: {len(brand_tokens)}")
                    if component_groups[brand_name]:
                        sample_comp = next(iter(component_groups[brand_name].keys()))
                        if sample_comp and component_groups[brand_name][sample_comp]:
                            sample_path = component_groups[brand_name][sample_comp][0]
                            print(f"  Sample component path: {sample_path}")
                            print(f"  Path in brand tokens: {sample_path in brand_tokens}")
                            
                            # Manually check a few tokens
                            for i, token_path in enumerate(brand_tokens.keys()):
                                if i < 3:  # Just check the first 3
                                    print(f"  Brand token path {i}: {token_path}")
            
            # Generate SCSS for brands
            for brand in semantic_tokens["brands"]:
                if brand in ["evydcore", "bruhealth"]:
                    normalized_brand = brand.lower().replace("-", "")
                    friendly_name = "EVYD Core" if brand == "evydcore" else "bruHealth"
                    
                    # Get the brand tokens
                    brand_tokens = semantic_tokens["brands"][brand]
                    
                    # Debug info only in verbose mode
                    if verbose:
                        print(f"\nDEBUG: Calling generate_scss_module for {brand}")
                        print(f"  Number of tokens: {len(brand_tokens)}")
                        print(f"  Number of component groups: {len(component_groups[normalized_brand]) if normalized_brand in component_groups else 0}")
                    
                    output_scss = generate_scss_module(
                        brand_tokens,
                        brand,
                        f"{friendly_name} brand-specific tokens",
                        component_groups=component_groups,
                        system_groups=system_groups,
                        token_sets=token_sets
                    )
                    
                    # Format output filename
                    output_name = "_evyd-core.scss" if brand == "evydcore" else "_bruhealth.scss"
                    write_to_file(output_scss, CONFIG["scssOutputPath"] + "/semantic-tokens/brands", output_name)
            
            # Create main SCSS entry point that imports all variables
            create_scss_index()
        else:
            print("Dry run mode: SCSS files would be generated but not written")
    
    # Generate JS if configured
    if CONFIG["outputFormats"]["generateJS"]:
        print("\nGenerating JavaScript modules...")
        if not args.dry_run:
            # JS generation logic would go here
            pass
        else:
            print("Dry run mode: JavaScript files would be generated but not written")
    
    # Update cache with the new run information (unless in dry-run mode)
    if not args.dry_run:
        update_cache_info(token_file, current_hash, total_token_count, args.cache_file)
    
    print(f"Token extraction complete! {total_token_count} tokens processed.")
    
    # Check if component sections were included
    for brand in ["evydcore", "bruhealth"]:
        if brand in component_groups and len(component_groups[brand]) > 0:
            print(f"Found {len(component_groups[brand])} component groups for {brand}.")
        else:
            print(f"No component groups found for {brand}.")
    
    print("Output files generated in:")
    if CONFIG["outputFormats"]["generateSCSS"]:
        print(f"- SCSS: {CONFIG['scssOutputPath']}")
    if CONFIG["outputFormats"]["generateJS"]:
        print(f"- JS: {CONFIG['jsOutputPath']}")

if __name__ == "__main__":
    main() 