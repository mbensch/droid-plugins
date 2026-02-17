#!/usr/bin/env python3
"""
Droid Receipts - Generate visual receipts for Droid sessions.

Triggered by SessionEnd hook. Reads session data from:
- Hook stdin (session_id, transcript_path, cwd)
- Session settings JSON (token counts, model)
- Transcript JSONL (session title, timestamps)

Generates an SVG receipt saved to ~/.factory/receipts/
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Pricing: $1 per 1 million tokens
PRICE_PER_MILLION = 1.0

# Output directory for receipts
RECEIPTS_DIR = Path.home() / ".factory" / "receipts"


def format_currency(tokens: int) -> str:
    """Calculate cost at $1/M tokens."""
    cost = tokens / 1_000_000 * PRICE_PER_MILLION
    return f"${cost:.2f}"


def format_number(n: int) -> str:
    """Format number with thousand separators."""
    return f"{n:,}"


def format_duration(ms: int) -> str:
    """Format duration from milliseconds."""
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    
    if hours > 0:
        return f"{hours}h {minutes % 60}m {seconds % 60}s"
    elif minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    else:
        return f"{seconds}s"


def get_model_name(model: str) -> str:
    """Clean up model name for display."""
    model_map = {
        "claude-opus-4-6": "Claude Opus 4.6",
        "claude-opus-4-6-fast": "Claude Opus 4.6 Fast",
        "claude-opus-4-5-20251101": "Claude Opus 4.5",
        "claude-sonnet-4-5-20250929": "Claude Sonnet 4.5",
        "claude-haiku-4-5-20251001": "Claude Haiku 4.5",
        "gpt-5.1-codex-max": "GPT-5.1 Codex Max",
        "gpt-5.1-codex": "GPT-5.1 Codex",
        "gpt-5.1": "GPT-5.1",
        "gpt-5.2": "GPT-5.2",
        "gpt-5.2-codex": "GPT-5.2 Codex",
        "gpt-5.3-codex": "GPT-5.3 Codex",
        "gemini-3-pro-preview": "Gemini 3 Pro",
        "gemini-3-flash-preview": "Gemini 3 Flash",
        "glm-4.7": "Droid Core (GLM-4.7)",
        "glm-5": "Droid Core (GLM-5)",
        "kimi-k2.5": "Droid Core (Kimi K2.5)",
        "minimax-m2.5": "MiniMax M2.5",
    }
    return model_map.get(model, model)


def generate_droid_name(session_id: str) -> str:
    """Generate a Star Wars-style droid name from session ID."""
    # Extract hex-like characters from session ID
    hex_chars = "".join(c for c in session_id.upper() if c in "0123456789ABCDEF")
    
    # Pad if needed
    if len(hex_chars) < 8:
        hex_chars = hex_chars.ljust(8, "0")
    
    # Star Wars droid prefixes
    prefixes = ["R2", "C3", "BB", "K2", "IG", "BD", "QT", "AP", "RX", "TC", "GNK", "WED"]
    
    # Use first hex digit to pick prefix
    prefix_idx = int(hex_chars[0], 16) % len(prefixes)
    prefix = prefixes[prefix_idx]
    
    # Generate model number from remaining hex
    model_num = hex_chars[1:4]
    
    return f"{prefix}-{model_num}"


def escape_xml(text: str) -> str:
    """Escape XML special characters."""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;"))


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#039;"))


def generate_html(session_data: dict) -> str:
    """Generate HTML receipt from session data."""
    
    # Extract data
    session_id = session_data["session_id"]
    session_short = session_id[:8] if len(session_id) >= 8 else session_id
    location = session_data.get("location", "The Cloud")[:30]
    model = session_data["model"]
    model_name = get_model_name(model)
    droid_name = generate_droid_name(session_id)
    tokens = session_data["tokens"]
    end_time = session_data.get("end_time", datetime.now().isoformat())
    active_time = session_data.get("active_time_ms", 0)
    
    # Calculate totals
    input_tokens = tokens.get("inputTokens", 0)
    output_tokens = tokens.get("outputTokens", 0)
    cache_write = tokens.get("cacheCreationTokens", 0)
    cache_read = tokens.get("cacheReadTokens", 0)
    total_tokens = input_tokens + output_tokens + cache_write + cache_read
    
    # Format date
    try:
        dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        date_str = end_time
    
    duration_str = format_duration(active_time)
    
    # Escape text
    location = escape_html(location)
    model_name = escape_html(model_name)
    droid_name = escape_html(droid_name)
    session_short = escape_html(session_short)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Droid Receipt - {session_short}</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    
    body {{
      font-family: 'Courier New', Courier, monospace;
      font-size: 14px;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    
    .receipt {{
      background: #fafafa;
      width: 400px;
      padding: 30px 25px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
      border-radius: 4px;
      animation: slideIn 0.5s ease-out;
    }}
    
    @keyframes slideIn {{
      from {{ opacity: 0; transform: translateY(-20px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .header {{
      text-align: center;
      padding-bottom: 20px;
      border-bottom: 2px solid #333;
    }}
    
    .logo {{
      font-family: Arial, sans-serif;
      font-size: 28px;
      font-weight: bold;
      letter-spacing: 4px;
      color: #333;
      margin-bottom: 5px;
    }}
    
    .subtitle {{
      font-size: 11px;
      color: #666;
      letter-spacing: 2px;
    }}
    
    .model-badge {{
      background: #333;
      color: #fff;
      padding: 8px 16px;
      border-radius: 20px;
      display: inline-block;
      margin: 20px 0;
      font-size: 12px;
      font-weight: bold;
    }}
    
    .meta {{
      margin: 15px 0;
    }}
    
    .meta-row {{
      display: flex;
      justify-content: space-between;
      padding: 5px 0;
      border-bottom: 1px dashed #ccc;
    }}
    
    .meta-row:last-child {{
      border-bottom: none;
    }}
    
    .meta-label {{
      color: #666;
    }}
    
    .meta-value {{
      color: #333;
      font-weight: 500;
    }}
    
    .separator {{
      border-bottom: 2px solid #333;
      margin: 15px 0;
    }}
    
    .items-header {{
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      font-weight: bold;
      border-bottom: 1px dashed #ccc;
    }}
    
    .item {{
      margin: 8px 0;
    }}
    
    .item-row {{
      display: flex;
      justify-content: space-between;
      padding: 3px 0;
      color: #555;
    }}
    
    .item-row .qty {{
      text-align: center;
      flex: 1;
    }}
    
    .item-row .price {{
      text-align: right;
      min-width: 80px;
    }}
    
    .item-label {{
      min-width: 120px;
    }}
    
    .total-section {{
      border-top: 2px solid #333;
      margin-top: 15px;
      padding-top: 15px;
    }}
    
    .total-row {{
      display: flex;
      justify-content: space-between;
      font-size: 18px;
      font-weight: bold;
      padding: 5px 0;
    }}
    
    .footer {{
      text-align: center;
      margin-top: 25px;
      padding-top: 20px;
      border-top: 2px dashed #ccc;
    }}
    
    .cashier {{
      color: #333;
      margin-bottom: 15px;
    }}
    
    .thank-you {{
      font-size: 13px;
      color: #333;
      margin-bottom: 15px;
    }}
    
    .github-link {{
      font-size: 11px;
      color: #999;
    }}
    
    .github-link a {{
      color: #666;
      text-decoration: none;
    }}
    
    .github-link a:hover {{
      color: #333;
    }}
    
    @media print {{
      body {{
        background: white;
      }}
      .receipt {{
        box-shadow: none;
      }}
    }}
  </style>
</head>
<body>
  <div class="receipt">
    <div class="header">
      <div class="logo">FACTORY</div>
      <div class="subtitle">DROID RECEIPT</div>
    </div>
    
    <div style="text-align: center;">
      <span class="model-badge">{model_name}</span>
    </div>
    
    <div class="meta">
      <div class="meta-row">
        <span class="meta-label">Location</span>
        <span class="meta-value">{location}</span>
      </div>
      <div class="meta-row">
        <span class="meta-label">Session</span>
        <span class="meta-value">{session_short}</span>
      </div>
      <div class="meta-row">
        <span class="meta-label">Date</span>
        <span class="meta-value">{date_str}</span>
      </div>
      <div class="meta-row">
        <span class="meta-label">Duration</span>
        <span class="meta-value">{duration_str}</span>
      </div>
    </div>
    
    <div class="separator"></div>
    
    <div class="items-header">
      <span>ITEM</span>
      <span>QTY</span>
      <span>PRICE</span>
    </div>
    
    <div class="item">
      <div class="item-row">
        <span class="item-label">Input tokens</span>
        <span class="qty">{format_number(input_tokens)}</span>
        <span class="price">{format_currency(input_tokens)}</span>
      </div>
      <div class="item-row">
        <span class="item-label">Output tokens</span>
        <span class="qty">{format_number(output_tokens)}</span>
        <span class="price">{format_currency(output_tokens)}</span>
      </div>'''
    
    if cache_write > 0:
        html += f'''
      <div class="item-row">
        <span class="item-label">Cache write</span>
        <span class="qty">{format_number(cache_write)}</span>
        <span class="price">{format_currency(cache_write)}</span>
      </div>'''
    
    if cache_read > 0:
        html += f'''
      <div class="item-row">
        <span class="item-label">Cache read</span>
        <span class="qty">{format_number(cache_read)}</span>
        <span class="price">{format_currency(cache_read)}</span>
      </div>'''
    
    html += f'''
    </div>
    
    <div class="total-section">
      <div class="total-row">
        <span>TOTAL</span>
        <span>{format_currency(total_tokens)}</span>
      </div>
    </div>
    
    <div class="footer">
      <div class="cashier">SERVED BY: {droid_name}</div>
      <div class="thank-you">Thank you for building!</div>
      <div class="github-link">
        <a href="https://github.com/Factory-AI/factory" target="_blank">github.com/Factory-AI/factory</a>
      </div>
    </div>
  </div>
  
  <script>
    console.log('Droid Receipt Generated!');
    console.log('Session: {session_short}');
    console.log('Total: {format_currency(total_tokens)}');
  </script>
</body>
</html>'''
    
    return html


def generate_svg(session_data: dict) -> str:
    """Generate SVG receipt from session data."""
    
    # Extract data
    session_id = session_data["session_id"]
    # Use short session ID (first 8 chars)
    session_short = session_id[:8] if len(session_id) >= 8 else session_id
    location = session_data.get("location", "The Cloud")[:30]
    model = session_data["model"]
    model_name = get_model_name(model)
    droid_name = generate_droid_name(session_id)
    tokens = session_data["tokens"]
    end_time = session_data.get("end_time", datetime.now().isoformat())
    active_time = session_data.get("active_time_ms", 0)
    
    # Calculate totals - sum ALL tokens for total cost
    input_tokens = tokens.get("inputTokens", 0)
    output_tokens = tokens.get("outputTokens", 0)
    cache_write = tokens.get("cacheCreationTokens", 0)
    cache_read = tokens.get("cacheReadTokens", 0)
    total_tokens = input_tokens + output_tokens + cache_write + cache_read
    
    input_cost = format_currency(input_tokens)
    output_cost = format_currency(output_tokens)
    cache_write_cost = format_currency(cache_write)
    cache_read_cost = format_currency(cache_read)
    total_cost = format_currency(total_tokens)
    
    # Format date
    try:
        dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        date_str = end_time
    
    # Format duration
    duration_str = format_duration(active_time)
    
    # Escape text for XML
    location = escape_xml(location)
    model_name = escape_xml(model_name)
    droid_name = escape_xml(droid_name)
    session_short = escape_xml(session_short)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="580" viewBox="0 0 400 580" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .receipt-bg {{ fill: #f8f8f8; }}
      .text {{ font-family: 'Courier New', Courier, monospace; font-size: 12px; fill: #333; }}
      .text-bold {{ font-family: 'Courier New', Courier, monospace; font-size: 12px; fill: #333; font-weight: bold; }}
      .text-large {{ font-family: 'Courier New', Courier, monospace; font-size: 16px; fill: #333; font-weight: bold; }}
      .text-small {{ font-family: 'Courier New', Courier, monospace; font-size: 10px; fill: #666; }}
      .text-tiny {{ font-family: 'Courier New', Courier, monospace; font-size: 9px; fill: #999; }}
      .separator {{ stroke: #333; stroke-width: 2; }}
      .light-separator {{ stroke: #ccc; stroke-width: 1; stroke-dasharray: 2,2; }}
      .logo-text {{ font-family: Arial, sans-serif; font-size: 24px; fill: #333; font-weight: bold; }}
      .model-tag {{ fill: #e8e8e8; }}
    </style>
  </defs>
  
  <!-- Receipt background -->
  <rect class="receipt-bg" x="10" y="10" width="380" height="560" rx="4"/>
  
  <!-- Header -->
  <text x="200" y="55" class="logo-text" text-anchor="middle">FACTORY</text>
  <text x="200" y="78" class="text-small" text-anchor="middle">DROID RECEIPT</text>
  
  <!-- Separator -->
  <line x1="30" y1="95" x2="370" y2="95" class="separator"/>
  
  <!-- Model badge -->
  <rect class="model-tag" x="100" y="105" width="200" height="22" rx="3"/>
  <text x="200" y="121" class="text-bold" text-anchor="middle" font-size="11">{model_name}</text>
  
  <!-- Session info -->
  <text x="30" y="150" class="text">Location</text>
  <text x="370" y="150" class="text" text-anchor="end">{location}</text>
  <line x1="105" y1="146" x2="285" y2="146" class="light-separator"/>
  
  <text x="30" y="170" class="text">Session</text>
  <text x="370" y="170" class="text" text-anchor="end">{session_short}</text>
  <line x1="105" y1="166" x2="285" y2="166" class="light-separator"/>
  
  <text x="30" y="190" class="text">Date</text>
  <text x="370" y="190" class="text" text-anchor="end">{date_str}</text>
  <line x1="105" y1="186" x2="285" y2="186" class="light-separator"/>
  
  <text x="30" y="210" class="text">Duration</text>
  <text x="370" y="210" class="text" text-anchor="end">{duration_str}</text>
  <line x1="105" y1="206" x2="285" y2="206" class="light-separator"/>
  
  <!-- Separator -->
  <line x1="30" y1="230" x2="370" y2="230" class="separator"/>
  
  <!-- Header -->
  <text x="30" y="255" class="text-bold">ITEM</text>
  <text x="200" y="255" class="text-bold" text-anchor="middle">QTY</text>
  <text x="370" y="255" class="text-bold" text-anchor="end">PRICE</text>
  
  <line x1="30" y1="265" x2="370" y2="265" class="light-separator"/>
  
  <!-- Line items -->
  <text x="45" y="290" class="text">Input tokens</text>
  <text x="200" y="290" class="text" text-anchor="middle">{format_number(input_tokens)}</text>
  <text x="370" y="290" class="text" text-anchor="end">{input_cost}</text>
  
  <text x="45" y="310" class="text">Output tokens</text>
  <text x="200" y="310" class="text" text-anchor="middle">{format_number(output_tokens)}</text>
  <text x="370" y="310" class="text" text-anchor="end">{output_cost}</text>'''
    
    # Add cache tokens if present
    y_offset = 330
    if cache_write > 0:
        svg += f'''
  <text x="45" y="{y_offset}" class="text">Cache write</text>
  <text x="200" y="{y_offset}" class="text" text-anchor="middle">{format_number(cache_write)}</text>
  <text x="370" y="{y_offset}" class="text" text-anchor="end">{cache_write_cost}</text>'''
        y_offset += 20
    
    if cache_read > 0:
        svg += f'''
  <text x="45" y="{y_offset}" class="text">Cache read</text>
  <text x="200" y="{y_offset}" class="text" text-anchor="middle">{format_number(cache_read)}</text>
  <text x="370" y="{y_offset}" class="text" text-anchor="end">{cache_read_cost}</text>'''
        y_offset += 20
    
    # Total section
    total_y = y_offset + 15
    
    svg += f'''
  
  <!-- Total section -->
  <line x1="30" y1="{total_y}" x2="370" y2="{total_y}" class="separator"/>
  
  <text x="30" y="{total_y + 25}" class="text-bold" font-size="14">TOTAL</text>
  <text x="370" y="{total_y + 25}" class="text-bold" font-size="14" text-anchor="end">{total_cost}</text>
  
  <line x1="30" y1="{total_y + 40}" x2="370" y2="{total_y + 40}" class="separator"/>
  
  <!-- Footer -->
  <text x="200" y="{total_y + 70}" class="text" text-anchor="middle">SERVED BY: {droid_name}</text>
  
  <text x="200" y="{total_y + 100}" class="text" text-anchor="middle">Thank you for building!</text>
  
  <line x1="100" y1="{total_y + 120}" x2="300" y2="{total_y + 120}" class="light-separator"/>
  
  <text x="200" y="{total_y + 140}" class="text-small" text-anchor="middle">github.com/Factory-AI/factory</text>
</svg>'''
    
    return svg


def main():
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)
        
        session_id = hook_input.get("session_id", "")
        transcript_path = hook_input.get("transcript_path", "").replace("~", os.environ.get("HOME", "~"))
        cwd = hook_input.get("cwd", "")
        
        # Extract location from cwd
        location = Path(cwd).name if cwd else "The Cloud"
        
        # Read session settings
        settings_path = transcript_path.replace(".jsonl", ".settings.json")
        
        if not os.path.exists(settings_path):
            print(f"No session settings found at {settings_path}", file=sys.stderr)
            sys.exit(0)  # Non-blocking exit
        
        with open(settings_path, "r") as f:
            settings = json.load(f)
        
        tokens = settings.get("tokenUsage", {})
        model = settings.get("model", "unknown")
        active_time_ms = settings.get("assistantActiveTimeMs", 0)
        
        # Skip if no token data
        if not tokens:
            print("No token usage data available", file=sys.stderr)
            sys.exit(0)
        
        # Parse transcript for end time
        end_time = datetime.now().isoformat()
        
        if os.path.exists(transcript_path):
            with open(transcript_path, "r") as f:
                # Get last timestamp
                for line in reversed(list(f)):
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            if "timestamp" in entry:
                                end_time = entry["timestamp"]
                                break
                        except:
                            pass
        
        # Build session data
        session_data = {
            "session_id": session_id,
            "location": location,
            "model": model,
            "tokens": tokens,
            "end_time": end_time,
            "active_time_ms": active_time_ms,
        }
        
        # Create output directory
        RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Determine output format from env or default to both
        output_format = os.environ.get("DROID_RECEIPT_FORMAT", "html").lower()
        
        # Generate and save receipts
        opened_path = None
        
        if output_format in ("html", "both"):
            html_content = generate_html(session_data)
            html_path = RECEIPTS_DIR / f"{session_id}.html"
            with open(html_path, "w") as f:
                f.write(html_content)
            print(f"HTML receipt saved to {html_path}")
            opened_path = html_path
        
        if output_format in ("svg", "both"):
            svg_content = generate_svg(session_data)
            svg_path = RECEIPTS_DIR / f"{session_id}.svg"
            with open(svg_path, "w") as f:
                f.write(svg_content)
            print(f"SVG receipt saved to {svg_path}")
            if not opened_path:
                opened_path = svg_path
        
        # Open in browser (macOS)
        if opened_path and sys.platform == "darwin":
            os.system(f'open "{opened_path}"')
        
    except Exception as e:
        print(f"Error generating receipt: {e}", file=sys.stderr)
        sys.exit(0)  # Non-blocking exit


if __name__ == "__main__":
    main()
