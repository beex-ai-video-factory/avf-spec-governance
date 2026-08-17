"""
Zero-dependency YAML fallback for AVF Runbook validators when pyyaml is not installed.
"""

def safe_load(stream):
    if hasattr(stream, "read"):
        text = stream.read()
    else:
        text = str(stream)
        
    lines = text.splitlines()
    data = {}
    current_prompt = None
    prompts = []
    current_list_key = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
            
        if line.startswith("version:"):
            data["version"] = line.split(":", 1)[1].strip()
        elif line.startswith("project:"):
            data["project"] = line.split(":", 1)[1].strip()
        elif line.startswith("total_prompts:"):
            data["total_prompts"] = int(line.split(":", 1)[1].strip())
        elif line.startswith("prompts:"):
            data["prompts"] = prompts
        elif line.startswith("- id:") or line.startswith("  - id:"):
            current_prompt = {}
            prompts.append(current_prompt)
            current_prompt["id"] = line.split(":", 1)[1].strip()
            current_list_key = None
        elif current_prompt is not None:
            if line.startswith("    - ") or line.startswith("  - "):
                item_val = stripped[2:].strip()
                if current_list_key and current_list_key in current_prompt:
                    current_prompt[current_list_key].append(item_val)
            elif ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                if val == "[]":
                    current_prompt[key] = []
                    current_list_key = None
                elif val == "":
                    if i + 1 < len(lines) and (lines[i+1].startswith("    - ") or lines[i+1].startswith("  - ")):
                        current_prompt[key] = []
                        current_list_key = key
                    else:
                        current_list_key = None
                        multiline_parts = []
                        i += 1
                        while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("      ")):
                            multiline_parts.append(lines[i].strip())
                            i += 1
                        current_prompt[key] = " ".join(multiline_parts)
                        continue
                else:
                    current_prompt[key] = val
                    current_list_key = None
        i += 1
        
    return data
