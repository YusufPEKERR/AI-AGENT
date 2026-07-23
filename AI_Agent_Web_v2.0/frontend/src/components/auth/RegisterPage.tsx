import React, { useState, useRef, useEffect } from 'react';
import { useAuthStore } from '../../store/useAuthStore';

interface RegisterPageProps {
  onSwitchToLogin: () => void;
}

export const RegisterPage: React.FC<RegisterPageProps> = ({ onSwitchToLogin }) => {
  const [username, setUsername]             = useState('');
  const [password, setPassword]             = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword]     = useState(false);
  const [showConfirm, setShowConfirm]       = useState(false);
  const [error, setError]                   = useState('');
  const [isLoading, setIsLoading]           = useState(false);
  const [shake, setShake]                   = useState(false);
  const { register } = useAuthStore();
  const usernameRef = useRef<HTMLInputElement>(null);

  useEffect(() => { usernameRef.current?.focus(); }, []);

  const triggerError = (msg: string) => {
    setError(msg);
    setShake(true);
    setTimeout(() => setShake(false), 600);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      triggerError('Şifreler eşleşmiyor.');
      return;
    }

    setIsLoading(true);
    await new Promise((r) => setTimeout(r, 700));

    const result = register(username.trim(), password);
    setIsLoading(false);

    if (!result.success) {
      triggerError(result.error || 'Kayıt başarısız.');
    }
    // success → useAuthStore isAuthenticated=true → App otomatik ana sayfaya geçer
  };

  const inputStyle = (hasError: boolean): React.CSSProperties => ({
    width: '100%',
    boxSizing: 'border-box',
    padding: '12px 14px 12px 42px',
    background: 'rgba(15,23,42,0.8)',
    border: `1px solid ${hasError ? 'rgba(239,68,68,0.5)' : 'rgba(255,255,255,0.08)'}`,
    borderRadius: '12px',
    color: '#f1f5f9',
    fontSize: '14px',
    outline: 'none',
    transition: 'all 0.2s',
  });

  const iconWrap: React.CSSProperties = {
    position: 'absolute',
    left: '14px',
    top: '50%',
    transform: 'translateY(-50%)',
    color: '#475569',
    pointerEvents: 'none',
  };

  const eyeBtn: React.CSSProperties = {
    position: 'absolute',
    right: '14px',
    top: '50%',
    transform: 'translateY(-50%)',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    color: '#475569',
    padding: '2px',
    display: 'flex',
    alignItems: 'center',
    transition: 'color 0.2s',
  };

  const formReady = username && password && confirmPassword && !isLoading;

  return (
    <div style={{
      minHeight: '100vh', width: '100vw',
      background: 'radial-gradient(ellipse at 50% 0%, rgba(168,85,247,0.12) 0%, #090d16 60%)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontFamily: "'Inter', system-ui, sans-serif",
      position: 'relative', overflow: 'hidden',
    }}>
      {/* Arkaplan parçacıkları */}
      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', pointerEvents: 'none' }}>
        {[...Array(20)].map((_, i) => (
          <div key={i} style={{
            position: 'absolute',
            width: `${Math.random() * 3 + 1}px`,
            height: `${Math.random() * 3 + 1}px`,
            background: i % 2 === 0 ? 'rgba(168,85,247,0.4)' : 'rgba(6,182,212,0.4)',
            borderRadius: '50%',
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animation: `float ${Math.random() * 8 + 6}s ease-in-out infinite`,
            animationDelay: `${Math.random() * 5}s`,
          }} />
        ))}
      </div>

      {/* Grid */}
      <div style={{
        position: 'absolute', inset: 0,
        backgroundImage: 'linear-gradient(rgba(168,85,247,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(168,85,247,0.03) 1px, transparent 1px)',
        backgroundSize: '60px 60px', pointerEvents: 'none',
      }} />

      {/* Kart */}
      <div style={{
        position: 'relative', width: '100%', maxWidth: '420px', margin: '0 16px',
        animation: shake ? 'shake 0.5s ease-in-out' : undefined,
      }}>
        {/* Üst glow */}
        <div style={{
          position: 'absolute', top: '-60px', left: '50%', transform: 'translateX(-50%)',
          width: '200px', height: '60px',
          background: 'radial-gradient(ellipse, rgba(168,85,247,0.35) 0%, transparent 70%)',
          filter: 'blur(10px)', pointerEvents: 'none',
        }} />

        <div style={{
          background: 'rgba(15,23,42,0.75)',
          backdropFilter: 'blur(24px)', WebkitBackdropFilter: 'blur(24px)',
          border: '1px solid rgba(168,85,247,0.2)', borderRadius: '20px',
          padding: '48px 40px',
          boxShadow: '0 0 0 1px rgba(255,255,255,0.05), 0 20px 60px rgba(0,0,0,0.5), 0 0 80px rgba(168,85,247,0.08)',
        }}>
          {/* Başlık */}
          <div style={{ textAlign: 'center', marginBottom: '36px' }}>
            <div style={{
              width: '72px', height: '72px',
              background: 'linear-gradient(135deg, rgba(168,85,247,0.2), rgba(6,182,212,0.2))',
              border: '1px solid rgba(168,85,247,0.35)', borderRadius: '18px',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              margin: '0 auto 20px',
              boxShadow: '0 0 30px rgba(168,85,247,0.2)',
            }}>
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="8" r="4" stroke="url(#rg1)" strokeWidth="1.5" />
                <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="url(#rg2)" strokeWidth="1.5" strokeLinecap="round" />
                <path d="M19 8v6M16 11h6" stroke="url(#rg3)" strokeWidth="1.5" strokeLinecap="round" />
                <defs>
                  <linearGradient id="rg1" x1="8" y1="4" x2="16" y2="12" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#a855f7" /><stop offset="1" stopColor="#06b6d4" />
                  </linearGradient>
                  <linearGradient id="rg2" x1="4" y1="20" x2="20" y2="20" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#a855f7" /><stop offset="1" stopColor="#06b6d4" />
                  </linearGradient>
                  <linearGradient id="rg3" x1="16" y1="8" x2="22" y2="14" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#a855f7" /><stop offset="1" stopColor="#06b6d4" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <h1 style={{
              margin: '0 0 6px', fontSize: '26px', fontWeight: '700', letterSpacing: '-0.5px',
              background: 'linear-gradient(135deg, #a855f7 0%, #38bdf8 100%)',
              WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            }}>
              Hesap Oluştur
            </h1>
            <p style={{ margin: 0, fontSize: '13px', color: 'rgba(148,163,184,0.8)' }}>
              OpenPlexus AI'a katılın
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} noValidate>
            {/* Kullanıcı Adı */}
            <div style={{ marginBottom: '16px' }}>
              <label htmlFor="reg-username" style={{ display: 'block', fontSize: '13px', color: '#94a3b8', marginBottom: '7px', fontWeight: '500' }}>
                Kullanıcı Adı
              </label>
              <div style={{ position: 'relative' }}>
                <span style={iconWrap}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" />
                  </svg>
                </span>
                <input
                  id="reg-username" ref={usernameRef} type="text"
                  value={username} onChange={(e) => { setUsername(e.target.value); setError(''); }}
                  placeholder="Kullanıcı adı seçin" autoComplete="username" required
                  style={inputStyle(!!error)}
                  onFocus={(e) => { e.target.style.borderColor = 'rgba(168,85,247,0.5)'; e.target.style.boxShadow = '0 0 0 3px rgba(168,85,247,0.1)'; }}
                  onBlur={(e) => { e.target.style.borderColor = error ? 'rgba(239,68,68,0.5)' : 'rgba(255,255,255,0.08)'; e.target.style.boxShadow = 'none'; }}
                />
              </div>
            </div>

            {/* Şifre */}
            <div style={{ marginBottom: '16px' }}>
              <label htmlFor="reg-password" style={{ display: 'block', fontSize: '13px', color: '#94a3b8', marginBottom: '7px', fontWeight: '500' }}>
                Şifre
              </label>
              <div style={{ position: 'relative' }}>
                <span style={iconWrap}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" />
                  </svg>
                </span>
                <input
                  id="reg-password" type={showPassword ? 'text' : 'password'}
                  value={password} onChange={(e) => { setPassword(e.target.value); setError(''); }}
                  placeholder="Şifre belirleyin (min. 4 karakter)" autoComplete="new-password" required
                  style={{ ...inputStyle(!!error), paddingRight: '42px' }}
                  onFocus={(e) => { e.target.style.borderColor = 'rgba(168,85,247,0.5)'; e.target.style.boxShadow = '0 0 0 3px rgba(168,85,247,0.1)'; }}
                  onBlur={(e) => { e.target.style.borderColor = error ? 'rgba(239,68,68,0.5)' : 'rgba(255,255,255,0.08)'; e.target.style.boxShadow = 'none'; }}
                />
                <button type="button" id="reg-toggle-password" onClick={() => setShowPassword(p => !p)}
                  style={eyeBtn}
                  onMouseEnter={(e) => ((e.target as HTMLElement).style.color = '#a855f7')}
                  onMouseLeave={(e) => ((e.target as HTMLElement).style.color = '#475569')}>
                  {showPassword
                    ? <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" /><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" /><line x1="1" y1="1" x2="23" y2="23" /></svg>
                    : <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>
                  }
                </button>
              </div>
            </div>

            {/* Şifre Tekrar */}
            <div style={{ marginBottom: '24px' }}>
              <label htmlFor="reg-confirm-password" style={{ display: 'block', fontSize: '13px', color: '#94a3b8', marginBottom: '7px', fontWeight: '500' }}>
                Şifre Tekrar
              </label>
              <div style={{ position: 'relative' }}>
                <span style={iconWrap}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M9 12l2 2 4-4" /><rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" />
                  </svg>
                </span>
                <input
                  id="reg-confirm-password" type={showConfirm ? 'text' : 'password'}
                  value={confirmPassword} onChange={(e) => { setConfirmPassword(e.target.value); setError(''); }}
                  placeholder="Şifrenizi tekrar girin" autoComplete="new-password" required
                  style={{ ...inputStyle(!!error && password !== confirmPassword), paddingRight: '42px' }}
                  onFocus={(e) => { e.target.style.borderColor = 'rgba(168,85,247,0.5)'; e.target.style.boxShadow = '0 0 0 3px rgba(168,85,247,0.1)'; }}
                  onBlur={(e) => { e.target.style.borderColor = (error && password !== confirmPassword) ? 'rgba(239,68,68,0.5)' : 'rgba(255,255,255,0.08)'; e.target.style.boxShadow = 'none'; }}
                />
                <button type="button" id="reg-toggle-confirm" onClick={() => setShowConfirm(p => !p)}
                  style={eyeBtn}
                  onMouseEnter={(e) => ((e.target as HTMLElement).style.color = '#a855f7')}
                  onMouseLeave={(e) => ((e.target as HTMLElement).style.color = '#475569')}>
                  {showConfirm
                    ? <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" /><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" /><line x1="1" y1="1" x2="23" y2="23" /></svg>
                    : <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>
                  }
                </button>
              </div>
            </div>

            {/* Hata */}
            <div style={{ height: '28px', marginTop: '-12px', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              {error && (
                <>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ef4444" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                  <span style={{ fontSize: '13px', color: '#ef4444' }}>{error}</span>
                </>
              )}
            </div>

            {/* Kayıt Butonu */}
            <button
              id="register-submit-btn" type="submit" disabled={!formReady}
              style={{
                width: '100%', padding: '14px',
                background: !formReady
                  ? 'rgba(30,41,59,0.5)'
                  : 'linear-gradient(135deg, #a855f7 0%, #06b6d4 100%)',
                border: 'none', borderRadius: '12px',
                color: !formReady ? '#475569' : '#fff',
                fontSize: '15px', fontWeight: '600',
                cursor: !formReady ? 'not-allowed' : 'pointer',
                transition: 'all 0.25s ease',
                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
                boxShadow: !formReady ? 'none' : '0 4px 20px rgba(168,85,247,0.35)',
              }}
              onMouseEnter={(e) => { if (formReady) e.currentTarget.style.transform = 'translateY(-1px)'; }}
              onMouseLeave={(e) => { e.currentTarget.style.transform = 'translateY(0)'; }}
            >
              {isLoading ? (
                <>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                    style={{ animation: 'spin 0.8s linear infinite' }}>
                    <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                  </svg>
                  Hesap oluşturuluyor...
                </>
              ) : (
                <>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="8.5" cy="7" r="4" />
                    <line x1="20" y1="8" x2="20" y2="14" /><line x1="23" y1="11" x2="17" y2="11" />
                  </svg>
                  Kayıt Ol
                </>
              )}
            </button>
          </form>

          {/* Giriş linki */}
          <div style={{ marginTop: '24px', textAlign: 'center' }}>
            <span style={{ fontSize: '13px', color: '#64748b' }}>Zaten hesabın var mı? </span>
            <button
              id="switch-to-login-btn"
              onClick={onSwitchToLogin}
              style={{
                border: 'none', cursor: 'pointer',
                fontSize: '13px', fontWeight: '600',
                background: 'linear-gradient(135deg, #a855f7, #38bdf8)',
                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                padding: 0,
              } as React.CSSProperties}
            >
              Giriş Yap
            </button>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) scale(1); opacity: 0.4; }
          50% { transform: translateY(-20px) scale(1.2); opacity: 0.8; }
        }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          15% { transform: translateX(-8px); } 30% { transform: translateX(8px); }
          45% { transform: translateX(-6px); } 60% { transform: translateX(6px); }
          75% { transform: translateX(-3px); } 90% { transform: translateX(3px); }
        }
        input::placeholder { color: rgba(100,116,139,0.5); }
      `}</style>
    </div>
  );
};

export default RegisterPage;
