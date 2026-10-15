#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Clash Ruleset Builder for AI Providers
Generates standalone and consolidated ruleset files for Clash / Clash Meta (Mihomo).
Focuses strictly on precise Domain and IP/ASN assets (no process-level rules).
"""

from collections import OrderedDict
from datetime import datetime
import os
import shutil

REPO_URL = "https://github.com/zfdang/clash-ruleset-ai-providers"
AUTHOR = "zfdang"

# Define rules for each provider
RULES_DATA = {
    "OpenAI": {
        "filename": "openai.yaml",
        "description": "Rules for OpenAI (ChatGPT, API, Codex, Voice / LiveKit, CDN, ArkoseLabs)",
        "rules": [
            # Core domains & Web
            "DOMAIN-SUFFIX,openai.com",
            "DOMAIN-SUFFIX,chatgpt.com",
            "DOMAIN-SUFFIX,oaistatic.com",
            "DOMAIN-SUFFIX,oaiusercontent.com",
            "DOMAIN-SUFFIX,ai.com",
            # Voice / Realtime streaming (LiveKit Cloud)
            "DOMAIN-SUFFIX,chatgpt.livekit.cloud",
            "DOMAIN-SUFFIX,host.livekit.cloud",
            "DOMAIN-SUFFIX,turn.livekit.cloud",
            # OpenAI Specific CDN & Dedicated Endpoints
            "DOMAIN,chat.openai.com.cdn.cloudflare.net",
            "DOMAIN,openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net",
            "DOMAIN,openaicomproductionae4b.blob.core.windows.net",
            "DOMAIN,production-openaicom-storage.azureedge.net",
            "DOMAIN,openaiapi-site.azureedge.net",
            "DOMAIN,openaicom.imgix.net",
            "DOMAIN,static.cloudflareinsights.com",
            "DOMAIN,browser-intake-datadoghq.com",
            # Human Verification (Specific Arkose endpoints for OpenAI, avoid broad arkoselabs.com)
            "DOMAIN,openai-api.arkoselabs.com",
            "DOMAIN,client-api.arkoselabs.com",
            # Keywords
            "DOMAIN-KEYWORD,openai",
            "DOMAIN-KEYWORD,chatgpt",
            # Dedicated IP / ASN
            "IP-CIDR,24.199.123.28/32,no-resolve",
            "IP-CIDR,64.23.132.171/32,no-resolve",
            "IP-ASN,20473,no-resolve",
        ],
    },
    "Anthropic": {
        "filename": "anthropic.yaml",
        "description": "Rules for Anthropic & Claude (Web, API, CDN)",
        "rules": [
            # Core domains & Web
            "DOMAIN-SUFFIX,anthropic.com",
            "DOMAIN-SUFFIX,claude.ai",
            "DOMAIN-SUFFIX,claude.com",
            "DOMAIN-SUFFIX,claudeusercontent.com",
            # CDN & Endpoints
            "DOMAIN,servd-anthropic-website.b-cdn.net",
            "DOMAIN,anthropic.imgix.net",
            # Keywords
            "DOMAIN-KEYWORD,anthropic",
            "DOMAIN-KEYWORD,claude",
        ],
    },
    "Antigravity": {
        "filename": "antigravity.yaml",
        "description": "Rules for Google Antigravity & Gemini / Google AI Services",
        "rules": [
            # Antigravity Core Cloud Code Backend
            "DOMAIN,daily-cloudcode-pa.googleapis.com",
            "DOMAIN,cloudcode-pa.googleapis.com",
            "DOMAIN,autopush-cloudcode-pa.sandbox.googleapis.com",
            "DOMAIN,preprod-daily-cloudcode-pa.sandbox.googleapis.com",
            # Antigravity & AI Code Assist Endpoints
            "DOMAIN,antigravity.google.com",
            "DOMAIN,aicode.googleapis.com",
            "DOMAIN,alkalimakersuiteapplets.pa.googleapis.com",
            "DOMAIN,alkalimakersuite-pa.clients6.google.com",
            "DOMAIN,proactivebackend-pa.googleapis.com",
            # Gemini API & Generative Language
            "DOMAIN,generativelanguage.googleapis.com",
            "DOMAIN-SUFFIX,generativeai.google",
            "DOMAIN-KEYWORD,generativelanguage",
            # Google AI Studio & MakerSuite
            "DOMAIN,aistudio.google.com",
            "DOMAIN,makersuite.google.com",
            "DOMAIN,ai.google.dev",
            # Gemini Web Platforms
            "DOMAIN-SUFFIX,gemini.google.com",
            "DOMAIN-SUFFIX,bard.google.com",
            # Google DeepMind
            "DOMAIN-SUFFIX,deepmind.google",
            "DOMAIN-SUFFIX,deepmind.com",
            # Google Cloud AI Platform
            "DOMAIN,aiplatform.googleapis.com",
            # Authentication (OAuth token exchange for Antigravity agent mode)
            "DOMAIN,oauth2.googleapis.com",
        ],
    },
}


def parse_and_sort_rules(rules):
    """
    Sort rules by type priority:
    DOMAIN -> DOMAIN-SUFFIX -> DOMAIN-KEYWORD -> IP-CIDR -> IP-CIDR6 -> IP-ASN -> Others
    """
    type_priority = {
        "DOMAIN": 1,
        "DOMAIN-SUFFIX": 2,
        "DOMAIN-KEYWORD": 3,
        "IP-CIDR": 4,
        "IP-CIDR6": 5,
        "IP-ASN": 6,
    }

    # Deduplicate while preserving relative order
    seen = set()
    unique_rules = []
    for r in rules:
        r_clean = r.strip()
        if r_clean and r_clean not in seen:
            seen.add(r_clean)
            unique_rules.append(r_clean)

    def sort_key(rule):
        parts = rule.split(",", 1)
        rtype = parts[0].strip()
        val = parts[1].strip() if len(parts) > 1 else ""
        return (type_priority.get(rtype, 99), val.lower())

    return sorted(unique_rules, key=sort_key)


def count_stats(rules):
    stats = OrderedDict()
    for r in rules:
        rtype = r.split(",", 1)[0].strip()
        stats[rtype] = stats.get(rtype, 0) + 1
    return stats


def generate_yaml_content(name, description, rules, updated_time):
    sorted_rules = parse_and_sort_rules(rules)
    stats = count_stats(sorted_rules)

    lines = [
        f"# NAME: {name}",
        f"# AUTHOR: {AUTHOR}",
        f"# REPO: {REPO_URL}",
        f"# UPDATED: {updated_time}",
        f"# DESCRIPTION: {description}",
    ]
    for k, v in stats.items():
        lines.append(f"# {k}: {v}")
    lines.append(f"# TOTAL: {len(sorted_rules)}")
    lines.append("payload:")
    for r in sorted_rules:
        lines.append(f"  - {r}")
    lines.append("")
    return "\n".join(lines)


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rules_dir = os.path.join(root_dir, "rules")
    os.makedirs(rules_dir, exist_ok=True)

    updated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    all_rules = []
    generated_files = []

    # 1. Generate standalone files
    for name, data in RULES_DATA.items():
        rules = data["rules"]
        all_rules.extend(rules)
        content = generate_yaml_content(name, data["description"], rules, updated_time)

        # Output to rules/<filename>
        target_path = os.path.join(rules_dir, data["filename"])
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        generated_files.append(target_path)

        # Also copy/mirror to root as <Name>.yaml
        root_target = os.path.join(root_dir, f"{name}.yaml")
        shutil.copyfile(target_path, root_target)
        generated_files.append(root_target)

    # 2. Generate aggregated ai-providers file
    agg_content = generate_yaml_content(
        "AIProviders",
        "Consolidated ruleset for OpenAI, Anthropic, and Antigravity (Gemini/Google AI)",
        all_rules,
        updated_time,
    )
    agg_rules_path = os.path.join(rules_dir, "ai-providers.yaml")
    with open(agg_rules_path, "w", encoding="utf-8") as f:
        f.write(agg_content)
    generated_files.append(agg_rules_path)

    # Root mirror for aggregated file
    agg_root_path = os.path.join(root_dir, "AIProviders.yaml")
    shutil.copyfile(agg_rules_path, agg_root_path)
    generated_files.append(agg_root_path)

    print(f"Successfully generated {len(generated_files)} ruleset files:")
    for gf in generated_files:
        rel = os.path.relpath(gf, root_dir)
        print(f" - {rel}")


if __name__ == "__main__":
    main()
