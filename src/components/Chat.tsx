import { useState, useRef, useEffect } from 'react';
import { sendChatMessage, type ChatMessage } from '../lib/chatService';

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: '你好!我是主人的 AI 助手。问我关于研究、项目或经历的问题吧。',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // 自动滚动到底部
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg: ChatMessage = { role: 'user', content: text };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await sendChatMessage(messages, text);
      setMessages([...newMessages, { role: 'assistant', content: res.message }]);
    } catch {
      setMessages([
        ...newMessages,
        { role: 'assistant', content: '抱歉,出了点问题,请稍后再试。' },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="glass rounded-2xl overflow-hidden flex flex-col" style={{ height: '60vh', maxHeight: '600px' }}>
      {/* 消息列表 */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'text-white'
                  : 'bg-white/5 text-zinc-200 border border-white/10'
              }`}
              style={
                msg.role === 'user'
                  ? { background: 'linear-gradient(135deg, var(--accent-start), var(--accent-end))' }
                  : undefined
              }
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white/5 border border-white/10 px-4 py-3 rounded-2xl">
              <span className="inline-flex gap-1">
                <span className="w-2 h-2 rounded-full bg-zinc-500 animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 rounded-full bg-zinc-500 animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 rounded-full bg-zinc-500 animate-bounce" style={{ animationDelay: '300ms' }} />
              </span>
            </div>
          </div>
        )}
      </div>

      {/* 输入区 */}
      <div className="border-t border-white/10 p-4 flex items-center gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入问题..."
          disabled={loading}
          className="flex-1 bg-transparent text-white placeholder-zinc-600 outline-none text-sm px-2"
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="px-4 py-2 rounded-full text-sm font-medium text-white transition-opacity disabled:opacity-40"
          style={{ background: 'linear-gradient(135deg, var(--accent-start), var(--accent-end))' }}
        >
          发送
        </button>
      </div>
    </div>
  );
}
