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
| **AIProviders** | **三合一全量合集**（含 OpenAI、Anthropic、Antigravity 全部域名与官方出口 IP） | 89 | [Raw 链接](https://raw.githubusercontent.com/zfdang/clash-ruleset-ai-providers/main/AIProviders.yaml) | [CDN 链接](https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/AIProviders.yaml) |
| **OpenAI** | ChatGPT、Sora、OpenAI API、LiveKit 租户、专用 CDN、官方 Voice 出口 IP | 47 | [Raw 链接](https://raw.githubusercontent.com/zfdang/clash-ruleset-ai-providers/main/OpenAI.yaml) | [CDN 链接](https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/OpenAI.yaml) |
| **Antigravity** | Google Antigravity 编辑器、Gemini、Cloud Code PA、AI Studio、NotebookLM | 31 | [Raw 链接](https://raw.githubusercontent.com/zfdang/clash-ruleset-ai-providers/main/Antigravity.yaml) | [CDN 链接](https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/Antigravity.yaml) |
| **Anthropic** | Claude (Web/App)、Anthropic API、Dev/MCP 专用端点、官方 CIDR 网段 | 11 | [Raw 链接](https://raw.githubusercontent.com/zfdang/clash-ruleset-ai-providers/main/Anthropic.yaml) | [CDN 链接](https://fastly.jsdelivr.net/gh/zfdang/clash-ruleset-ai-providers@main/Anthropic.yaml) |

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
- **核心站点与产品**：`DOMAIN-SUFFIX,openai.com`, `DOMAIN-SUFFIX,chatgpt.com`, `DOMAIN-SUFFIX,chat.com`, `DOMAIN-SUFFIX,sora.com`, `DOMAIN-SUFFIX,oaistatic.com`, `DOMAIN-SUFFIX,oaiusercontent.com`, `DOMAIN-SUFFIX,oaistatsig.com`, `DOMAIN-SUFFIX,crixet.com`, `DOMAIN-SUFFIX,chatgpt.site`
- **实时语音通讯 (LiveKit 专属租户)**：`DOMAIN-SUFFIX,chatgpt.livekit.cloud`
- **人机验证 (ArkoseLabs 专用子域)**：`DOMAIN,openai-api.arkoselabs.com`, `DOMAIN,client-api.arkoselabs.com`
- **专用 CDN / 资源存储 / 精准埋点**：`DOMAIN,cdn.openaimerge.com`, `DOMAIN,chat.openai.com.cdn.cloudflare.net`, `DOMAIN,openaiassets.blob.core.windows.net`, `DOMAIN,openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net`, `DOMAIN,openaicomproductionae4b.blob.core.windows.net`, `DOMAIN,production-openaicom-storage.azureedge.net`, `DOMAIN,openaiapi-site.azureedge.net`, `DOMAIN,openaicom.imgix.net`, `DOMAIN,browser-intake-datadoghq.com`, `DOMAIN,static.cloudflareinsights.com`, `DOMAIN,openai.qualtrics.com`, `DOMAIN,o33249.ingest.sentry.io`
- **官方 ChatGPT Voice 出口 IP**：`4.151.200.38/32` 等共计 23 个 `/32`（数据来源：`https://openai.com/chatgpt-voice.json`）

### 🧠 Anthropic
- **核心站点与 Web**：`DOMAIN-SUFFIX,anthropic.com`, `DOMAIN-SUFFIX,claude.ai`, `DOMAIN-SUFFIX,claude.com`, `DOMAIN-SUFFIX,clau.de`, `DOMAIN-SUFFIX,claude.dev`, `DOMAIN-SUFFIX,claudeusercontent.com`
- **开发者与 MCP 专用**：`DOMAIN-SUFFIX,claudemcpclient.com`, `DOMAIN-SUFFIX,claudemcpcontent.com`
- **专用 CDN**：`DOMAIN,servd-anthropic-website.b-cdn.net`, `DOMAIN,anthropic.imgix.net`
- **官方公布 IP 网段**：`IP-CIDR,160.79.104.0/21,no-resolve`（数据来源：`https://docs.anthropic.com/en/api/ip-addresses`）

### 🚀 Antigravity (Google)
- **后端服务 (Cloud Code PA / 调度服务)**：`DOMAIN,antigravity-pa.googleapis.com`, `DOMAIN,antigravity.googleapis.com`, `DOMAIN,daily-cloudcode-pa.googleapis.com`, `DOMAIN,cloudcode-pa.googleapis.com`, `DOMAIN,cloudaicompanion.googleapis.com`, `DOMAIN,geller-pa.googleapis.com`, `DOMAIN,robinfrontend-pa.googleapis.com`, `DOMAIN,aisandbox-pa.googleapis.com`, `DOMAIN-SUFFIX,antigravity-unleash.goog`
- **推理与辅助接口**：`DOMAIN,antigravity.google.com`, `DOMAIN,aicode.googleapis.com`, `DOMAIN,alkalicore-pa.clients6.google.com`, `DOMAIN,geminiweb-pa.clients6.google.com`, `DOMAIN,webchannel-alkalimakersuite-pa.clients6.google.com`, `DOMAIN,alkalimakersuite-pa.clients6.google.com`, `DOMAIN,generativelanguage.googleapis.com`, `DOMAIN-SUFFIX,generativeai.google`, `DOMAIN,proactivebackend-pa.googleapis.com`, `DOMAIN,aiplatform.googleapis.com`
- **官方产品与平台**：`DOMAIN,aistudio.google.com`, `DOMAIN,makersuite.google.com`, `DOMAIN,notebooklm.google.com`, `DOMAIN,ai.google.dev`, `DOMAIN-SUFFIX,ai.studio`, `DOMAIN-SUFFIX,gemini.google.com`, `DOMAIN-SUFFIX,gemini.google`, `DOMAIN,gemini.gstatic.com`, `DOMAIN-SUFFIX,bard.google.com`, `DOMAIN-SUFFIX,deepmind.google`, `DOMAIN-SUFFIX,deepmind.com`
- **身份认证**：`DOMAIN,oauth2.googleapis.com`

---

## 🌐 域名与 IP 来源出处深度解析 (Provenance & Sources)

本项目收录的所有域名与 IP 规则均有据可查，严格遵循 **“官方文档优先、权威上游交叉验证、精准实测兜底”** 的原则。

### 1. 核心数据来源体系

| 来源分类 | 主要出处与依据 | 作用与贡献 |
| :--- | :--- | :--- |
| **官方技术文档与端点** | • OpenAI Voice IP List: `https://openai.com/chatgpt-voice.json`<br>• Anthropic API IP Ranges: `https://docs.anthropic.com/en/api/ip-addresses` | 提供厂商第一手官方认可的入站与出站固定 CIDR / IP，保证语音流与 API 通信不漏球。 |
| **权威开源规则上游** | • `v2fly/domain-list-community` (MetaCubeX geosite 上游)<br>• `ACL4SSR`、`dler-io`、`blackmatrix7` (精炼过滤版) | 汇聚全球开发者长期维护的可靠域名库，用于交叉校验新老域名与专有 CDN。 |
| **本地抓包与逆向分析** | • Google Antigravity 本地 `language_server` 与客户端网络抓包 | 精准提取 Antigravity 编辑器在 Agent 运行与代码辅助时所建立的私有 PA 调度连接。 |
| **网络真实性测探** | • WHOIS 溯源反查<br>• HTTP 重定向与证书链检测 | 剔除已失效域名（如 `ai.com`）与历史误收录机房 ASN（如 Vultr `AS20473`）。 |

---

### 2. 各 Provider 规则归属明细

#### 🤖 OpenAI 规则来源

| 条目 / 规则 | 归属分类 | 详细来源与技术依据 |
| :--- | :--- | :--- |
| `openai.com`, `chatgpt.com`, `oaistatic.com`, `oaiusercontent.com` | 核心产品资产 | OpenAI 官方 Web / App 核心服务主域名与前端静态文件托管域（上游 v2fly 标配）。 |
| `chat.com` | 核心产品资产 | OpenAI 于 2024 年底斥巨资收购并直接 301 重定向至 ChatGPT 首页的顶级官方域名。 |
| `sora.com` | 核心产品资产 | OpenAI 旗下文生视频模型 Sora 的官方独立 Web 产品主域名。 |
| `oaistatsig.com` | 特征开关与灰度 | OpenAI 官方搭建的专属 Statsig 代理网关，**取代有误伤风险的通用 `statsig.com`**。 |
| `crixet.com`, `chatgpt.site` | 重定向与关联资产 | OpenAI 官方备案持有的相关产品辅助域名（经 v2fly / MetaCubeX 确认收录）。 |
| `chatgpt.livekit.cloud` | 实时语音通话 | ChatGPT 官方高级语音模式 (Advanced Voice Mode) 专用的 LiveKit WebRTC 租户端点。 |
| `cdn.openaimerge.com`, `openaiassets.blob.core.windows.net`, `openaicom-*.azurefd.net` | 专用 CDN 与存储 | 包含 OpenAI 专属租户标识的 Microsoft Azure Front Door 及 Azure Blob 存储节点。 |
| `openai.qualtrics.com` | 用户调查与反馈 | OpenAI 在 Qualtrics 平台开设的专有问卷收集子域名。 |
| `o33249.ingest.sentry.io` | 精准崩溃上报 | OpenAI 组织在 Sentry 的专属数据上报主机，**精准定位单个主机，坚决不通配全局 `sentry.io`**。 |
| `openai-api.arkoselabs.com`, `client-api.arkoselabs.com` | 人机验证 (Captcha) | OpenAI 登录注册与防刷安全验证所使用的专属子域名（拒绝使用泛 `arkoselabs.com`）。 |
| 23 个 `/32` IP (`4.151.200.38/32` 等) | 官方 Voice 出口 IP | **官方公布**：直接提取自官方权威地址 `https://openai.com/chatgpt-voice.json`。 |

#### 🧠 Anthropic (Claude) 规则来源

| 条目 / 规则 | 归属分类 | 详细来源与技术依据 |
| :--- | :--- | :--- |
| `anthropic.com`, `claude.ai` | 核心产品资产 | Anthropic 官方公司主页、API 基础接口端点及 Claude Web 交互主域名。 |
| `claude.com`, `clau.de` | 官方域名与短链 | Anthropic 官方品牌顶级域名以及官方发布的推文短链接跳转域（上游 v2fly 交叉验证）。 |
| `claude.dev` | 开发者中心 | Anthropic 面向 API 开发者与模型生态建设的官方门户域名。 |
| `claudeusercontent.com` | 渲染与用户内容 | **关键依赖**：Claude 用于展示代码预览、HTML/SVG 交互沙箱 (Artifacts) 及多模态素材的核心资产域。 |
| `claudemcpclient.com`, `claudemcpcontent.com` | 协议专有端点 | Claude Model Context Protocol (MCP) 模型上下文协议体系专用的客户端与上下文交换域名。 |
| `servd-anthropic-website.b-cdn.net`, `anthropic.imgix.net` | 静态素材 CDN | 官方官方文档站点与前端静态图片加速端点（BunnyCDN 与 Imgix）。 |
| `IP-CIDR,160.79.104.0/21,no-resolve` | 官方公布 IP 网段 | **官方公布**：直接来源于 Anthropic 开发者文档 [IP Addresses](https://docs.anthropic.com/en/api/ip-addresses)，涵盖全部出入站 API CIDR。 |

#### 🚀 Antigravity (Google / Gemini) 规则来源

| 条目 / 规则 | 归属分类 | 详细来源与技术依据 |
| :--- | :--- | :--- |
| `daily-cloudcode-pa.googleapis.com`, `cloudcode-pa.googleapis.com` | IDE 核心调度后端 | Antigravity 官方编辑器本地后台语言服务 (`language_server`) 启动参数中强制指定的云端 PA 通信后端。 |
| `antigravity-pa.googleapis.com`, `antigravity.googleapis.com`, `antigravity.google.com` | 产品专属服务 | Google 内部为 Antigravity AI 原生编辑器独立配置的服务总线与 API 映射端点。 |
| `antigravity-unleash.goog` | 功能灰度与分流 | Antigravity 编辑器内置功能灰度发布（基于 Unleash 系统）专用的 Google `.goog` 顶级域名。 |
| `cloudaicompanion.googleapis.com`, `geller-pa.googleapis.com`, `robinfrontend-pa.googleapis.com` | AI Companion 辅助 | Google Cloud Code / Gemini Code Assist 代码理解与补全的核心后台服务（上游 v2fly 交叉确认）。 |
| `generativelanguage.googleapis.com`, `generativeai.google` | Gemini 推理 API | Google Gemini 与 PaLM 系列大语言模型官方对外 Generative Language API 的核心通信接口。 |
| `alkalicore-pa.clients6.google.com`, `geminiweb-pa.clients6.google.com`, `webchannel-alkalimakersuite-pa.clients6.google.com` | Web 通道与长连接 | Gemini 网页工作台与 MakerSuite 建立双向长连接 (WebChannel / gRPC over HTTP) 的必要端点。 |
| `aistudio.google.com`, `makersuite.google.com`, `ai.google.dev`, `ai.studio` | 官方开发者平台 | Google AI Studio（原 MakerSuite）官方控制台与 Google AI 开发者门户入口。 |
| `notebooklm.google.com` | 知识与研究助手 | Google DeepMind 驱动的 AI 交互式笔记本应用 NotebookLM 官方主域名。 |
| `gemini.google`, `gemini.google.com`, `gemini.gstatic.com` | 产品与静态资源 | Gemini 官方品牌域名、对话主页及专属静态资源加速域名（严格隔离于通用 `gstatic.com`）。 |
| `deepmind.google`, `deepmind.com` | 机构核心主页 | Google DeepMind 官方研究主页及模型发布门户。 |
| `oauth2.googleapis.com` | 身份认证与凭据 | Antigravity Agent 模式下进行 Google 账号 Token 刷新与鉴权交换的必要端点。 |

---

### 3. 被剔除规则的溯源与证伪证据

为保持规则集极致纯净，本项目对传统规则集中的常见错误条目进行了严格审计并予以剔除：

1. **`ai.com`（已剔除）**：
   - *历史背景*：曾被 OpenAI 短暂租用并跳转到 ChatGPT。
   - *实测现状*：经 `curl -sIL https://ai.com` 测探，目前已跳转至 `https://ai.com/start`，由一家独立的第三方 AI Agent 公司运营，**已完全脱离 OpenAI 体系**，上游主流列表均已废弃。
2. **`IP-ASN,20473`（已剔除）**：
   - *历史背景*：blackmatrix7 等规则集中收录。
   - *实测现状*：WHOIS 反查结果为 `The Constant Company LLC`（即主机商 **Vultr** 的全机房 ASN）。若收录会导致访问 Vultr 全球所有 VPS 的流量均被劫持进 AI 节点，属于严重收录失误。
3. **`24.199.123.28/32`, `64.23.132.171/32`（已剔除）**：
   - *实测现状*：WHOIS 查证为 DigitalOcean 机房的个人反代主机，非 OpenAI 官方资产。
4. **`stripe.com`, `auth0.com`, `challenges.cloudflare.com`, `sentry.io`（已剔除）**：
   - *实测现状*：均为全球通用的公共基础设施，通配收录会引发全局非 AI 业务的误伤与支付风控。OpenAI 所需的专用部分已通过特定主机（如 `o33249.ingest.sentry.io`、`openai-api.arkoselabs.com`）精准替代。
5. **所有关键词规则 (`DOMAIN-KEYWORD`)（已剔除）**：
   - *实测现状*：关键词会粗暴匹配任意包含子串的无关网站（如包含 `openai` 或 `claude` 的个人博客与讨论帖），违背精准分流原则。上游权威列表（v2fly、MetaCubeX）均不采用关键词匹配。

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