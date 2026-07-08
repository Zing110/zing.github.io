import { useState } from 'react';
import { planets } from '../data/planets';
import Nebula from './Nebula';

export default function NebulaHero() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selected = planets.find((p) => p.id === selectedId);

  return (
    <>
      <div className="relative w-full h-screen overflow-hidden">
        {/* 星云层:占下半部分,不遮标题 */}
        <div className="absolute left-0 right-0 bottom-0 h-[60%] z-0">
          <Nebula selectedId={selectedId} onSelectPlanet={setSelectedId} />
        </div>

        {/* 标题:占上半部分,文字浮在星云上方 */}
        <div
          className="absolute left-0 right-0 top-0 h-[45%] z-10 flex flex-col items-center justify-end pb-8 pointer-events-none transition-opacity duration-500"
          style={{ opacity: selected ? 0 : 1 }}
        >
          <div className="container text-center fade-in-up">
            <p className="text-sm text-zinc-500 mb-6 tracking-widest uppercase">
              Researcher · Engineer
            </p>
            <h1 className="text-5xl sm:text-7xl font-bold mb-6 tracking-tight">
              <span className="gradient-text">你的名字</span>
            </h1>
            <p className="text-lg sm:text-xl text-zinc-400 max-w-2xl mx-auto">
              研究方向 / 一句话定位
            </p>
          </div>
        </div>

        {/* 底部提示 */}
        {!selected && (
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 text-xs text-zinc-600 pointer-events-none">
            鼠标悬停减速 · 点击探索
          </div>
        )}

        {/* 详情卡:右侧悬浮,与飞到镜头前的星球并排 */}
        {selected && (
          <div
            key={selected.id}
            className="absolute right-6 sm:right-12 top-1/2 -translate-y-1/2 z-20 w-[min(90vw,360px)] fade-in-up"
          >
            <div className="glass rounded-2xl p-7">
              <div className="flex items-center gap-3 mb-4">
                <span
                  className="w-3 h-3 rounded-full"
                  style={{ background: selected.color, boxShadow: `0 0 12px ${selected.color}` }}
                />
                <span className="text-xs text-zinc-500 uppercase tracking-wider">
                  {selected.type === 'project' ? '项目' : '技能'}
                </span>
              </div>

              <h3 className="text-2xl font-semibold mb-3 text-white">{selected.name}</h3>
              <p className="text-sm text-zinc-400 mb-4">{selected.summary}</p>
              <p className="text-sm text-zinc-300 leading-relaxed mb-5">{selected.detail}</p>

              <div className="flex flex-wrap gap-2 mb-6">
                {selected.tags.map((tag) => (
                  <span
                    key={tag}
                    className="text-xs px-2.5 py-1 rounded-full bg-white/5 border border-white/10 text-zinc-400"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              <div className="flex items-center justify-between">
                {selected.link ? (
                  <a
                    href={selected.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-zinc-300 hover:text-white transition-colors"
                  >
                    访问 →
                  </a>
                ) : (
                  <span />
                )}
                <button
                  onClick={() => setSelectedId(null)}
                  className="text-sm text-zinc-500 hover:text-white transition-colors"
                >
                  返回 ←
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
