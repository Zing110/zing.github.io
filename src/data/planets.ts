// ===== 星云星球数据 =====
// 每个星球代表一个项目或技能。后期改内容只动这个文件。
// 接入真实内容时,把 name/summary/detail/tags 换成你的真实信息。

export interface Planet {
  id: string;
  name: string;
  type: 'project' | 'skill';
  // 类别:相似类别会在星云中聚拢,且连线更明显
  category: 'research' | 'engineering';
  // 轨道半径(相对单位,决定星球离中心的距离)
  orbitRadius: number;
  // 公转速度(弧度/帧),负值 = 反向公转
  orbitSpeed: number;
  // 初始公转相位(弧度),决定起始位置
  initialAngle: number;
  // 星球半径(相对单位,决定大小)
  size: number;
  // 颜色(用于星球材质和光晕)
  color: string;
  // 详情卡片内容
  summary: string;
  detail: string;
  tags: string[];
  // 外链(可选)
  link?: string;
}

export const planets: Planet[] = [
  {
    id: 'ml-research',
    name: 'ML 研究',
    type: 'project',
    category: 'research',
    orbitRadius: 3.2,
    orbitSpeed: 0.0015,
    initialAngle: 0,
    size: 0.45,
    color: '#6366f1',
    summary: '机器学习研究方向',
    detail: '这里写该项目的详细描述:做了什么、用了什么方法、取得了什么成果。占位文本,接入真实内容时替换。',
    tags: ['PyTorch', 'NLP', '研究'],
  },
  {
    id: 'web-dev',
    name: 'Web 开发',
    type: 'skill',
    category: 'engineering',
    orbitRadius: 2.4,
    orbitSpeed: -0.002,
    initialAngle: 1.2,
    size: 0.35,
    color: '#818cf8',
    summary: '全栈 Web 开发能力',
    detail: '掌握前端框架(React/Vue)和后端开发,能独立完成项目。占位文本。',
    tags: ['React', 'Node.js', 'TypeScript'],
  },
  {
    id: 'system-design',
    name: '系统设计',
    type: 'skill',
    category: 'engineering',
    orbitRadius: 4.0,
    orbitSpeed: 0.001,
    initialAngle: 2.5,
    size: 0.4,
    color: '#3b82f6',
    summary: '分布式系统设计',
    detail: '具备分布式系统设计与优化经验。占位文本。',
    tags: ['架构', '分布式', '性能优化'],
  },
  {
    id: 'paper-1',
    name: '论文 A',
    type: 'project',
    category: 'research',
    orbitRadius: 3.6,
    orbitSpeed: -0.0018,
    initialAngle: 3.8,
    size: 0.38,
    color: '#7c3aed',
    summary: '发表的学术论文',
    detail: '论文标题、会议/期刊、贡献点。占位文本。',
    tags: ['论文', '顶会'],
  },
  {
    id: 'internship',
    name: '实习经历',
    type: 'project',
    category: 'engineering',
    orbitRadius: 2.8,
    orbitSpeed: 0.0022,
    initialAngle: 5.0,
    size: 0.42,
    color: '#0ea5e9',
    summary: '某公司实习',
    detail: '实习期间负责的工作和成果。占位文本。',
    tags: ['实习', '工程'],
  },
  {
    id: 'open-source',
    name: '开源项目',
    type: 'project',
    category: 'engineering',
    orbitRadius: 4.4,
    orbitSpeed: -0.0012,
    initialAngle: 0.6,
    size: 0.36,
    color: '#4f46e5',
    summary: '个人开源项目',
    detail: 'GitHub 上的个人项目,获得的 star 数等。占位文本。',
    tags: ['开源', 'GitHub'],
    link: 'https://github.com/Zing110',
  },
];
