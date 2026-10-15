# Clash Ruleset for AI Providers

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ruleset: Clash Classical](https://img.shields.io/badge/Clash-Rule--Provider-orange.svg)](#-clash--mihomo-使用配置教程)

专为 **Clash** / **Clash Meta (Mihomo)** / **Clash Verge Rev** / **Clash Nyanpasu** / **Stash** / **Shadowrocket** 设计的高精度 AI Provider 分流规则集。

专注于纯粹的 **域名 (DOMAIN)** 与 **IP/ASN** 资源匹配，**不依赖** 客户端进程名，具备极佳的通用性与跨平台兼容性。

---

## 🎯 规则设计准则：恰到好处的精准度

> **既不盲目扩大范围导致误伤，也不遗漏关键依赖导致服务异常。**

### 1. 杜绝“滥用全局域名”造成的误伤
很多传统 AI 规则集将公共第三方服务的大域名直接打包收录，导致极大的副作用：
- **`stripe.com` (通用支付)**：若强行代理进 AI 节点，在访问其他完全无关的海外电商/SaaS 付款时会频繁触发风控阻断。
- **`auth0.com` (通用身份认证)**：全球成千上万个非 AI 网站使用 Auth0 登录，强行代理会导致登录状态混乱。
- **`challenges.cloudflare.com` (Cloudflare Turnstile 验证码)**：全网海量网站使用该验证服务，不应归为 AI 专有规则。
- **`arkoselabs.com`**：本项目仅精准收录 OpenAI 专用的验证子域名（`openai-api.arkoselabs.com` 与 `client-api.arkoselabs.com`），而非粗暴通配全局。

### 2. Antigravity 的高精度分流（保护 Google 日常服务）
Google DeepMind 的 **Antigravity** 编辑器依赖 Google 后端。若粗暴匹配 `google.com` 或 `googleapis.com`，会将用户的日常 Google 搜索、YouTube 视频、Gmail 以及 Chrome 同步流量全部绑架到 Antigravity 节点上。

本项目通过反编译分析 `Antigravity`、`language_server` 后台服务与抓包，精确提取了其核心服务域名：
- **IDE 核心调度后端**：`daily-cloudcode-pa.googleapis.com`、`cloudcode-pa.googleapis.com`、`preprod-daily-cloudcode-pa.sandbox.googleapis.com`
- **模型推理与代码生成 API**：`generativelanguage.googleapis.com`、`aicode.googleapis.com`、`aiplatform.googleapis.com`、`proactivebackend-pa.googleapis.com`
- **平台与工作台**：`antigravity.google.com`、`aistudio.google.com`、`makersuite.google.com`、`gemini.google.com`、`deepmind.google`
- **Agent 鉴权交换**：`oauth2.googleapis.com`

---

## 📦 规则集列表与订阅链接

| 规则集名称 | 适用范围 | 条目数 | GitHub Raw 订阅链接 | CDN 快速订阅链接 (jsDelivr) |
| :--- | :--- | :---: | :--- | :--- |
| **AIProviders** | **三合一全量合集**（含 OpenAI、Anthropic、Antigravity 全部域名与 IP） | 52+ | [Raw 链接](https://raw.githubusercontent.com/zfdang/clash-ruleset-ai-providers/main/AIProviders.yaml) | [CDN 链接](https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/AIProviders.yaml) |
| **Antigravity** | Google Antigravity 编辑器、Gemini API、Cloud Code PA 后端 | 21+ | [Raw 链接](https://raw.githubusercontent.com/zfdang/clash-ruleset-ai-providers/main/Antigravity.yaml) | [CDN 链接](https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/Antigravity.yaml) |
| **OpenAI** | ChatGPT (Web / 桌面端 / 语音通话 LiveKit)、OpenAI API、专用 CDN | 23+ | [Raw 链接](https://raw.githubusercontent.com/zfdang/clash-ruleset-ai-providers/main/OpenAI.yaml) | [CDN 链接](https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/OpenAI.yaml) |
| **Anthropic** | Claude (Web / 桌面端)、Anthropic API、Claude 专有 CDN | 8+ | [Raw 链接](https://raw.githubusercontent.com/zfdang/clash-ruleset-ai-providers/main/Anthropic.yaml) | [CDN 链接](https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/Anthropic.yaml) |

> 仓库根目录与 `rules/` 子目录下的文件完全一致，您可以按喜好引用。

---

## 🚀 Clash / Mihomo 使用配置教程

无论您使用的是 **Clash Verge Rev**、**Mihomo Party**、**Clash Nyanpasu** 还是 **原版 Clash**，只需将规则加入配置文件的 `rule-providers`、`proxy-groups` 与 `rules` 即可。

### 方案一：三类 Provider 独立分流（推荐）

各个 AI 厂商风控标准不一（如 Antigravity 对机房 IP 要求极严，Claude 偏好英美节点，OpenAI 支持多地区）。独立分流允许为每个 AI 平台指定不同的出口节点。

```yaml
# 1. 策略组配置 (proxy-groups)
proxy-groups:
  # Antigravity 策略组：强烈建议分配纯净家庭宽带 / 住宅 IP，避开常见数据中心机房
  - name: "🚀 Antigravity"
    type: select
    proxies:
      - "🇺🇸 美国住宅"
      - "🇸🇬 新加坡原生"
      - DIRECT

  # OpenAI 策略组：美国 / 日本 / 新加坡 等常用优质节点
  - name: "🤖 OpenAI"
    type: select
    proxies:
      - "🇺🇸 美国 01"
      - "🇯🇵 日本 01"
      - DIRECT

  # Anthropic 策略组：Claude 服务节点
  - name: "🧠 Anthropic"
    type: select
    proxies:
      - "🇺🇸 美国 01"
      - "🇬🇧 英国 01"
      - DIRECT

# 2. 规则提供者 (rule-providers)
rule-providers:
  antigravity-rules:
    type: http
    behavior: classical
    url: "https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/Antigravity.yaml"
    path: ./ruleset/Antigravity.yaml
    interval: 86400

  openai-rules:
    type: http
    behavior: classical
    url: "https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/OpenAI.yaml"
    path: ./ruleset/OpenAI.yaml
    interval: 86400

  anthropic-rules:
    type: http
    behavior: classical
    url: "https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/Anthropic.yaml"
    path: ./ruleset/Anthropic.yaml
    interval: 86400

# 3. 匹配规则 (rules)
rules:
  - RULE-SET,antigravity-rules,🚀 Antigravity
  - RULE-SET,openai-rules,🤖 OpenAI
  - RULE-SET,anthropic-rules,🧠 Anthropic
  # 其他常规规则（如 GEOIP,CN,DIRECT 等）
```

---

### 方案二：统一聚合分流

如果您只需要一个统管所有 AI 服务的策略组，使用 `AIProviders.yaml` 即可一步到位：

```yaml
# 1. 策略组配置
proxy-groups:
  - name: "✨ AI Services"
    type: select
    proxies:
      - "🇺🇸 美国 01"
      - "🇯🇵 日本 01"
      - "🇸🇬 新加坡 01"
      - DIRECT

# 2. 规则提供者
rule-providers:
  ai-providers:
    type: http
    behavior: classical
    url: "https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/AIProviders.yaml"
    path: ./ruleset/AIProviders.yaml
    interval: 86400

# 3. 匹配规则
rules:
  - RULE-SET,ai-providers,✨ AI Services
  # 其他常规规则
```

---

## 🔍 各 Provider 收录明细对照表

### 🤖 OpenAI
- **核心站点与 Web**：`DOMAIN-SUFFIX,openai.com`, `DOMAIN-SUFFIX,chatgpt.com`, `DOMAIN-SUFFIX,oaistatic.com`, `DOMAIN-SUFFIX,oaiusercontent.com`, `DOMAIN-SUFFIX,ai.com`
- **实时语音通讯 (LiveKit WebRTC)**：`DOMAIN-SUFFIX,chatgpt.livekit.cloud`, `DOMAIN-SUFFIX,host.livekit.cloud`, `DOMAIN-SUFFIX,turn.livekit.cloud`
- **人机验证 (ArkoseLabs 专用子域)**：`DOMAIN,openai-api.arkoselabs.com`, `DOMAIN,client-api.arkoselabs.com`
- **专用 CDN / 资源存储**：`DOMAIN,chat.openai.com.cdn.cloudflare.net`, `DOMAIN,openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net`, `DOMAIN,openaicomproductionae4b.blob.core.windows.net`, `DOMAIN,production-openaicom-storage.azureedge.net`, `DOMAIN,openaiapi-site.azureedge.net`, `DOMAIN,openaicom.imgix.net`, `DOMAIN,browser-intake-datadoghq.com`, `DOMAIN,static.cloudflareinsights.com`
- **关键词与专用 IP/ASN**：`DOMAIN-KEYWORD,openai`, `DOMAIN-KEYWORD,chatgpt`, `IP-CIDR,24.199.123.28/32,no-resolve`, `IP-CIDR,64.23.132.171/32,no-resolve`, `IP-ASN,20473,no-resolve`

### 🧠 Anthropic
- **核心站点与 Web**：`DOMAIN-SUFFIX,anthropic.com`, `DOMAIN-SUFFIX,claude.ai`, `DOMAIN-SUFFIX,claude.com`, `DOMAIN-SUFFIX,claudeusercontent.com`
- **专用 CDN**：`DOMAIN,servd-anthropic-website.b-cdn.net`, `DOMAIN,anthropic.imgix.net`
- **关键词**：`DOMAIN-KEYWORD,anthropic`, `DOMAIN-KEYWORD,claude`

### 🚀 Antigravity (Google)
- **后端服务 (Cloud Code PA)**：`DOMAIN,daily-cloudcode-pa.googleapis.com`, `DOMAIN,cloudcode-pa.googleapis.com`, `DOMAIN,autopush-cloudcode-pa.sandbox.googleapis.com`, `DOMAIN,preprod-daily-cloudcode-pa.sandbox.googleapis.com`
- **推理与辅助接口**：`DOMAIN,generativelanguage.googleapis.com`, `DOMAIN,aicode.googleapis.com`, `DOMAIN,aiplatform.googleapis.com`, `DOMAIN,alkalimakersuiteapplets.pa.googleapis.com`, `DOMAIN,alkalimakersuite-pa.clients6.google.com`, `DOMAIN,proactivebackend-pa.googleapis.com`
- **官方产品与站点**：`DOMAIN,antigravity.google.com`, `DOMAIN,aistudio.google.com`, `DOMAIN,makersuite.google.com`, `DOMAIN,ai.google.dev`, `DOMAIN-SUFFIX,gemini.google.com`, `DOMAIN-SUFFIX,bard.google.com`, `DOMAIN-SUFFIX,deepmind.google`, `DOMAIN-SUFFIX,deepmind.com`, `DOMAIN-SUFFIX,generativeai.google`
- **身份认证**：`DOMAIN,oauth2.googleapis.com`

---

## 💡 Antigravity 常见报错与排查建议

当 Antigravity 在 Agent 执行模式下报错：
```text
agent executor error: FAILED_PRECONDITION (code 400): User location is not supported for the API use.
```

**原因分析与对策**：
1. **IP 属性问题（机房 IDC vs 住宅 ISP）**：Google 的 Agent 路径不仅检查国家代码，还会检测出口 IP 的 ASN / 机房特征。常见的主机商托管 IP（如 AWS / GCP / DigitalOcean 等大厂机房广播 IP）极易被拦截。**对策**：为 Antigravity 策略组切换原生住宅宽带或低风控小众 ISP 节点。
2. **确认网络分流命中**：打开 Clash 客户端的「连接 (Connections)」或「日志 (Logs)」面板，触发 Antigravity 提问，观察是否有 `daily-cloudcode-pa.googleapis.com` 或 `generativelanguage.googleapis.com` 连接，确认其是否准确流经你指定的 Antigravity 策略组。

---

## 🛠️ 本地构建与维护

仓库内所有规则文件均通过 Python 脚本自动构建，确保排序标准、去重无误：

```bash
# 修改 scripts/build.py 内的 RULES_DATA 后运行：
python3 scripts/build.py
```

构建脚本将自动：
- 对每类规则去重、按类型排布优先级 (`DOMAIN` → `DOMAIN-SUFFIX` → `DOMAIN-KEYWORD` → `IP-CIDR` → `IP-ASN`)
- 自动重新统计各类型条目数量及最后更新时间
- 同步生成根目录与 `rules/` 目录的单体规则与全量聚合规则

---

## 📄 License

本项目基于 [MIT License](LICENSE) 开源。欢迎 Star、Fork 或提交 PR 共同完善端点。