import React, { useState, useEffect } from 'react';
import { Cpu, HardDrive, Server, ShieldCheck, Activity, RefreshCw, AlertTriangle, CheckCircle } from 'lucide-react';
import { SystemMetrics } from '../../types';
import { API_BASE_URL } from '../../services/api';

export const SystemMonitor: React.FC = () => {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [doctorData, setDoctorData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchMetrics = () => {
    fetch(`${API_BASE_URL}/system/metrics`)
      .then(res => res.json())
      .then(data => setMetrics(data))
      .catch(err => console.error('Metrics fetch error:', err));

    fetch(`${API_BASE_URL}/system/doctor`)
      .then(res => res.json())
      .then(data => setDoctorData(data))
      .catch(err => console.error('Doctor fetch error:', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 3000);
    return () => clearInterval(interval);
  }, []);

  const formatUptime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const hrs = Math.floor(mins / 60);
    return `${hrs}s ${mins % 60}d ${seconds % 60}sn`;
  };

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-4rem)] p-6 space-y-6 overflow-y-auto">
      {/* Top Controls Header */}
      <div className="flex items-center justify-between glass-panel p-6 rounded-2xl border-cyan-500/20">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Activity className="w-6 h-6 text-cyan-400" />
            Live System Health & Doctor Diagnostics
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Sunucu kaynakları, aktif süreçler ve AI Doctor otomatik denetim raporu.
          </p>
        </div>

        <button
          onClick={fetchMetrics}
          className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300 hover:text-cyan-400 hover:border-cyan-500/40 transition-all"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Yenile</span>
        </button>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* CPU Gauge */}
        <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span className="font-semibold flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-cyan-400" /> CPU Kullanımı
            </span>
            <span className="font-mono text-cyan-400 font-bold">{metrics?.cpu_percent || 0}%</span>
          </div>
          <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden p-0.5 border border-slate-800">
            <div
              className="bg-gradient-to-r from-cyan-400 to-blue-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${metrics?.cpu_percent || 0}%` }}
            />
          </div>
        </div>

        {/* RAM Gauge */}
        <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span className="font-semibold flex items-center gap-1.5">
              <Server className="w-4 h-4 text-purple-400" /> Bellek (RAM)
            </span>
            <span className="font-mono text-purple-400 font-bold">{metrics?.memory_percent || 0}%</span>
          </div>
          <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden p-0.5 border border-slate-800">
            <div
              className="bg-gradient-to-r from-purple-400 to-pink-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${metrics?.memory_percent || 0}%` }}
            />
          </div>
          <div className="text-[11px] text-slate-500 font-mono">
            {metrics?.memory_used_mb} MB / {metrics?.memory_total_mb} MB
          </div>
        </div>

        {/* Disk Gauge */}
        <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span className="font-semibold flex items-center gap-1.5">
              <HardDrive className="w-4 h-4 text-amber-400" /> Disk Alanı
            </span>
            <span className="font-mono text-amber-400 font-bold">{metrics?.disk_percent || 0}%</span>
          </div>
          <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden p-0.5 border border-slate-800">
            <div
              className="bg-gradient-to-r from-amber-400 to-orange-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${metrics?.disk_percent || 0}%` }}
            />
          </div>
          <div className="text-[11px] text-slate-500 font-mono">
            {metrics?.disk_used_gb} GB / {metrics?.disk_total_gb} GB
          </div>
        </div>

        {/* Uptime Info Card */}
        <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span className="font-semibold flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400" /> Çalışma Süresi
            </span>
            <span className="font-mono text-emerald-400 font-bold">Uptime</span>
          </div>
          <div className="text-lg font-bold text-slate-100 font-mono">
            {formatUptime(metrics?.uptime_seconds || 0)}
          </div>
          <div className="text-[11px] text-slate-500 font-mono">
            OS: {metrics?.os_platform} • Python {metrics?.python_version}
          </div>
        </div>
      </div>

      {/* AI Doctor Diagnostics & Top Processes */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: AI Doctor Report */}
        <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <h3 className="font-bold text-slate-100 text-sm flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              OpenPlexus Doctor Otonom Teşhis
            </h3>
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-950 text-emerald-400 border border-emerald-800">
              Skor: {doctorData?.score || 100}/100
            </span>
          </div>

          <div className="space-y-3">
            {doctorData?.diagnostics?.map((item: any, i: number) => (
              <div
                key={i}
                className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800/80 flex items-start gap-3 text-xs"
              >
                {item.level === 'WARNING' || item.level === 'CRITICAL' ? (
                  <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                ) : (
                  <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                )}
                <div>
                  <span className="font-semibold text-slate-200 block">{item.level || 'INFO'}</span>
                  <p className="text-slate-400 mt-0.5">{item.msg}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Top Active Processes Table */}
        <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
          <h3 className="font-bold text-slate-100 text-sm flex items-center gap-2 pb-3 border-b border-slate-800">
            <Server className="w-5 h-5 text-cyan-400" />
            En Çok Bellek Kullanan Süreçler
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-slate-800 text-slate-500">
                  <th className="pb-2">PID</th>
                  <th className="pb-2">Process</th>
                  <th className="pb-2">CPU %</th>
                  <th className="pb-2">RAM %</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50 text-slate-300">
                {metrics?.top_processes?.map((proc) => (
                  <tr key={proc.pid} className="hover:bg-slate-900/50">
                    <td className="py-2.5 text-cyan-400 font-semibold">{proc.pid}</td>
                    <td className="py-2.5 font-sans font-medium text-slate-200">{proc.name}</td>
                    <td className="py-2.5 text-purple-400">{proc.cpu_percent?.toFixed(1) || '0.0'}%</td>
                    <td className="py-2.5 text-emerald-400">{proc.memory_percent?.toFixed(1) || '0.0'}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
