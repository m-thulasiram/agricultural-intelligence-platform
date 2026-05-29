import React from 'react';
import {
  BarChart as RechartsBarChart,
  Bar,
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
          <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.fill || entry.color }} />
          <span className="text-gray-600">{entry.name}:</span>
          <span className="font-semibold text-gray-900">
            {typeof entry.value === 'number' ? entry.value.toFixed(2) : entry.value}
          </span>
        </div>
      ))}
    </div>
  );
};

export default function BarChart({
  data = [],
  bars = [],
  xKey = 'name',
  height = 300,
  showGrid = true,
  showLegend = true,
  showTooltip = true,
  stacked = false,
  horizontal = false,
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
      <RechartsBarChart
        data={data}
        margin={{ top: 5, right: 10, left: 0, bottom: 5 }}
        layout={horizontal ? 'vertical' : 'horizontal'}
      >
        {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />}
        <XAxis
          type={horizontal ? 'number' : 'category'}
          dataKey={horizontal ? undefined : xKey}
          tick={{ fontSize: 12, fill: '#9ca3af' }}
          tickLine={false}
          axisLine={{ stroke: '#e5e7eb' }}
        />
        <YAxis
          type={horizontal ? 'category' : 'number'}
          dataKey={horizontal ? xKey : undefined}
          tick={{ fontSize: 12, fill: '#9ca3af' }}
          tickLine={false}
          axisLine={{ stroke: '#e5e7eb' }}
        />
        {showTooltip && <Tooltip content={<CustomTooltip />} />}
        {showLegend && (
          <Legend
            verticalAlign="bottom"
            iconType="rect"
            iconSize={8}
            formatter={(value) => <span className="text-xs text-gray-600">{value}</span>}
          />
        )}
        {bars.map((bar, idx) => (
          <Bar
            key={bar.dataKey || idx}
            dataKey={bar.dataKey}
            name={bar.name || bar.dataKey}
            fill={colors[idx % colors.length]}
            radius={[4, 4, 0, 0]}
            stackId={stacked ? 'stack' : undefined}
          />
        ))}
      </RechartsBarChart>
    </ResponsiveContainer>
  );
}
