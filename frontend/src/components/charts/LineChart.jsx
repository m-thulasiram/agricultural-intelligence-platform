import React from 'react';
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-white shadow-lg rounded-lg border border-gray-200 p-3">
      <p className="text-xs font-medium text-gray-500 mb-2">{label}</p>
      {payload.map((entry, idx) => (
        <div key={idx} className="flex items-center gap-2 text-sm">
          <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }} />
          <span className="text-gray-600">{entry.name}:</span>
          <span className="font-semibold text-gray-900">
            {typeof entry.value === 'number' ? entry.value.toFixed(2) : entry.value}
          </span>
        </div>
      ))}
    </div>
  );
};

export default function LineChart({
  data = [],
  lines = [],
  xKey = 'name',
  height = 300,
  showGrid = true,
  showLegend = true,
  showTooltip = true,
  yAxisLabel,
  xAxisLabel,
  colors = ['#22c55e', '#3b82f6', '#eab308', '#ef4444', '#8b5cf6'],
}) {
  if (!data.length) {
    return (
      <div className="flex items-center justify-center h-full min-h-[200px] text-gray-400 text-sm">
        No data available
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsLineChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
        <defs>
          {lines.map((line, idx) => (
            <linearGradient key={line.dataKey || idx} id={`lineGrad-${idx}`} x1="0" y1="0" x2="1" y2="0">
              <stop offset="5%" stopColor={colors[idx % colors.length]} stopOpacity={0.8} />
              <stop offset="95%" stopColor={colors[idx % colors.length]} stopOpacity={0.2} />
            </linearGradient>
          ))}
        </defs>
        {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />}
        <XAxis
          dataKey={xKey}
          tick={{ fontSize: 12, fill: '#9ca3af' }}
          tickLine={false}
          axisLine={{ stroke: '#e5e7eb' }}
          label={xAxisLabel ? { value: xAxisLabel, position: 'insideBottom', offset: -5, fill: '#9ca3af', fontSize: 12 } : undefined}
        />
        <YAxis
          tick={{ fontSize: 12, fill: '#9ca3af' }}
          tickLine={false}
          axisLine={{ stroke: '#e5e7eb' }}
          label={yAxisLabel ? { value: yAxisLabel, angle: -90, position: 'insideLeft', fill: '#9ca3af', fontSize: 12 } : undefined}
        />
        {showTooltip && <Tooltip content={<CustomTooltip />} />}
        {showLegend && (
          <Legend
            verticalAlign="bottom"
            iconType="circle"
            iconSize={8}
            formatter={(value) => <span className="text-xs text-gray-600">{value}</span>}
          />
        )}
        {lines.map((line, idx) => (
          <Line
            key={line.dataKey || idx}
            type="monotone"
            dataKey={line.dataKey}
            name={line.name || line.dataKey}
            stroke={colors[idx % colors.length]}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 5, strokeWidth: 0, fill: colors[idx % colors.length] }}
          />
        ))}
      </RechartsLineChart>
    </ResponsiveContainer>
  );
}
