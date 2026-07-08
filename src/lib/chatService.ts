// ===== Chat 服务抽象层 =====
// 这是关键工程点:所有对话逻辑都通过这个模块。
// 当前是 mock 实现,未来接入真实 API(Cloudflare Workers + DeepSeek)
// 时,只需替换 sendChatMessage 的实现,UI 不用改。

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  message: string;
  // 未来可扩展: citations, sources 等
}

/**
 * 发送对话消息。
 * - 当前:mock 实现,关键词匹配 + 预设回答 + 模拟延迟
 * - 未来:替换为 fetch Cloudflare Worker URL
 */
export async function sendChatMessage(
  history: ChatMessage[],
  userMessage: string
): Promise<ChatResponse> {
  // === Mock 实现 ===
  await mockDelay(600 + Math.random() * 400);

  const reply = mockReply(userMessage);
  return { message: reply };

  // === 未来真实实现(注释保留,接入时取消注释) ===
  // const res = await fetch('https://your-worker.workers.dev/chat', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ history, message: userMessage }),
  // });
  // if (!res.ok) throw new Error('请求失败');
  // const data = await res.json();
  // return { message: data.reply };
}

// ===== Mock 内部实现 =====
function mockDelay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function mockReply(message: string): string {
  const lower = message.toLowerCase();

  if (message.includes('你好') || message.includes('hello') || lower.includes('hi')) {
    return '你好!我是这个主页主人的 AI 助手。你可以问我关于他的研究方向、项目经历或学术背景。';
  }

  if (message.includes('研究') || message.includes('方向')) {
    return '主人目前的研究方向包括 [待填充]。更多细节可以在"研究"页面查看。';
  }

  if (message.includes('项目') || message.includes('经历')) {
    return '主人参与过若干研究项目,详见"经历"页面。这里先 mock 一下,接入真实模型后我会给出详细回答。';
  }

  if (message.includes('论文') || message.includes('paper') || message.includes('发表')) {
    return '论文列表正在整理中,敬请期待。';
  }

  if (message.includes('联系方式') || message.includes('邮箱') || message.includes('联系')) {
    return '你可以通过页面底部的邮箱或 GitHub 联系主人。';
  }

  return '这是一个很好的问题!(mock 回复)接入真实模型后,我会基于主人的个人资料给出更详细的回答。你可以问我研究方向、项目经历、论文等。';
}
