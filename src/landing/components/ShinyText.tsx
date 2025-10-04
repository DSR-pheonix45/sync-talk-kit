import { useEffect, useRef } from 'react';

export default function ShinyText({ text, disabled = false, speed = 3, className = '' }: { text: string; disabled?: boolean; speed?: number; className?: string; }) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (disabled) return;
    const container = containerRef.current;
    if (!container) return;

    const handleMouseMove = (e: MouseEvent) => {
      const { left, top, width, height } = container.getBoundingClientRect();
      const x = (e.clientX - left) / width;
      const y = (e.clientY - top) / height;
      container.style.setProperty('--mouse-x', x.toFixed(2));
      container.style.setProperty('--mouse-y', y.toFixed(2));
    };

    container.addEventListener('mousemove', handleMouseMove);
    return () => container.removeEventListener('mousemove', handleMouseMove);
  }, [disabled]);

  return (
    <div
      ref={containerRef}
      className={`relative overflow-hidden ${className}`}
      style={{ ['--speed' as any]: `${speed}s` }}
    >
      <div className="relative z-10">{text}</div>
      {!disabled && (
        <div className="absolute inset-0 pointer-events-none transition-opacity">
          <div
            className="absolute inset-0 bg-gradient-radial from-[#00FFD1]/20 to-transparent opacity-0 group-hover:opacity-100 blur-xl"
            style={{
              transform: 'translate(calc(var(--mouse-x, 0.5) * 100%), calc(var(--mouse-y, 0.5) * 100%))',
              transition: `transform var(--speed) ease`,
            }}
          />
        </div>
      )}
    </div>
  );
}
