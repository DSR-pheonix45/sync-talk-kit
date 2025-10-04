import { useRef, useEffect } from 'react';

export default function Squares({
  direction = 'right',
  speed = 1,
  borderColor = '#00FFD1',
  squareSize = 40,
  hoverFillColor = '#0B1221',
}: {
  direction?: 'right' | 'left' | 'down' | 'up' | 'diagonal';
  speed?: number;
  borderColor?: string;
  squareSize?: number;
  hoverFillColor?: string;
}) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const requestRef = useRef<number | null>(null);
  const numSquaresX = useRef(0);
  const numSquaresY = useRef(0);
  const gridOffset = useRef({ x: 0, y: 0 });
  const hoveredSquareRef = useRef<{ x: number; y: number } | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const resizeCanvas = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      numSquaresX.current = Math.ceil(canvas.width / squareSize) + 1;
      numSquaresY.current = Math.ceil(canvas.height / squareSize) + 1;
    };

    const onMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const x = Math.floor((e.clientX - rect.left + gridOffset.current.x) / squareSize);
      const y = Math.floor((e.clientY - rect.top + gridOffset.current.y) / squareSize);
      hoveredSquareRef.current = { x, y };
    };

    window.addEventListener('resize', resizeCanvas);
    canvas.addEventListener('mousemove', onMouseMove);
    resizeCanvas();

    const drawGrid = () => {
      if (!ctx) return;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const startX = Math.floor(gridOffset.current.x / squareSize) * squareSize;
      const startY = Math.floor(gridOffset.current.y / squareSize) * squareSize;

      for (let x = startX; x < canvas.width + squareSize; x += squareSize) {
        for (let y = startY; y < canvas.height + squareSize; y += squareSize) {
          const squareX = x - (gridOffset.current.x % squareSize);
          const squareY = y - (gridOffset.current.y % squareSize);

          if (
            hoveredSquareRef.current &&
            Math.floor((x - startX) / squareSize) === hoveredSquareRef.current.x &&
            Math.floor((y - startY) / squareSize) === hoveredSquareRef.current.y
          ) {
            ctx.fillStyle = hoverFillColor;
            ctx.fillRect(squareX, squareY, squareSize, squareSize);
          }

          ctx.strokeStyle = borderColor;
          ctx.lineWidth = 1;
          ctx.strokeRect(squareX, squareY, squareSize, squareSize);
        }
      }
    };

    const animate = () => {
      const delta = speed * 0.5;
      switch (direction) {
        case 'right':
          gridOffset.current.x += delta;
          break;
        case 'left':
          gridOffset.current.x -= delta;
          break;
        case 'down':
          gridOffset.current.y += delta;
          break;
        case 'up':
          gridOffset.current.y -= delta;
          break;
        case 'diagonal':
          gridOffset.current.x += delta;
          gridOffset.current.y += delta;
          break;
      }
      drawGrid();
      requestRef.current = requestAnimationFrame(animate);
    };

    requestRef.current = requestAnimationFrame(animate);

    return () => {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
      window.removeEventListener('resize', resizeCanvas);
      canvas.removeEventListener('mousemove', onMouseMove);
    };
  }, [borderColor, direction, hoverFillColor, speed, squareSize]);

  return <canvas ref={canvasRef} className="w-full h-full" />;
}
