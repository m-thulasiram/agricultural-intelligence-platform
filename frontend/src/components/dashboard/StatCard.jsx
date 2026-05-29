import React from 'react';

export default function StatCard({ icon, label, value, trend, color = 'primary', subtitle, loading }) {
  const colorMap = {
    primary: { bg: 'bg-primary-50', text: 'text-primary-600', icon: 'text-primary-600' },
    green: { bg: 'bg-green-50', text: 'text-green-600', icon: 'text-green-600' },
    yellow: { bg: 'bg-yellow-50', text: 'text-yellow-600', icon: 'text-yellow-600' },
    red: { bg: 'bg-red-50', text: 'text-red-600', icon: 'text-red-600' },
    blue: { bg: 'bg-blue-50', text: 'text-blue-600', icon: 'text-blue-600' },
    indigo: { bg: 'bg-indigo-50', text: 'text-indigo-600', icon: 'text-indigo-600' },
  };

  const colors = colorMap[color] || colorMap.primary;

  if (loading) {
    return (
      <div className="card animate-pulse">
        <div className="flex items-start justify-between">
          <div className="space-y-3 flex-1">
            <div className="h-4 bg-gray-200 rounded w-24" />
            <div className="h-8 bg-gray-200 rounded w-32" />
            <div className="h-3 bg-gray-200 rounded w-20" />
          </div>
          <div className="w-12 h-12 bg-gray-200 rounded-xl" />
        </div>
      </div>
    );
  }

  const trendColor = trend > 0 ? 'text-green-600' : trend < 0 ? 'text-red-600' : 'text-gray-500';
  const TrendIcon = trend > 0
    ? () => (
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
      )
    : trend < 0
    ? () => (
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      )
    : null;

  return (
    <div className="card hover:shadow-md transition-shadow duration-200 animate-fade-in">
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-sm font-medium text-gray-500">{label}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {(trend !== undefined || subtitle) && (
            <div className="flex items-center gap-2">
              {trend !== undefined && (
                <span className={`inline-flex items-center gap-0.5 text-xs font-medium ${trendColor}`}>
                  {TrendIcon && <TrendIcon />}
                  {Math.abs(trend)}%
                </span>
              )}
              {subtitle && <span className="text-xs text-gray-400">{subtitle}</span>}
            </div>
          )}
        </div>
        {icon && (
          <div className={`w-12 h-12 ${colors.bg} rounded-xl flex items-center justify-center flex-shrink-0`}>
            <svg className={`w-6 h-6 ${colors.icon}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={icon} />
            </svg>
          </div>
        )}
      </div>
    </div>
  );
}
