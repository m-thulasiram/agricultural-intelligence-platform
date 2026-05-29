import React from 'react';
import {
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const entry = payload[0];
  return (
    <div className="bg-white shadow-lg rounded-lg border border-gray-200 p-3">
      <div className="flex items-center gap-2 text-sm">
        <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.payload.fill || entry.color }} />
        <span className="text-gray-600">{entry.name}:</span>
        <span className="font-semibold text-gray-900">
          {typeof entry.value === 'number' ? entry.value.toFixed(1) : entry.value}%
        </span>
      </div>
    </div>
  );
};

const RADIAN = Math.PI / 180;

const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 1.4;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  if (percent < 0.05) return null;
  return (
    <text
      x={x}
      y={y}
      fill="#374151"
      textAnchor={x > cx ? 'start' : 'end'}
      dominantBaseline="central"
      fontSize={11}
      fontWeight={500}
    >
      {(percent * 100).toFixed(0)}%
    </text>
  );
};

export default function PieChart({
  data = [],
  dataKey = 'value',
  nameKey = 'name',
  height = 300,
  showLegend = true,
  showTooltip = true,
  showLabels = false,
  innerRadius = 0,
  outerRadius = 100,
  colors = ['#22c55e', '#3b82f6', '#eab308', '#ef4444', '#8b5cf6', '#06b6d4', '#f97316', '#6366f1'],
}) {
  if (!data.length) {
    return (
      <div className="flex items-center justify-center h-full min-h-[200px] text-gray-400 text-sm">
        No data available
      </div>
    );
  }

  const total = data.reduce((sum, entry) => sum + (entry[dataKey] || 0), 0);
  const dataWithPercent = data.map((entry) => ({
    ...entry,
    percentage: total > 0 ? ((entry[dataKey] / total) * 100).toFixed(1) : 0,
  }));

  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsPieChart>
        <Pie
          data={dataWithPercent}
          dataKey={dataKey}
          nameKey={nameKey}
          cx="50%"
          cy="50%"
          innerRadius={innerRadius}
          outerRadius={outerRadius}
          label={showLabels ? CustomLabel : undefined}
          paddingAngle={2}
        >
          {dataWithPercent.map((entry, idx) => (
            <Cell
              key={`cell-${idx}`}
              fill={entry.color || colors[idx % colors.length]}
              stroke="transparent"
            />
          ))}
        </Pie>
        {showTooltip && <Tooltip content={<CustomTooltip />} />}
        {showLegend && (
          <Legend
            verticalAlign="bottom"
            iconType="circle"
            iconSize={8}
            formatter={(value) => <span className="text-xs text-gray-600">{value}</span>}
          />
        )}
      </RechartsPieChart>
    </ResponsiveContainer>
  );
}
