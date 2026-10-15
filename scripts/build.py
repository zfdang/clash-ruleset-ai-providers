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
        "description": "Rules for OpenAI (ChatGPT, API, Sora, Voice LiveKit/Egress IPs, CDN, ArkoseLabs)",
        "rules": [
            # Core domains & Web
            "DOMAIN-SUFFIX,openai.com",
            "DOMAIN-SUFFIX,chatgpt.com",
            "DOMAIN-SUFFIX,chat.com",
            "DOMAIN-SUFFIX,sora.com",
            "DOMAIN-SUFFIX,oaistatic.com",
            "DOMAIN-SUFFIX,oaiusercontent.com",
            "DOMAIN-SUFFIX,oaistatsig.com",
            "DOMAIN-SUFFIX,crixet.com",
            "DOMAIN-SUFFIX,chatgpt.site",
            # Voice / Realtime streaming (OpenAI specific tenant)
            "DOMAIN-SUFFIX,chatgpt.livekit.cloud",
            # OpenAI Specific CDN & Dedicated Endpoints
            "DOMAIN,cdn.openaimerge.com",
            "DOMAIN,chat.openai.com.cdn.cloudflare.net",
            "DOMAIN,openaiassets.blob.core.windows.net",
            "DOMAIN,openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net",
            "DOMAIN,openaicomproductionae4b.blob.core.windows.net",
            "DOMAIN,production-openaicom-storage.azureedge.net",
            "DOMAIN,openaiapi-site.azureedge.net",
            "DOMAIN,openaicom.imgix.net",
            "DOMAIN,static.cloudflareinsights.com",
            "DOMAIN,browser-intake-datadoghq.com",
            "DOMAIN,openai.qualtrics.com",
            "DOMAIN,o33249.ingest.sentry.io",
            # Human Verification (Specific Arkose endpoints for OpenAI, avoid broad arkoselabs.com)
            "DOMAIN,openai-api.arkoselabs.com",
            "DOMAIN,client-api.arkoselabs.com",
            # ChatGPT Voice Official Egress IPs (https://openai.com/chatgpt-voice.json)
            "IP-CIDR,4.151.200.38/32,no-resolve",
            "IP-CIDR,4.155.146.196/32,no-resolve",
            "IP-CIDR,4.197.172.116/32,no-resolve",
            "IP-CIDR,4.217.235.100/32,no-resolve",
            "IP-CIDR,4.245.198.13/32,no-resolve",
            "IP-CIDR,13.71.25.29/32,no-resolve",
            "IP-CIDR,20.74.221.21/32,no-resolve",
            "IP-CIDR,20.162.96.163/32,no-resolve",
            "IP-CIDR,20.168.48.117/32,no-resolve",
            "IP-CIDR,20.184.36.134/32,no-resolve",
            "IP-CIDR,20.203.144.245/32,no-resolve",
            "IP-CIDR,40.118.236.137/32,no-resolve",
            "IP-CIDR,51.4.112.173/32,no-resolve",
            "IP-CIDR,52.143.181.161/32,no-resolve",
            "IP-CIDR,68.155.152.41/32,no-resolve",
            "IP-CIDR,72.146.20.246/32,no-resolve",
            "IP-CIDR,74.248.148.7/32,no-resolve",
            "IP-CIDR,102.37.57.54/32,no-resolve",
            "IP-CIDR,135.220.40.201/32,no-resolve",
            "IP-CIDR,172.203.39.49/32,no-resolve",
            "IP-CIDR,172.207.173.200/32,no-resolve",
            "IP-CIDR,172.214.226.198/32,no-resolve",
            "IP-CIDR,191.233.251.27/32,no-resolve",
        ],
    },
    "Anthropic": {
        "filename": "anthropic.yaml",
        "description": "Rules for Anthropic & Claude (Web, API, Dev/MCP, CDN, Official IPs)",
        "rules": [
            # Core domains & Web
            "DOMAIN-SUFFIX,anthropic.com",
            "DOMAIN-SUFFIX,claude.ai",
            "DOMAIN-SUFFIX,claude.com",
            "DOMAIN-SUFFIX,clau.de",
            "DOMAIN-SUFFIX,claude.dev",
            "DOMAIN-SUFFIX,claudeusercontent.com",
            "DOMAIN-SUFFIX,claudemcpclient.com",
            "DOMAIN-SUFFIX,claudemcpcontent.com",
            # CDN & Endpoints
            "DOMAIN,servd-anthropic-website.b-cdn.net",
            "DOMAIN,anthropic.imgix.net",
            # Official IP Range (https://docs.anthropic.com/en/api/ip-addresses)
            "IP-CIDR,160.79.104.0/21,no-resolve",
        ],
    },
    "Antigravity": {
        "filename": "antigravity.yaml",
        "description": "Rules for Google Antigravity & Gemini / Google AI Services",
        "rules": [
            # Antigravity Core Cloud Code Backend & Service Endpoints
            "DOMAIN,antigravity-pa.googleapis.com",
            "DOMAIN,antigravity.googleapis.com",
            "DOMAIN,daily-cloudcode-pa.googleapis.com",
            "DOMAIN,cloudcode-pa.googleapis.com",
            "DOMAIN,cloudaicompanion.googleapis.com",
            "DOMAIN,geller-pa.googleapis.com",
            "DOMAIN,robinfrontend-pa.googleapis.com",
            "DOMAIN,aisandbox-pa.googleapis.com",
            "DOMAIN-SUFFIX,antigravity-unleash.goog",
            # Antigravity Web & AI Code Assist Endpoints
            "DOMAIN,antigravity.google.com",
            "DOMAIN,aicode.googleapis.com",
            "DOMAIN,alkalicore-pa.clients6.google.com",
            "DOMAIN,geminiweb-pa.clients6.google.com",
            "DOMAIN,webchannel-alkalimakersuite-pa.clients6.google.com",
            "DOMAIN,alkalimakersuite-pa.clients6.google.com",
            "DOMAIN,proactivebackend-pa.googleapis.com",
            # Gemini API & Generative Language
            "DOMAIN,generativelanguage.googleapis.com",
            "DOMAIN-SUFFIX,generativeai.google",
            # Google AI Studio, MakerSuite & NotebookLM
            "DOMAIN,aistudio.google.com",
            "DOMAIN,makersuite.google.com",
            "DOMAIN,notebooklm.google.com",
            "DOMAIN,ai.google.dev",
            "DOMAIN-SUFFIX,ai.studio",
            # Gemini & DeepMind Web Platforms
            "DOMAIN-SUFFIX,gemini.google.com",
            "DOMAIN-SUFFIX,gemini.google",
            "DOMAIN,gemini.gstatic.com",
            "DOMAIN-SUFFIX,bard.google.com",
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


def get_existing_timestamp(file_path):
    """Extract existing UPDATED timestamp from file if it exists."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("# UPDATED:"):
                        return line.split("# UPDATED:", 1)[1].strip()
        except Exception:
            pass
    return None


def get_existing_payload(file_path):
    """Extract payload lines from existing file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if "payload:" in content:
                    return content.split("payload:", 1)[1].strip()
        except Exception:
            pass
    return None


def generate_yaml_content(name, description, rules, current_time, target_path=None):
    sorted_rules = parse_and_sort_rules(rules)
    stats = count_stats(sorted_rules)

    new_payload = "\n".join([f"  - {r}" for r in sorted_rules]).strip()
    updated_time = current_time

    # If file exists and payload rules haven't changed, retain original timestamp
    if target_path and os.path.exists(target_path):
        old_payload = get_existing_payload(target_path)
        old_timestamp = get_existing_timestamp(target_path)
        if old_payload == new_payload and old_timestamp:
            updated_time = old_timestamp

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
        target_path = os.path.join(rules_dir, data["filename"])
        content = generate_yaml_content(name, data["description"], rules, updated_time, target_path=target_path)

        # Output to rules/<filename>
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        generated_files.append(target_path)

        # Also copy/mirror to root as <Name>.yaml
        root_target = os.path.join(root_dir, f"{name}.yaml")
        shutil.copyfile(target_path, root_target)
        generated_files.append(root_target)

    # 2. Generate aggregated ai-providers file
    agg_rules_path = os.path.join(rules_dir, "ai-providers.yaml")
    agg_content = generate_yaml_content(
        "AIProviders",
        "Consolidated ruleset for OpenAI, Anthropic, and Antigravity (Gemini/Google AI)",
        all_rules,
        updated_time,
        target_path=agg_rules_path,
    )
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
