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
import random
import traceback

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
        last_modified = datetime.datetime.now().isoformat()
        
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
    "tokenStudioFile": "token-studio/tokens.json",
    "jsOutputPath": "src/tokens",
    "scssOutputPath": "src/styles/tokens",
    
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

def process_tokens(flattened_tokens):
    """
    Process tokens from a flattened structure into organized categories.
    
    Args:
        flattened_tokens: Dictionary of flattened tokens from Token Studio
        
    Returns:
        Dictionary of processed tokens by category
    """
    # Print some sample tokens for debugging
    sample_tokens = list(flattened_tokens.items())[:5]
    for path, data in sample_tokens:
        print(f"Sample token: {path} = {data}")
    
    result = {
        "colors": {
            "semantic": {
                "error": {},
                "warning": {},
                "success": {},
                "info": {}
            },
            "neutral": {},
            "palette": {},
            "other": {}
        },
        "brandColors": {
            "bruhealth": {},
            "evydcore": {}
        },
        "font": {},
        "scale": {}
    }
    
    # Group tokens by their type for processing
    grouped_tokens = {
        "color": {},
        "brand": {},
        "font": {},
        "scale": {}
    }
    
    # First pass: Group tokens by their type
    for token_path, token_data in flattened_tokens.items():
        token_type = token_data.get("type", "").lower()
        
        # Group color tokens
        if token_type in ["color", "border", "background", "text-color"]:
            # Check if this is a brand color
            if any(brand in token_path.lower() for brand in ['brand', 'evyd', 'bruhealth']):
                grouped_tokens["brand"][token_path] = token_data
            else:
                grouped_tokens["color"][token_path] = token_data
        
        # Group font tokens
        elif token_type in ["text", "typography", "fontFamily", "fontWeight", "lineHeight", "letterSpacing", "fontSize"]:
            grouped_tokens["font"][token_path] = token_data
        
        # Group scale tokens (spacing, sizing, etc.)
        elif token_type in ["number", "dimension", "size", "spacing", "borderRadius"]:
            grouped_tokens["scale"][token_path] = token_data
    
    # Process token counts
    token_counts = {
        "color": len(grouped_tokens["color"]),
        "brand": len(grouped_tokens["brand"]),
        "font": len(grouped_tokens["font"]),
        "scale": len(grouped_tokens["scale"])
    }
    
    # Second pass: Process each token type using appropriate organizers
    # Process color tokens
    for token_path, token_data in grouped_tokens["color"].items():
        result["colors"] = organize_option_colors(token_path, token_data, result["colors"])
    
    # Process brand tokens
    for token_path, token_data in grouped_tokens["brand"].items():
        # Categorize by brand
        if 'bruhealth' in token_path.lower():
            brand = 'bruhealth'
            else:
            brand = 'evydcore'
        
        # Format the color name, taking the last part of the path
        parts = token_path.split('.')
        color_name = f"color-{brand}-{format_token_name(parts[-1])}"
        result["brandColors"][brand][color_name] = token_data['value']
    
    # Process font and scale tokens with our new organizers
    if grouped_tokens["font"]:
        result["font"] = organize_option_font(grouped_tokens["font"])
    
    if grouped_tokens["scale"]:
        result["scale"] = organize_option_scale(grouped_tokens["scale"])
    
    # Print token counts
    for token_type, count in token_counts.items():
        print(f"Processed {count} {token_type} tokens")
    
    # Print the result structure for debugging
    print("\nResult structure:")
    print(f"  Base colors: {len(result['colors'].get('neutral', {})) + len(result['colors'].get('palette', {}))} items")
    print(f"  Semantic colors: {sum(len(cat) for cat in result['colors'].get('semantic', {}).values())} items")
    print(f"  Brand colors:")
    for brand, colors in result['brandColors'].items():
        print(f"    {brand}: {len(colors)} items")
    if "font" in result:
        print(f"  Font tokens: {sum(len(cat) for cat in result['font'].values())} items")
    if "scale" in result:
        print(f"  Scale tokens: {sum(len(cat) for cat in result['scale'].values())} items")
    
    # Return the processed tokens
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

def format_scss_token_value(value, token_type, token_sets=None, max_depth=10):
    """
    Format a token value for SCSS.
    
    Args:
        value: The token value to format
        token_type: The type of token
        token_sets: Optional - the full token sets for resolving token references
        max_depth: Maximum recursion depth for resolving nested references
    
    Returns:
        Formatted SCSS value
    """
    # Prevent infinite recursion with circular references
    if max_depth <= 0:
        print(f"Warning: Maximum reference resolution depth reached. Possible circular reference: {value}")
        return str(value)
    
    # If it's a dictionary with a 'value' key, extract just the value
    if isinstance(value, dict) and 'value' in value:
        value = value['value']
    
    # Handle token references
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        # Get the token path from the reference
        token_path = value[1:-1]
        
        # Special handling for common spacing and sizing references
        if token_path.startswith("font.paragraph-indent.none"):
            return "0"
        
        if token_path.startswith("16px-scale"):
            # Extract percentage value from patterns like {16px-scale.12%}
            percentage_match = re.search(r'(\d+)%', token_path)
            if percentage_match:
                percentage = int(percentage_match.group(1))
                # Convert percentage to px value based on 16px base
                px_value = round(16 * percentage / 100)
                return f"{px_value}px"
            return "16px"  # Default fallback
        
        # Handle base.padding references
        if token_path.startswith("base.padding"):
            # Extract size number from patterns like base.padding.size-4
            size_match = re.search(r'size-(\d+)', token_path)
            if size_match:
                size_num = int(size_match.group(1))
                return f"{size_num * 4}px"
            
            if "none" in token_path:
                return "0"
            
            return "4px"  # Default padding
        
        # Handle base.gap references
        if token_path.startswith("base.gap"):
            # Extract size number from patterns like base.gap.size-4
            size_match = re.search(r'size-(\d+)', token_path)
            if size_match:
                size_num = int(size_match.group(1))
                return f"{size_num * 4}px"
            
            if "none" in token_path:
                return "0"
            
            return "8px"  # Default gap
        
        # Handle base.radius references
        if token_path.startswith("base.radius"):
            # Extract size number from patterns like base.radius.size-3
            size_match = re.search(r'size-(\d+)', token_path)
            if size_match:
                size_num = int(size_match.group(1))
                return f"{size_num * 2}px"
            
            if "pill" in token_path:
                return "999px"
            
            return "4px"  # Default radius
        
        # Handle font line-height references
        if token_path.startswith("font.line-height"):
            # Extract line height value
            height_match = re.search(r'\.(\d+)', token_path)
            if height_match:
                height_value = int(height_match.group(1))
                return f"{height_value}px"
            return "normal"
        
        # Handle font size references
        if token_path.startswith("font.size"):
            # Extract size value
            size_match = re.search(r'\.(\d+)', token_path)
            if size_match:
                size_value = int(size_match.group(1))
                return f"{size_value}px"
            return "16px"  # Default font size
        
        # Handle base.width/height references
        if token_path.startswith("base.width") or token_path.startswith("base.height"):
            # Extract size number
            size_match = re.search(r'size-(\d+)', token_path)
            if size_match:
                size_value = size_match.group(1)
                # Handle special case for size-4a
                if 'a' in size_value:
                    size_value = size_value.replace('a', '')
                    size_num = int(size_value)
                    return f"{size_num * 4 + 2}px"
                size_num = int(size_value)
                return f"{size_num * 4}px"
            return "auto"
        
        # If token_sets is provided, try to resolve the reference directly
        if token_sets:
            # Try to find the referenced token
            referenced_token = None
            
            # First check if the token exists directly in the flattened structure
            if token_path in token_sets:
                referenced_token = token_sets[token_path]
            
            # If we found the referenced token, resolve its value (recursively if needed)
            if referenced_token:
                referenced_value = referenced_token.get("value")
                if referenced_value:
                    # Recursively resolve nested references
                if isinstance(referenced_value, str) and referenced_value.startswith("{") and referenced_value.endswith("}"):
                        return format_scss_token_value(referenced_value, referenced_token.get("type", token_type), token_sets, max_depth - 1)
                else:
                        # Direct value, still needs formatting
                        return format_scss_token_value(referenced_value, referenced_token.get("type", token_type), token_sets, max_depth - 1)
        
        # If we couldn't resolve the reference, provide a fallback based on token type
        if token_type in ["number", "dimension", "spacing", "size", "borderRadius"]:
            # For scale tokens, use a reasonable default based on naming convention
            if "spacing" in token_path:
                return "8px"  # Default spacing
            elif "radius" in token_path:
                return "4px"  # Default radius
            elif "size" in token_path:
                return "16px"  # Default size
            else:
                return "4px"  # Generic default
        
        # Preserve the reference if we can't resolve it (for debugging)
        print(f"Warning: Could not resolve token reference: {value}")
        return value
    
    # Handle basic types based on token_type
    if token_type == "color":
        return value  # Colors can be returned as-is in SCSS
    
    if token_type in ["number", "dimension", "spacing", "size", "borderRadius"]:
        # Ensure numeric values have appropriate units if not provided
        if isinstance(value, (int, float)):
            # For spacing, size, etc., consider adding default units if needed
            return str(value)  # For now, just convert to string
        elif isinstance(value, str):
            # If it's already a string (like "10px"), return as is
            return value
    
    # For other types, just convert to string
    if isinstance(value, (int, float)):
        return str(value)
    
    if isinstance(value, str):
            return value
    
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
    Write content to a file.
    
    Args:
        content: Content to write
        directory: Directory to write to (can be empty if filename is a full path)
        filename: Filename to write to (can be a full path)
    """
    # Handle both directory + filename and full path in filename
    if directory and not os.path.isabs(filename):
    file_path = os.path.join(directory, filename)
    else:
        file_path = filename
    
    # Ensure the file path directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Print success
    if os.path.exists(file_path):
    print(f"Created file: {file_path}")
    else:
        print(f"Failed to create file: {file_path}")

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

def organize_option_colors(token_path, token_data, result_categories=None):
    """
    Organize color tokens into semantic, neutral, palette, and other categories.
    
    Args:
        token_path: Path of the token
        token_data: Token data containing type, value, etc.
        result_categories: Dictionary of color categories where tokens will be added
        
    Returns:
        Updated dictionary with token added to appropriate category
    """
    if result_categories is None:
        result_categories = {
            'semantic': {},
            'neutral': {},
            'palette': {},
            'other': {}
        }
    
    # Get token value and type
    token_value = token_data.get('value')
    token_type = token_data.get('type')
    
    # Skip non-color tokens
    if token_type != 'color':
        return result_categories
    
    # Skip deprecated tokens and tokens with "-depr" in the name
    if "depr" in token_path.lower():
        return result_categories
    
    # Skip dark theme tokens and tokens with "Dark (WIP)" in the path
    if "dark" in token_path.lower() or "Dark (WIP)" in token_path:
        return result_categories
    
    # Extract parts for analysis
    parts = token_path.split('.')
    token_name = parts[-1]  # Last part is the token name
    
    # Handle brand colors separately (they should be in brand-specific files)
    if "brands/" in token_path:
        return result_categories
    
    # Check for semantic colors first (error, warning, success, info)
    is_semantic = False
    semantic_keywords = ['error', 'warning', 'success', 'info', 'primary', 'secondary', 'tertiary', 
                         'brand', 'accent', 'danger', 'alert', 'notification']
    
    for keyword in semantic_keywords:
        if keyword in token_path.lower():
            is_semantic = True
            break
    
    if is_semantic:
        # Generate a semantic token name
        semantic_name = f"color-{token_name}".lower()
        
        # Check if this name already exists
        counter = 1
        original_name = semantic_name
        while semantic_name in result_categories['semantic']:
            semantic_name = f"{original_name}-{counter}"
            counter += 1
            
        result_categories['semantic'][semantic_name] = token_value
        return result_categories
    
    # Check if it's a neutral/stone color
    # Note: We now treat stone colors as regular palette colors, not neutral colors
    is_neutral = 'neutral' in token_path.lower() and 'neutral-depr' not in token_path.lower()
    
    if is_neutral:
        # Preserve original name for neutral colors
        if 'Light.color.neutral' in token_path:
            # Extract shade name
            parts = token_path.split('.')
            shade = parts[-1].lower()
            neutral_name = f"color-neutral-{shade}".lower()
            
            # Clean up the name - remove 'white' or 'black' from the variable name
            # These should be part of the description, not the variable name
            neutral_name = neutral_name.replace('-white', '')
            neutral_name = neutral_name.replace('-black', '')
            
            # Check if this name already exists
            counter = 1
            original_name = neutral_name
            while neutral_name in result_categories['neutral']:
                neutral_name = f"{original_name}-{counter}"
                counter += 1
                
            result_categories['neutral'][neutral_name] = token_value
            return result_categories
    
    # Check if it's a color palette
    is_palette = False
    for color_name in ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'teal', 'indigo', 
                       'cyan', 'amber', 'lime', 'emerald', 'violet', 'fuchsia', 'sky', 'turquoise', 
                       'cobalt', 'brick', 'marmalade', 'jade', 'merigold', 'grape', 'lemon', 
                       'cerulean', 'lavender', 'stone', 'crimson', 'sea', 'rose']:
        if color_name in token_path.lower():
            is_palette = True
            color_group = color_name
                    break
        
    if is_palette:
        # Format color name based on token path
        parts = token_path.split('.')
        shade = parts[-1].lower()
        
        # Handle special case for main colors with '-main' or '-pri' suffix
        color_name = f"color-{color_group}-{shade}".lower()
        
        # Clean up the name - remove 'white' or 'black' from the variable name
        # These should be part of the description, not the variable name
        color_name = color_name.replace(' white', '')
        color_name = color_name.replace(' black', '')
        
        # Check if this name already exists
        counter = 1
        original_name = color_name
        while color_name in result_categories['palette']:
            color_name = f"{original_name}-{counter}"
            counter += 1
            
        result_categories['palette'][color_name] = token_value
        return result_categories
    
    # For any other color that doesn't match the above categories
    other_name = f"color-{token_name}".lower()
    
    # Check if this name already exists
    counter = 1
    original_name = other_name
    while other_name in result_categories['other']:
        other_name = f"{original_name}-{counter}"
        counter += 1
        
    result_categories['other'][other_name] = token_value
    return result_categories

def organize_option_scale(tokens):
    """
    Organize scale option tokens into logical categories with improved naming conventions and subcategories.
    
    Returns a dictionary with the following categories:
    - spacing:
      - inset: Padding and margin tokens
      - gap: Gap and grid tokens
      - layout: Layout spacing
      - standard: Standardized spacing values
    - sizing:
      - width: Width-related tokens
      - height: Height-related tokens
      - font: Font size related dimensions
      - component: Component sizing
      - standard: Standardized size values
    - radius: Tokens related to border-radius values
    - borders: Tokens related to border widths and strokes
    - elevation: Tokens related to z-index and elevation
    - other: Uncategorized scale tokens
    """
    # Top-level categories
    categories = {
        "spacing": {
            "standard": {},
            "inset": {},
            "gap": {},
            "layout": {}
        },
        "sizing": {
            "standard": {},
            "width": {},
            "height": {},
            "font": {},
            "component": {}
        },
        "radius": {},
        "borders": {},
        "elevation": {},
        "other": {}
    }
    
    # Pattern matching for primary categorization
    primary_patterns = {
        "spacing": [r'spacing', r'space', r'gap', r'margin', r'padding', r'indent', r'inset'],
        "sizing": [r'size', r'width', r'height', r'scale', r'dimension'],
        "radius": [r'radius', r'corner', r'rounded', r'pill'],
        "borders": [r'border', r'stroke', r'outline', r'thickness'],
        "elevation": [r'elevation', r'z-?index', r'layer', r'level']
    }
    
    # Pattern matching for subcategories
    spacing_patterns = {
        "inset": [r'padding', r'margin', r'inset'],
        "gap": [r'gap', r'grid', r'column', r'row', r'gutter'],
        "layout": [r'layout', r'container', r'section', r'panel']
    }
    
    sizing_patterns = {
        "width": [r'width', r'w-'],
        "height": [r'height', r'h-'],
        "font": [r'font', r'text', r't-'],
        "component": [r'button', r'icon', r'avatar', r'input', r'card', r'component']
    }
    
    # Predefined size names for standardization and sorting
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
    def standardize_name(token_path, category, subcategory=None):
        # Extract name parts
        parts = token_path.split('/')[-1].split('.')
        original_name = parts[-1].lower()
        
        # Clean the token name (replace spaces with hyphens, ensure valid CSS variable name)
        clean_name = original_name.replace(' ', '-')
        clean_name = re.sub(r'[^\w\-]', '', clean_name)
        
        # Create standardized name based on category and optional subcategory
        if subcategory and subcategory != "standard":
            # Include subcategory in the name
            clean_name = f'scale-{category}-{subcategory}-{clean_name}'
            else:
            # Just use the main category
            clean_name = f'scale-{category}-{clean_name}'
        
        return clean_name
    
    # Helper function to sort tokens by size
    def sort_key_for_token(token_name):
        # First check for size designations like xs, sm, md, etc.
        for size_name, order in size_names.items():
            if f"-{size_name}" in token_name or f"-{size_name}-" in token_name:
                return order
        
        # Then extract numeric value if present
        numeric_matches = re.findall(r'(\d+)', token_name)
        if numeric_matches:
            # If there are multiple matches, use the last one as it's often the most specific
            return int(numeric_matches[-1])
        
        # Default sort value
        return 1000  # Place at the end
    
    # Process each token
    for token_path, token_data in tokens.items():
        value = token_data.get("value", "")
        categorized = False
        token_name = token_path.lower()
        
        # Skip deprecated tokens
        if "-depr" in token_name:
            continue
        
        # First determine the main category
        main_category = None
        for category, patterns in primary_patterns.items():
            if any(re.search(pattern, token_name, re.IGNORECASE) for pattern in patterns):
                main_category = category
                break
        
        # If no main category is found, use some heuristics
        if not main_category:
            if "base" in token_name:
                if "radius" in token_name:
                    main_category = "radius"
                elif "gap" in token_name or "padding" in token_name or "margin" in token_name:
                    main_category = "spacing"
                elif "width" in token_name or "height" in token_name or "size" in token_name:
                    main_category = "sizing"
        
        # Default to "other" if still no category
        if not main_category:
            main_category = "other"
        
        # For spacing and sizing, determine subcategory
        subcategory = "standard"  # Default subcategory
        
        if main_category == "spacing":
            # Determine spacing subcategory
            for subcat, patterns in spacing_patterns.items():
                if any(re.search(pattern, token_name, re.IGNORECASE) for pattern in patterns):
                    subcategory = subcat
                    break
            
            # Check for numeric patterns that indicate standard sizes
            if re.search(r'spacing-\d+', token_name) or re.search(r'space-\d+', token_name):
                subcategory = "standard"
                
            # Format the name and add to the right category
            standard_name = standardize_name(token_path, main_category, subcategory)
            categories[main_category][subcategory][standard_name] = value
                categorized = True
            
        elif main_category == "sizing":
            # Determine sizing subcategory
            for subcat, patterns in sizing_patterns.items():
                if any(re.search(pattern, token_name, re.IGNORECASE) for pattern in patterns):
                    subcategory = subcat
                break
        
            # Check for numeric patterns that indicate standard sizes
            if re.search(r'sizing-\d+', token_name) or re.search(r'size-\d+', token_name):
                subcategory = "standard"
                
            # Format the name and add to the right category
            standard_name = standardize_name(token_path, main_category, subcategory)
            categories[main_category][subcategory][standard_name] = value
                categorized = True
            
        elif main_category in ["radius", "borders", "elevation"]:
            # These don't have subcategories yet
            standard_name = standardize_name(token_path, main_category)
            categories[main_category][standard_name] = value
                categorized = True
        
        else:
            # For "other" category
            path_parts = token_path.split('/')
            original_name = path_parts[-1].lower()
            clean_name = original_name.replace(' ', '-')
            clean_name = re.sub(r'[^\w\-]', '', clean_name)
            categories["other"][f"scale-{clean_name}"] = value
    
    # Sort each category and subcategory
    result = {
        "spacing": {},
        "sizing": {},
        "radius": {},
        "borders": {},
        "elevation": {},
        "other": {}
    }
    
    # Sort spacing subcategories
    for subcategory in categories["spacing"]:
        sorted_dict = {}
        for token_name in sorted(categories["spacing"][subcategory].keys(), key=sort_key_for_token):
            sorted_dict[token_name] = categories["spacing"][subcategory][token_name]
        result["spacing"].update(sorted_dict)
    
    # Sort sizing subcategories
    for subcategory in categories["sizing"]:
        sorted_dict = {}
        for token_name in sorted(categories["sizing"][subcategory].keys(), key=sort_key_for_token):
            sorted_dict[token_name] = categories["sizing"][subcategory][token_name]
        result["sizing"].update(sorted_dict)
    
    # Sort remaining categories
    for category in ["radius", "borders", "elevation", "other"]:
        if isinstance(categories[category], dict):
        sorted_dict = {}
        for token_name in sorted(categories[category].keys(), key=sort_key_for_token):
            sorted_dict[token_name] = categories[category][token_name]
            result[category] = sorted_dict
    
    return result

def organize_option_font(tokens):
    """
    Organize font option tokens into logical categories with standardized naming.
    
    Returns a dictionary with the following categories:
    - family: Font family tokens
    - weight: Font weight tokens
    - size: Font size tokens
    - line-height: Line height tokens
    - letter-spacing: Letter spacing tokens
    - paragraph-spacing: Paragraph spacing tokens
    - paragraph-indent: Paragraph indent tokens
    - style: Font style tokens
    - system: System typography tokens (like heading, body, etc.)
    - other: Uncategorized typography tokens
    """
    categories = {
        "family": {},
        "weight": {},
        "size": {},
        "line-height": {},
        "letter-spacing": {},
        "paragraph-spacing": {},
        "paragraph-indent": {},
        "style": {},
        "system": {},
        "other": {}
    }
    
    # Pattern matching for categorization with regex for better accuracy
    patterns = {
        "family": [r'family', r'font-family', r'typeface', r'font$'],
        "weight": [r'weight', r'font-weight', r'bold', r'black', r'light', r'medium', r'regular', r'thin'],
        "size": [r'size', r'font-size', r'text-size', r'fontSize'],
        "line-height": [r'line-height', r'lineHeight', r'leading'],
        "letter-spacing": [r'letter-spacing', r'letterSpacing', r'tracking', r'character-spacing'],
        "paragraph-spacing": [r'paragraph-spacing', r'paragraphSpacing'],
        "paragraph-indent": [r'paragraph-indent', r'paragraphIndent', r'indent'],
        "style": [r'style', r'font-style', r'italic', r'oblique', r'normal'],
        "system": [r'heading', r'body', r'caption', r'label', r'display', r'title', r'overline', r'text-[lmsx]']
    }
    
    # Function to standardize token naming
    def standardize_name(token_path, category):
        # Extract name parts
        parts = token_path.split('/')[-1].split('.')
        original_name = parts[-1].lower()
        
        # Clean the token name (replace spaces with hyphens, ensure valid CSS variable name)
        clean_name = original_name.replace(' ', '-')
        # Remove any parentheses or special characters
        clean_name = re.sub(r'[^\w\-]', '', clean_name)
        # Create standardized name
        clean_name = f'font-{category}-{clean_name}'
        
        return clean_name
    
    # Custom sorting function for font sizes and weights
    def sort_key_for_font(token_name, category):
        if category == "size":
            # Extract numeric value if present
            match = re.search(r'(\d+)', token_name)
            if match:
                return int(match.group(1))
            # Check for named sizes
            size_order = {"2xs": 10, "xs": 20, "sm": 30, "md": 40, "lg": 50, "xl": 60, "2xl": 70}
            for size, order in size_order.items():
                if size in token_name:
                    return order
        elif category == "weight":
            # Weight order from lightest to heaviest
            weight_order = {
                "thin": 10, 
                "extralight": 20, 
                "light": 30, 
                "regular": 40, 
                "medium": 50, 
                "semibold": 60, 
                "bold": 70, 
                "extrabold": 80, 
                "black": 90
            }
            for weight, order in weight_order.items():
                if weight in token_name:
                    # Add to order if italic
                    return order + (5 if "italic" in token_name else 0)
        
        # Default sort value
        return 1000  # Place at the end
    
    # Process each token
    for token_path, token_data in tokens.items():
        value = token_data.get("value", "")
        categorized = False
        
        # Skip deprecated tokens
        if "-depr" in token_path.lower():
            continue
            
        # Get the path for better matching
        token_name = token_path.lower()
        
        # Check each category
        for category, patterns_list in patterns.items():
            if any(re.search(pattern, token_name, re.IGNORECASE) for pattern in patterns_list):
                standard_name = standardize_name(token_path, category)
                categories[category][standard_name] = value
                categorized = True
                break
        
        # If not categorized, put in other
        if not categorized:
            path_parts = token_path.split('/')
            original_name = path_parts[-1].lower()
            clean_name = original_name.replace(' ', '-')
            clean_name = re.sub(r'[^\w\-]', '', clean_name)
            categories["other"][f"font-{clean_name}"] = value
    
    # Sort each category appropriately
    for category, tokens_dict in categories.items():
        # Convert to a list of tuples for easier sorting
        sorted_items = list(tokens_dict.items())
        
        # Apply category-specific sorting
        if category in ["size", "weight"]:
            sorted_items.sort(key=lambda x: sort_key_for_font(x[0], category))
        else:
            # Sort alphabetically by key for other categories
            sorted_items.sort(key=lambda x: str(x[0]))
        
        # Convert back to dictionary
        categories[category] = {k: v for k, v in sorted_items}
    
    return categories

def generate_font_scss(organized_font_tokens, description="Font tokens for the design system", token_sets=None):
    """
    Generate SCSS for font tokens with appropriate categories and documentation.
    
    Args:
        organized_font_tokens: Dictionary of organized font tokens
        description: Description for the SCSS file
        token_sets: Optional - Full token sets for resolving references
        
    Returns:
        String with SCSS content
    """
    output = []
    
    # Add documentation header
    output.append("/* ========================================================================")
    output.append("   #FONT TOKENS")
    output.append("   ======================================================================== */")
    output.append("")
    output.append("/**")
    output.append(f" * {description}")
    output.append(" * Generated by token-extractor.py")
    output.append(" */")
    output.append("")
    
    # Add each category
    for category, tokens in organized_font_tokens.items():
        if tokens:
            category_title = category.replace("-", " ").title()
            output.append(f"/* Font {category_title} */")
            
            for token_name, value in tokens.items():
                if isinstance(value, dict) and "value" in value:
                    value = value["value"]
                
                # Format the value using the token resolver function
                formatted_value = format_scss_token_value(value, "font", token_sets)
                output.append(f"${token_name}: {formatted_value};")
    
    output.append("")
    
    return "\n".join(output)

def generate_scale_scss(organized_scale_tokens, description="Scale tokens for the design system", token_sets=None):
    """
    Generate SCSS for scale tokens with improved category organization and documentation.
    
    Args:
        organized_scale_tokens: Dictionary of organized scale tokens
        description: Description for the SCSS file
        token_sets: Optional - Full token sets for resolving references
        
    Returns:
        String with SCSS content
    """
    output = []
    
    # Add documentation header
    output.append("/* ========================================================================")
    output.append("   #SCALE TOKENS")
    output.append("   ======================================================================== */")
                    output.append("")
    output.append("/**")
    output.append(f" * {description}")
    output.append(" * Generated by token-extractor.py")
    output.append(" */")
                    output.append("")
                
    # For spacing category
    if "spacing" in organized_scale_tokens and organized_scale_tokens["spacing"]:
        # Add main category header
        output.append("/* ========================================================================")
        output.append("   #SPACING")
        output.append("   ======================================================================== */")
                    output.append("")
                
        # Find tokens with specific prefixes to group them
        standard_tokens = {}
        inset_tokens = {}
        gap_tokens = {}
        other_spacing_tokens = {}
        
        # Separate tokens into subcategories based on their names
        for token_name, value in organized_scale_tokens["spacing"].items():
            if isinstance(value, dict) and "value" in value:
                value = value["value"]
                
            if "inset" in token_name or "padding" in token_name or "margin" in token_name:
                inset_tokens[token_name] = value
            elif "gap" in token_name:
                gap_tokens[token_name] = value
            elif re.search(r'spacing-\d+$', token_name):  # Standard numeric spacing
                standard_tokens[token_name] = value
            else:
                other_spacing_tokens[token_name] = value
        
        # Output standard spacing tokens
        if standard_tokens:
            output.append("/* Standard Spacing Values */")
            for token_name, value in standard_tokens.items():
                formatted_value = format_scss_token_value(value, "spacing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                    output.append("")
            
        # Output inset (padding/margin) tokens
        if inset_tokens:
            output.append("/* Padding & Margin (Inset) */")
            for token_name, value in inset_tokens.items():
                formatted_value = format_scss_token_value(value, "spacing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                output.append("")
            
        # Output gap tokens
        if gap_tokens:
            output.append("/* Gaps & Gutters */")
            for token_name, value in gap_tokens.items():
                formatted_value = format_scss_token_value(value, "spacing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                output.append("")
                
        # Output other spacing tokens
        if other_spacing_tokens:
            output.append("/* Other Spacing */")
            for token_name, value in other_spacing_tokens.items():
                formatted_value = format_scss_token_value(value, "spacing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                        output.append("")
            
    # For sizing category
    if "sizing" in organized_scale_tokens and organized_scale_tokens["sizing"]:
        # Add main category header
        output.append("/* ========================================================================")
        output.append("   #SIZING")
        output.append("   ======================================================================== */")
                output.append("")
        
        # Find tokens with specific prefixes to group them
        standard_tokens = {}
        width_tokens = {}
        height_tokens = {}
        font_tokens = {}
        component_tokens = {}
        other_sizing_tokens = {}
        
        # Separate tokens into subcategories based on their names
        for token_name, value in organized_scale_tokens["sizing"].items():
            if isinstance(value, dict) and "value" in value:
                value = value["value"]
                
            if "width" in token_name:
                width_tokens[token_name] = value
            elif "height" in token_name:
                height_tokens[token_name] = value
            elif "font" in token_name or "text" in token_name or token_name.startswith("$scale-sizing-t-"):
                font_tokens[token_name] = value
            elif any(x in token_name for x in ["button", "icon", "avatar", "card", "component"]):
                component_tokens[token_name] = value
            elif re.search(r'sizing-\d+$', token_name):  # Standard numeric sizing
                standard_tokens[token_name] = value
            else:
                other_sizing_tokens[token_name] = value
        
        # Output standard sizing tokens
        if standard_tokens:
            output.append("/* Standard Size Values */")
            for token_name, value in standard_tokens.items():
                formatted_value = format_scss_token_value(value, "sizing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                output.append("")
        
        # Output width tokens
        if width_tokens:
            output.append("/* Width Dimensions */")
            for token_name, value in width_tokens.items():
                formatted_value = format_scss_token_value(value, "sizing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                output.append("")
            
        # Output height tokens
        if height_tokens:
            output.append("/* Height Dimensions */")
            for token_name, value in height_tokens.items():
                formatted_value = format_scss_token_value(value, "sizing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                output.append("")
            
        # Output font-related size tokens
        if font_tokens:
            output.append("/* Typography Sizes */")
            for token_name, value in font_tokens.items():
                formatted_value = format_scss_token_value(value, "sizing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                output.append("")
            
        # Output component sizing tokens
        if component_tokens:
            output.append("/* Component Sizes */")
            for token_name, value in component_tokens.items():
                formatted_value = format_scss_token_value(value, "sizing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                output.append("")
        
        # Output other sizing tokens
        if other_sizing_tokens:
            output.append("/* Other Sizes */")
            for token_name, value in other_sizing_tokens.items():
                formatted_value = format_scss_token_value(value, "sizing", token_sets)
                output.append(f"${token_name}: {formatted_value};")
                output.append("")
            
    # Add remaining categories with their original format
    for category in ["radius", "borders", "elevation", "other"]:
        if category in organized_scale_tokens and organized_scale_tokens[category]:
            category_title = category.replace("-", " ").title()
            output.append(f"/* {category_title} Scale */")
            
            for token_name, value in organized_scale_tokens[category].items():
                if isinstance(value, dict) and "value" in value:
                    value = value["value"]
                
                # Format the value using the token resolver function
                formatted_value = format_scss_token_value(value, category, token_sets)
                output.append(f"${token_name}: {formatted_value};")
            
                output.append("")
            
    return "\n".join(output)

def generate_scss_module(tokens, name, description, component_groups=None, system_groups=None, token_sets=None):
    """
    Generate SCSS variables from token data with improved documentation and organization.
    Simplified to handle only base color tokens (no light/dark theme separation).
    """
    is_brand = name in ["evydcore", "bruhealth"]
    is_option = name in ["colors", "scale", "font"]
    normalized_name = name.replace("-", "")
    
    output = []
    
    # Add documentation header
    output.append("/**")
    output.append(f" * {description}")
    output.append(" * Generated by token-extractor.py")
    output.append(" */")
                output.append("")
    
    # For option tokens (colors, scale, font)
    if is_option:
        if name == "colors":
            # Function to sort colors from lightest to darkest
            def sort_by_color_tone(color_name):
                # Extract the shade number if present (like 50, 100, 200, etc.)
                shade_match = re.search(r'-(\d+)(?:-|$)', color_name)
                if shade_match:
                    shade = int(shade_match.group(1))
                    # Higher shade numbers typically mean lighter colors in design systems
                    return shade
                
                # If no number, check for light/dark keywords
                if "white" in color_name:
                    return 1000  # Make white appear first (lightest)
                if "light" in color_name:
                    return 900  # Light colors near the top
                if "black" in color_name:
                    return 0    # Make black appear last (darkest)
                if "dark" in color_name:
                    return 100  # Dark colors near the bottom
                
                # Default order if we can't determine
                return 500
            
            # Process color categories
            if "semantic" in tokens and any(tokens["semantic"].values()):
                output.append("/* ========================================================================")
                output.append("   #SEMANTIC COLORS")
                output.append("   ======================================================================== */")
                output.append("")
                for category, colors in tokens["semantic"].items():
                    if colors:
                        output.append(f"/**")
                        output.append(f" * {category.capitalize()} Colors")
                        output.append(f" * Semantic colors that convey specific meanings in the UI.")
                        output.append(f" */")
                        # Sort colors from lightest to darkest
                        for color_name, value in sorted(colors.items(), key=lambda x: sort_by_color_tone(x[0]), reverse=True):
                            # Format the color value correctly
                            scss_value = format_scss_token_value(value, "color", token_sets)
                            output.append(f"${color_name}: {scss_value};")
                output.append("")
            
            if "neutral" in tokens and tokens["neutral"]:
                output.append("/* ========================================================================")
                output.append("   #NEUTRAL COLORS")
                output.append("   ======================================================================== */")
                output.append("")
                output.append("/**")
                output.append(" * Neutral Colors")
                output.append(" * Grayscale and neutral color tokens for backgrounds, text, and borders.")
                output.append(" */")
                # Sort colors from lightest to darkest
                for color_name, value in sorted(tokens["neutral"].items(), key=lambda x: sort_by_color_tone(x[0]), reverse=True):
                    # Format the color value correctly
                    scss_value = format_scss_token_value(value, "color", token_sets)
                    output.append(f"${color_name}: {scss_value};")
                output.append("")
            
            if "palette" in tokens and tokens["palette"]:
                output.append("/* ========================================================================")
                output.append("   #COLOR PALETTE")
                output.append("   ======================================================================== */")
                output.append("")
                output.append("/**")
                output.append(" * Color Palette")
                output.append(" * The complete set of color tokens available in the design system.")
                output.append(" * Colors are ordered from lightest to darkest.")
                output.append(" */")
                
                # Group colors by their base name for better organization
                color_groups = {}
                for color_name, value in tokens["palette"].items():
                    # Remove the shade number for grouping
                    base_name = re.sub(r'-\d+.*$', '', color_name)
                    if base_name not in color_groups:
                        color_groups[base_name] = {}
                    color_groups[base_name][color_name] = value
                
                # Output each color group
                for base_name, colors in sorted(color_groups.items()):
                    group_label = base_name.replace('color-', '')
                    output.append(f"/* {group_label.capitalize()} */")
                    
                    # Sort colors from lightest to darkest
                    for color_name, value in sorted(colors.items(), key=lambda x: sort_by_color_tone(x[0]), reverse=True):
                        scss_value = format_scss_token_value(value, "color", token_sets)
                        output.append(f"${color_name}: {scss_value};")
                output.append("")
            
            if "other" in tokens and tokens["other"]:
                output.append("/* ========================================================================")
                output.append("   #OTHER COLORS")
                output.append("   ======================================================================== */")
                output.append("")
                output.append("/**")
                output.append(" * Miscellaneous Colors")
                output.append(" * Additional color tokens that don't fit into the main categories.")
                output.append(" */")
                # Sort colors from lightest to darkest
                for color_name, value in sorted(tokens["other"].items(), key=lambda x: sort_by_color_tone(x[0]), reverse=True):
                    # Format the color value correctly
                    scss_value = format_scss_token_value(value, "color", token_sets)
                    output.append(f"${color_name}: {scss_value};")
                output.append("")
            
        elif name == "scale":
            # Process scale categories
            for category, values in tokens.items():
                if values:
                    output.append("/* ========================================================================")
                    output.append(f"   #{category.upper()} SCALE")
                    output.append("   ======================================================================== */")
                output.append("")
                    output.append("/**")
                    output.append(f" * {category.capitalize()} Scale Tokens")
                    if category == "spacing":
                        output.append(" * Tokens used for spacing, margins, padding, and layout.")
                    elif category == "sizing":
                        output.append(" * Tokens used for component sizes, widths, and heights.")
                    elif category == "radius":
                        output.append(" * Tokens used for border radius and rounded corners.")
                    else:
                        output.append(f" * {category.capitalize()} related size tokens.")
                    output.append(" */")
                output.append("")
            
                    # Group values by their pattern for better organization
                    pattern_groups = {}
                    for scale_name, value in values.items():
                        # Extract the basic pattern (e.g., scale-spacing-size, scale-sizing)
                        pattern_match = re.match(r'(scale-[a-z]+-[a-z]+)', scale_name)
                        if pattern_match:
                            pattern = pattern_match.group(1)
                        else:
                            pattern = scale_name.split('-')[0:2]
                            pattern = '-'.join(pattern)
                        
                        if pattern not in pattern_groups:
                            pattern_groups[pattern] = {}
                        pattern_groups[pattern][scale_name] = value
                    
                    # Output each pattern group
                    for pattern, scales in sorted(pattern_groups.items()):
                        pattern_label = pattern.replace('scale-', '').replace('-', ' ').title()
                        output.append(f"/* {pattern_label} */")
                        for scale_name, value in sorted(scales.items()):
                            scss_value = format_scss_token_value(value, "dimension", token_sets)
                            output.append(f"${scale_name}: {scss_value};")
                output.append("")
    
    # For brand tokens (keeping this logic for completeness)
    elif is_brand:
        # Process brand tokens (existing brand token logic)
        output.append("/* ========================================================================")
        output.append(f"   #{normalized_name.upper()} BRAND TOKENS")
        output.append("   ======================================================================== */")
        output.append("")
        
        # Make sure we have component groups for this brand
        brand_comp_groups = component_groups.get(normalized_name, {}) if component_groups else {}
        brand_sys_groups = system_groups.get(normalized_name, {}) if system_groups else {}
        
        # Process component tokens
        if brand_comp_groups:
            output.append("/* Component Tokens */")
                output.append("")
            for comp_name, tokens_list in sorted(brand_comp_groups.items()):
                if tokens_list:
                    output.append(f"/**")
                    output.append(f" * {comp_name.capitalize()} Component")
                    output.append(f" * Tokens specific to the {comp_name} component.")
                    output.append(f" */")
                for token_path in tokens_list:
                    if token_path in tokens:
                        token_data = tokens[token_path]
                        value = token_data["value"]
                        token_type = token_data["type"]
                        parts = token_path.split(".")
                            original_name = parts[-1]
                        scss_value = format_scss_token_value(value, token_type, token_sets)
                            output.append(f"${original_name}: {scss_value};")
                    output.append("")
        
        # Process system tokens
        if brand_sys_groups:
            output.append("/* System Tokens */")
                output.append("")
            for system_name, tokens_list in sorted(brand_sys_groups.items()):
                if tokens_list:
                    output.append(f"/**")
                    output.append(f" * System {system_name.capitalize()}")
                    output.append(f" * System-wide {system_name} tokens.")
                    output.append(f" */")
                for token_path in tokens_list:
                    if token_path in tokens:
                        token_data = tokens[token_path]
                        value = token_data["value"]
                        token_type = token_data["type"]
                        parts = token_path.split(".")
                            original_name = parts[-1]
                            scss_value = format_scss_token_value(value, token_type, token_sets)
                            output.append(f"${original_name}: {scss_value};")
                    output.append("")
    
    return "\n".join(output)

def flatten_tokens(tokens):
    """
    Flatten a nested token structure into a flat dictionary.
    Handles the Token Studio format with paths using dots.
    
    Args:
        tokens: The nested token structure
        
    Returns:
        A flat dictionary of tokens with their paths as keys
    """
    print("Flattening tokens...")
    print(f"Input tokens structure: {type(tokens)}")
    
    # Print the top-level keys for debugging
    if isinstance(tokens, dict):
        print(f"Top-level keys: {list(tokens.keys())}")
    
    flat_tokens = {}
    
    def process_token_group(token_group, current_path=""):
        # Check if this is a token (has a value and type)
        if isinstance(token_group, dict) and "value" in token_group and "type" in token_group:
            # This is a token, add it to the flat structure
            token_data = {
                "value": token_group["value"],
                "type": token_group["type"],
                "description": token_group.get("description", "")
            }
            flat_tokens[current_path] = token_data
        elif isinstance(token_group, dict):
            # This is not a token, process its children
            for key, value in token_group.items():
                # Skip metadata keys that start with '$'
                if not key.startswith("$"):
                    new_path = f"{current_path}.{key}" if current_path else key
                    process_token_group(value, new_path)
    
    # Start the recursive processing
    for top_key, top_value in tokens.items():
        process_token_group(top_value, top_key)
    
    print(f"Flattened {len(flat_tokens)} tokens")
    
    # Print a sample of flattened tokens for debugging
    sample_paths = list(flat_tokens.keys())[:3]
    if sample_paths:
        print("Sample token paths:")
        for path in sample_paths:
            print(f"  {path}: {flat_tokens[path]['value']} ({flat_tokens[path]['type']})")
    
    return flat_tokens

def load_tokens(token_file):
    """
    Load tokens from a JSON file.
    
    Args:
        token_file: Path to the token JSON file
        
    Returns:
        Dictionary of tokens or None if file not found or invalid
    """
    try:
        with open(token_file, 'r', encoding='utf-8') as f:
            tokens = json.load(f)
        return tokens
    except FileNotFoundError:
        print(f"Error: Token file not found: {token_file}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in token file: {token_file}")
        return None
    except Exception as e:
        print(f"Error loading token file: {e}")
        return None

def generate_master_scss_file(scss_output_dir):
    """
    Generate a master _tokens.scss file that imports all other token files.
    """
    output = []
    
    # Add documentation header
    output.append("/**")
    output.append(" * Master Tokens File")
    output.append(" * Generated by token-extractor.py")
    output.append(" *")
    output.append(" * This file imports all token files in the correct order.")
    output.append(" */")
        output.append("")
    
    # Add option token imports
    output.append("/* Option Tokens - Base Design Elements */")
    
    # Add color tokens
    if os.path.exists(os.path.join(scss_output_dir, "option-tokens", "_colors.scss")):
        output.append("@import 'option-tokens/colors';")
    
    # Add font tokens
    if os.path.exists(os.path.join(scss_output_dir, "option-tokens", "_fonts.scss")):
        output.append("@import 'option-tokens/fonts';")
    
    # Add scale tokens
    if os.path.exists(os.path.join(scss_output_dir, "option-tokens", "_scales.scss")):
        output.append("@import 'option-tokens/scales';")
    
    output.append("")
    
    # Add semantic token imports
    output.append("/* Semantic Tokens - Brand Colors */")
    
    # Check for BruHealth brand tokens
    if os.path.exists(os.path.join(scss_output_dir, "semantic-tokens", "brands", "_bruhealth.scss")):
        output.append("@import 'semantic-tokens/brands/bruhealth';")
    
    # Check for EVYDCore brand tokens
    if os.path.exists(os.path.join(scss_output_dir, "semantic-tokens", "brands", "_evyd-core.scss")):
        output.append("@import 'semantic-tokens/brands/evyd-core';")
    
    return "\n".join(output)

def format_token_name(name):
    """
    Format a token name to be a valid CSS variable name.
    Converts camelCase or PascalCase to kebab-case, removes invalid characters.
    
    Args:
        name: The original token name
        
    Returns:
        A CSS-valid variable name in kebab-case format
    """
    # Convert camelCase or PascalCase to kebab-case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    kebab_case = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
    
    # Remove any invalid characters
    valid_name = re.sub(r'[^a-z0-9-]', '-', kebab_case)
    
    # Remove duplicate hyphens
    valid_name = re.sub(r'-+', '-', valid_name)
    
    # Remove leading and trailing hyphens
    valid_name = valid_name.strip('-')
    
    return valid_name

def generate_brand_scss(brand_colors, brand_name, description):
    """
    Generate SCSS variables for brand colors as semantic tokens.
    
    Args:
        brand_colors: Dictionary of brand color tokens
        brand_name: Name of the brand (bruhealth, evydcore)
        description: Description for the file header
    
    Returns:
        String content of the SCSS module
    """
    output = []
    
    # Add documentation header
    output.append("/* ========================================================================")
    output.append(f"   #{brand_name.upper()} BRAND COLORS")
    output.append("   ======================================================================== */")
    output.append("")
    output.append("/**")
    output.append(f" * {description}")
    output.append(" * Generated by token-extractor.py")
    output.append(" */")
    output.append("")
    
    # Group brand colors by their semantic meaning
    color_groups = {}
    
    # First pass - categorize colors
    for color_name, value in brand_colors.items():
        # Find semantic group (primary, secondary, danger, success, etc.)
        semantic_match = None
        for semantic in ['primary', 'secondary', 'danger', 'success', 'warning', 'info', 'neutral', 'brand']:
            if semantic in color_name.lower():
                semantic_match = semantic
                break
        
        # If no semantic match found, look for state
        if not semantic_match:
            # Default to "other"
            semantic_match = "other"
        
        # Find state (rest, hover, press, focus, disabled, etc.)
        state_match = None
        for state in ['rest', 'hover', 'press', 'focus', 'disabled', 'active']:
            if state in color_name.lower():
                state_match = state
                break
        
        # Group by semantic meaning first, then by state
        if semantic_match not in color_groups:
            color_groups[semantic_match] = {}
        
        # Add to the appropriate group
        color_groups[semantic_match][color_name] = {
            'value': value,
            'state': state_match
        }
    
    # Order semantic groups for output
    semantic_order = ['brand', 'primary', 'secondary', 'danger', 'success', 'warning', 'info', 'neutral', 'other']
    
    # Second pass - output colors in organized groups
    for semantic in semantic_order:
        if semantic in color_groups and color_groups[semantic]:
            output.append(f"/* {semantic.capitalize()} Colors */")
            
            # Sort by state (rest, hover, press, disabled)
            state_order = {'rest': 1, 'hover': 2, 'press': 3, 'focus': 4, 'disabled': 5, 'active': 6, None: 99}
            
            sorted_colors = sorted(
                color_groups[semantic].items(),
                key=lambda x: state_order.get(x[1]['state'], 99)
            )
            
            for color_name, data in sorted_colors:
                # Format the reference value properly for SCSS
                color_value = data['value']
                if isinstance(color_value, str) and color_value.startswith("{") and color_value.endswith("}"):
                    # Convert to proper SCSS variable reference
                    ref_path = color_value[1:-1]
                    scss_ref = f"${ref_path.replace('.', '-')}"
                    output.append(f"${color_name}: {scss_ref};")
                else:
                    output.append(f"${color_name}: {color_value};")
            
            output.append("")
    
    return "\n".join(output)

def main():
    """
    Main function to extract tokens and generate SCSS modules.
    """
    parser = argparse.ArgumentParser(description='Extract tokens from Token Studio and generate SCSS/JS files.')
    parser.add_argument('--token-file', required=True, help='Path to the token studio JSON file')
    parser.add_argument('--scss-output', default='src/styles/tokens', help='Output directory for SCSS files')
    parser.add_argument('--js-output', default='src/tokens', help='Output directory for JS files')
    parser.add_argument('--generate-scss', action='store_true', help='Generate SCSS output')
    parser.add_argument('--generate-js', action='store_true', help='Generate JS output')
    parser.add_argument('--force', action='store_true', help='Force regeneration even if token file is unchanged')
    parser.add_argument('--verbose', action='store_true', help='Print verbose output')
    args = parser.parse_args()
    
    # Set verbose mode
    verbose = args.verbose
    
    # Check if the necessary directories exist
    ensure_directory_exists(os.path.dirname(args.token_file))
    ensure_directory_exists(args.scss_output)
    ensure_directory_exists(args.js_output)
    
    # Check if token-studio file exists
    if not os.path.isfile(args.token_file):
        print(f"Token Studio file not found: {args.token_file}")
        return
    
    print(f"Extracting tokens from {args.token_file}...")
    
    # Load tokens from Token Studio
    try:
        with open(args.token_file, 'r', encoding='utf-8') as f:
            tokens = json.load(f)
            print(f"Loaded token file with {len(tokens)} top-level entries")
    except Exception as e:
        print(f"Error loading token file: {str(e)}")
        return
    
    # Flatten tokens
    try:
        flattened_tokens = flatten_tokens(tokens)
        print(f"Flattened {len(flattened_tokens)} tokens from {args.token_file}")
        
        # Sample token paths for debugging
        if verbose:
            sample_paths = list(flattened_tokens.keys())[:5]
            if sample_paths:
                print("\nSample token paths:")
                for path in sample_paths:
                    print(f"  {path}: {flattened_tokens[path]['value']} ({flattened_tokens[path]['type']})")
    except Exception as e:
        print(f"Error flattening tokens: {str(e)}")
        traceback.print_exc()
        return
    
    # Ensure output directories exist
    ensure_directory_exists(os.path.join(args.scss_output, "option-tokens"))
    ensure_directory_exists(os.path.join(args.scss_output, "semantic-tokens"))
    ensure_directory_exists(os.path.join(args.scss_output, "semantic-tokens", "brands"))
    
    # Process tokens
    try:
        # Extract and categorize tokens
        print("Processing tokens...")
        result = process_tokens(flattened_tokens)
        
        # Generate SCSS files if requested
        if args.generate_scss:
            print("Generating SCSS files...")
            
            # For token reference resolution, we need to pass the raw flattened tokens
            # This is a simpler approach than trying to reconstruct the organized structure
            
            # Generate base color token SCSS
            if result["colors"]:
                print("Generating base color token SCSS...")
                scss_dir = os.path.join(args.scss_output, "option-tokens")
                ensure_directory_exists(scss_dir)
                
                base_tokens = {
                    "palette": result["colors"]["palette"],
                    "neutral": result["colors"]["neutral"],
                    "other": result["colors"]["other"]
                }
                scss_content = generate_scss_module(base_tokens, "colors", "Base color tokens", token_sets=flattened_tokens)
                
                scss_file = os.path.join(scss_dir, "_colors.scss")
                write_to_file(scss_content, "", scss_file)
                print(f"Created SCSS file: {scss_file} with base color tokens")
            
            # Generate font token SCSS
            if result["font"]:
                print("Generating font token SCSS...")
                scss_dir = os.path.join(args.scss_output, "option-tokens")
                ensure_directory_exists(scss_dir)
                
                scss_content = generate_font_scss(result["font"], "Font tokens for the design system", flattened_tokens)
                
                scss_file = os.path.join(scss_dir, "_fonts.scss")
                write_to_file(scss_content, "", scss_file)
                print(f"Created SCSS file: {scss_file} with font tokens")
            
            # Generate scale token SCSS
            if result["scale"]:
                print("Generating scale token SCSS...")
                scss_dir = os.path.join(args.scss_output, "option-tokens")
                ensure_directory_exists(scss_dir)
                
                scss_content = generate_scale_scss(result["scale"], "Scale tokens for the design system", flattened_tokens)
                
                scss_file = os.path.join(scss_dir, "_scales.scss")
                write_to_file(scss_content, "", scss_file)
                print(f"Created SCSS file: {scss_file} with scale tokens")
            
            # Generate semantic tokens for brand colors
            if "brandColors" in result:
                # Generate BruHealth brand tokens
                if "bruhealth" in result["brandColors"] and result["brandColors"]["bruhealth"]:
                    print("Generating BruHealth brand token SCSS...")
                    bruhealth_content = generate_brand_scss(
                        result["brandColors"]["bruhealth"],
                        "bruhealth",
                        "BruHealth brand color tokens"
                    )
                    bruhealth_file = os.path.join(args.scss_output, "semantic-tokens", "brands", "_bruhealth.scss")
                    write_to_file(bruhealth_content, "", bruhealth_file)
                    print(f"Created SCSS file: {bruhealth_file} with {len(result['brandColors']['bruhealth'])} tokens")
                
                # Generate EVYDCore brand tokens
                if "evydcore" in result["brandColors"] and result["brandColors"]["evydcore"]:
                    print("Generating EVYDCore brand token SCSS...")
                    evydcore_content = generate_brand_scss(
                        result["brandColors"]["evydcore"],
                        "evydcore",
                        "EVYDCore brand color tokens"
                    )
                    evydcore_file = os.path.join(args.scss_output, "semantic-tokens", "brands", "_evyd-core.scss")
                    write_to_file(evydcore_content, "", evydcore_file)
                    print(f"Created SCSS file: {evydcore_file} with {len(result['brandColors']['evydcore'])} tokens")
            
            # Generate master SCSS file that imports all token files
            master_scss_content = generate_master_scss_file(args.scss_output)
            master_scss_file = os.path.join(args.scss_output, "_tokens.scss")
            write_to_file(master_scss_content, "", master_scss_file)
            print(f"Created master SCSS file: {master_scss_file}")
        
        print("Token extraction completed successfully!")
    
    except Exception as e:
        print(f"Error processing tokens: {str(e)}")
        traceback.print_exc()
        return

if __name__ == "__main__":
    main() 