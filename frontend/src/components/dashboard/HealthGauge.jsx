import React from 'react';
import { getHealthCategory } from '../../utils/constants';

export default function HealthGauge({ value = 0, size = 'md', label = 'Health Index', showLabel = true }) {
  const sizeMap = {
    sm: { width: 120, height: 70, strokeWidth: 8, fontSize: 18 },
    md: { width: 180, height: 100, strokeWidth: 10, fontSize: 24 },
    lg: { width: 240, height: 130, strokeWidth: 12, fontSize: 32 },
  };

  const { width, height, strokeWidth, fontSize } = sizeMap[size] || sizeMap.md;
  const radius = (width - strokeWidth) / 2;
  const cx = width / 2;
  const cy = height - 10;
  const arcLength = Math.PI * radius;
  const progress = (value / 100) * arcLength;
  const category = getHealthCategory(value);

  return (
    <div className="flex flex-col items-center">
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        <defs>
          <linearGradient id={`gauge-${value}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ef4444" />
            <stop offset="25%" stopColor="#f97316" />
            <stop offset="50%" stopColor="#eab308" />
            <stop offset="75%" stopColor="#22c55e" />
            <stop offset="100%" stopColor="#16a34a" />
          </linearGradient>
        </defs>
        <path
          d={`M ${strokeWidth / 2} ${cy} A ${radius} ${radius} 0 0 1 ${width - strokeWidth / 2} ${cy}`}
          fill="none"
          stroke="#e5e7eb"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
        />
        <path
          d={`M ${strokeWidth / 2} ${cy} A ${radius} ${radius} 0 0 1 ${width - strokeWidth / 2} ${cy}`}
          fill="none"
          stroke={`url(#gauge-${value})`}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={`${progress} ${arcLength - progress}`}
          strokeDashoffset={0}
          style={{ transition: 'stroke-dasharray 1s ease-out' }}
        />
        <text
          x={cx}
          y={cy - 8}
          textAnchor="middle"
          fontSize={fontSize}
          fontWeight="bold"
          fill={category.color}
          fontFamily="Inter, system-ui, sans-serif"
        >
          {Math.round(value)}
        </text>
        <text
          x={cx}
          y={cy + 18}
          textAnchor="middle"
          fontSize={11}
          fill="#6b7280"
          fontFamily="Inter, system-ui, sans-serif"
        >
          {category.label}
        </text>
      </svg>
      {showLabel && (
        <p className="text-sm font-medium text-gray-600 mt-1">{label}</p>
      )}
    </div>
  );
}
