import React, { useState } from 'react';
import { useAppStore } from '../../store/useAppStore';
import { Lock, User, KeyRound, AlertCircle, Sparkles, Terminal } from 'lucide-react';

export const Login: React.FC = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const loginStore = useAppStore((state) => state.login);

  const getBackendUrl = () => {
    const host = window.location.hostname;
    const protocol = window.location.protocol === 'https:' ? 'https:' : 'http:';
    return `${protocol}//${host}:8000`;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!username.trim() || !password.trim()) {
      setError('Kullanıcı adı ve şifre alanları boş bırakılamaz.');
      return;
    }

    setLoading(true);
    const backendUrl = getBackendUrl();
    const endpoint = isRegister ? `${backendUrl}/api/auth/register` : `${backendUrl}/api/auth/login`;

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Bir hata oluştu.');
      }

      loginStore(data.token, data.username);
      // Force reload page / reload sessions
      window.location.reload();
    } catch (err: any) {
      setError(err.message || 'Sunucuya bağlanırken bir hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex items-center justify-center min-h-screen overflow-hidden bg-slate-950 font-sans">
      {/* Premium Background Gradients & Glows */}
      <div className="absolute top-[-20%] left-[-20%] w-[60%] h-[60%] rounded-full bg-cyan-900/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-20%] w-[60%] h-[60%] rounded-full bg-blue-900/20 blur-[120px] pointer-events-none" />

      {/* Glassmorphism Card */}
      <div className="relative w-full max-w-md p-8 mx-4 border rounded-3xl bg-slate-900/40 backdrop-blur-xl border-slate-800/80 shadow-2xl">
        
        {/* Header Icon & Title */}
        <div className="flex flex-col items-center mb-8 text-center">
          <div className="flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 shadow-lg shadow-cyan-500/20 text-white mb-4 animate-pulse">
            <Terminal className="w-7 h-7" />
          </div>
          <h2 className="flex items-center gap-2 text-2xl font-bold tracking-tight text-white">
            OpenPlexus <Sparkles className="w-5 h-5 text-cyan-400" />
          </h2>
          <p className="mt-2 text-sm text-slate-400">
            {isRegister 
              ? 'Yeni bir hesap oluşturarak otonom sistem ajanını kullanmaya başlayın.' 
              : 'Gelişmiş AI SysAdmin & DevSecOps portalına giriş yapın.'}
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="flex items-start gap-3 p-4 mb-6 border rounded-xl bg-red-950/20 border-red-900/50 text-red-400 text-sm">
            <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Auth Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Kullanıcı Adı
            </label>
            <div className="relative">
              <User className="absolute w-5 h-5 -translate-y-1/2 left-3 top-1/2 text-slate-500" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="kullanici_adi"
                disabled={loading}
                className="w-full pl-11 pr-4 py-3 border rounded-xl bg-slate-950/50 border-slate-800 text-white placeholder-slate-600 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500 transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Şifre
            </label>
            <div className="relative">
              <KeyRound className="absolute w-5 h-5 -translate-y-1/2 left-3 top-1/2 text-slate-500" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                disabled={loading}
                className="w-full pl-11 pr-4 py-3 border rounded-xl bg-slate-950/50 border-slate-800 text-white placeholder-slate-600 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500 transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="flex items-center justify-center w-full gap-2 py-3 px-4 rounded-xl font-semibold text-white bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 active:from-cyan-600 active:to-blue-700 disabled:opacity-50 disabled:pointer-events-none transition-all shadow-lg shadow-cyan-500/25"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white rounded-full border-t-transparent animate-spin" />
            ) : isRegister ? (
              'Kayıt Ol ve Giriş Yap'
            ) : (
              'Giriş Yap'
            )}
          </button>
        </form>

        {/* Toggle Mode Link */}
        <div className="mt-8 text-center text-sm text-slate-400">
          {isRegister ? 'Zaten bir hesabınız var mı?' : 'Henüz bir hesabınız yok mu?'}
          <button
            onClick={() => {
              setIsRegister(!isRegister);
              setError('');
            }}
            disabled={loading}
            className="ml-1.5 font-semibold text-cyan-400 hover:text-cyan-300 hover:underline transition-all"
          >
            {isRegister ? 'Giriş Yap' : 'Kayıt Ol'}
          </button>
        </div>
      </div>
    </div>
  );
};
