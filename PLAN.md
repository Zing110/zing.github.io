# 个人主页项目规划

> 最后更新:2026-07-07 · 维护中

## 项目概述

**目标**:搭建个人主页,用于工作申请、博士申请,展示研究/项目经历,并集成一个"懂我"的对话 Agent。

**风格演变**:初始设想"月之暗面风格"(简约优雅科技感),实操中演变为 **《无人深空》星系选择风格**——深空黑、稀疏星点、白色小光点星球(hover 才高亮)、星座式连线、神秘感来自"少"而非"多"。

**核心功能**:
1. 星云交互 Hero(3D,可探索星球 = 项目/技能)
2. 静态内容页(关于/研究/经历/论文)
3. 对话 Agent(目前 mock,后期接真实模型)

---

## 技术选型(已落地)

### 前端
- **框架**:Astro v7(islands 架构,静态内容用 .astro,交互组件用 React)
- **样式**:Tailwind v4(Vite 插件方式)
- **3D**:React Three Fiber + drei + three.js(星云场景)
- **字体**:Inter / JetBrains Mono(Google Fonts)

### 部署
- **托管**:GitHub Pages,仓库 `Zing110/zing.github.io`(项目仓库,非用户主页仓库)
- **线上地址**:https://zing110.github.io/zing.github.io/
- **构建**:GitHub Actions(`Source = GitHub Actions`,因为 Astro 需要构建步骤,不能用 branch 部署)
- **base 路径**:Astro 配 `/zing.github.io/`(项目仓库子路径),所有内部链接已适配

### Agent 后端(规划,未实现)
- **运行时**:Cloudflare Workers(免费 10 万次/天)
- **模型**:DeepSeek-V3(性价比最高,月成本 ¥1 内)
- **限流**:Cloudflare KV(每 IP 每分钟 5 次)
- **抽象层**:`src/lib/chatService.ts`——mock 实现,未来换真实 API 只改这一个文件

---

## 当前状态(截至 2026-07-07)

### ✅ 已完成
- [x] Astro + Tailwind + React 骨架搭建
- [x] 设计系统(`global.css`:深色主题、紫蓝渐变、毛玻璃、光晕)
- [x] 布局组件(Layout / Navbar / Footer),base 路径适配
- [x] GitHub Actions 自动部署,线上可访问
- [x] **星云交互 Hero**(`Nebula.tsx` + `NebulaHero.tsx`):
  - 白色小光点星球,hover 高亮放大(不变色)
  - 按 category(research/engineering)聚类布局
  - 同类连线明显、异类连线淡(星座网络)
  - 命中区随形变放大,解决悬停脱靶
  - OrbitControls 可拖动旋转 + 缓慢自转
  - 背景三层 Sparkles + Stars 营造深空体积感
  - 星云占下半屏,标题在上半屏不重叠
- [x] 星球数据结构(`planets.ts`,含 category 字段)
- [x] Chat 页面 + Mock 对话组件(打字机效果、抽象层)
- [x] About 占位页
- [x] `_source/` 目录(原始材料,已 gitignore,不入库)

### ⏳ 进行中 / 待办
- [ ] **填充真实内容**(当前最高优先级):
  - 星云 6 个星球全是占位文本,需替换为真实项目/技能
  - About 页文案
  - 材料放 `_source/`,由 Claude 读取后产出 `planets.ts` + Agent prompt
- [ ] 补建内容页:`/research`、`/experience`、`/publications`(可选)
- [ ] 接 Chat Agent 真实后端(Cloudflare Workers + DeepSeek)
- [ ] 本地 `3ccc92b`(gitignore)未 push 到远程

### ❌ 已知问题
- 本机 Chrome WebGL 不可用(NVIDIA 驱动 + llvmpipe 软件渲染冲突),**预览用 Edge**
- 星云星球内容为占位,无求职价值

---

## 工作流约定

- **每次改动都 commit**(用户明确要求),commit message 中文
- 原始材料放 `_source/`,含隐私不入库
- 内容总结由 Claude 直接做(跨文档关联 + 定制产出),不使用 self-distiller

---

## 关键设计决策记录

1. **星云风格 = 无人深空,非月之暗面**:做减法,神秘感来自留白和静默,不要花哨粒子拖尾。
2. **星球默认是白色小光点**:默认看不清,hover 才高亮显形——这是神秘感的核心。
3. **hover 高亮不变色**:保持白色,只放大变亮 + 淡彩色光晕作身份标识。
4. **category 聚类 + 连线分级**:同类聚拢、强连接;异类分散、弱连接。让星云有结构感。
5. **chatService 抽象层**:mock 与真实实现隔离,换后端不改 UI。
6. **项目仓库而非用户主页仓库**:仓库名 `zing.github.io` 与用户名 `Zing110` 大小写不匹配,作为项目仓库部署,代价是 URL 带子路径。

---

## 材料清单(待用户提供)

放 `_source/` 目录,Claude 读取后产出结构化内容。

### P0 核心
- 简历/CV
- 个人陈述/求职信/SoP(如有)
- 项目列表(名字/角色/技术/成果)

### P1 强烈推荐
- 代表项目详细报告(挑 2-3 个)
- 论文 PDF + 发表信息
- 成绩单(申博用)
- GitHub 用户名 / 想展示的 repo 链接

### P2 锦上添花
- 实习/工作成果总结(脱敏)
- 获奖/竞赛证明
- 技术博客/笔记(用于建模 Agent 风格)
- 推荐信(如愿意分享)

### 口头补充(直接告诉 Claude)
- 求职/申博方向偏好
- 性格/沟通风格(让 Agent 像你)
- 不愿公开的信息

---

## 时间线回顾

| 日期 | 事件 |
|------|------|
| 2026-07-07 | 项目启动,确定技术选型,初始化 Astro 骨架 |
| 2026-07-07 | 首次部署成功(静态 Hero 版) |
| 2026-07-07 | 星云交互 Hero 多轮迭代(月之暗面→无人深空风格),聚类+连线+命中区修复 |
| 2026-07-07 | 建立工作流约定(每次改动 commit)、`_source/` 目录、材料清单 |
| 待定 | 填充真实内容 → 补建内容页 → 接 Agent 后端 |
