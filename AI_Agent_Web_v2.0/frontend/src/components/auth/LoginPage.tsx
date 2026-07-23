import React, { useState, useRef, useEffect } from 'react';
import { useAuthStore } from '../../store/useAuthStore';

interface LoginPageProps {
  onSwitchToRegister?: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onSwitchToRegister }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [shake, setShake] = useState(false);
  const { login } = useAuthStore();
  const usernameRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    usernameRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    // Küçük gecikme ile loading animasyonu göster
    await new Promise((r) => setTimeout(r, 800));

    const success = login(username, password);
    setIsLoading(false);

    if (!success) {
      setError('Kullanıcı adı veya şifre hatalı.');
      setShake(true);
      setTimeout(() => setShake(false), 600);
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        width: '100vw',
        background: 'radial-gradient(ellipse at 50% 0%, rgba(6,182,212,0.12) 0%, #090d16 60%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: "'Inter', system-ui, sans-serif",
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Arkaplan parçacıkları */}
      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', pointerEvents: 'none' }}>
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              width: `${Math.random() * 3 + 1}px`,
              height: `${Math.random() * 3 + 1}px`,
              background: i % 2 === 0 ? 'rgba(6,182,212,0.4)' : 'rgba(168,85,247,0.4)',
              borderRadius: '50%',
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animation: `float ${Math.random() * 8 + 6}s ease-in-out infinite`,
              animationDelay: `${Math.random() * 5}s`,
            }}
          />
        ))}
      </div>

      {/* Grid çizgileri */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage:
            'linear-gradient(rgba(6,182,212,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(6,182,212,0.03) 1px, transparent 1px)',
          backgroundSize: '60px 60px',
          pointerEvents: 'none',
        }}
      />

      {/* Login Kartı */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          maxWidth: '420px',
          margin: '0 16px',
          animation: shake ? 'shake 0.5s ease-in-out' : undefined,
        }}
      >
        {/* Üst glow efekti */}
        <div
          style={{
            position: 'absolute',
            top: '-60px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '200px',
            height: '60px',
            background: 'radial-gradient(ellipse, rgba(6,182,212,0.35) 0%, transparent 70%)',
            filter: 'blur(10px)',
            pointerEvents: 'none',
          }}
        />

        <div
          style={{
            background: 'rgba(15,23,42,0.75)',
            backdropFilter: 'blur(24px)',
            WebkitBackdropFilter: 'blur(24px)',
            border: '1px solid rgba(6,182,212,0.2)',
            borderRadius: '20px',
            padding: '48px 40px',
            boxShadow:
              '0 0 0 1px rgba(255,255,255,0.05), 0 20px 60px rgba(0,0,0,0.5), 0 0 80px rgba(6,182,212,0.08)',
          }}
        >
          {/* Logo & Başlık */}
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            {/* Logo ikon */}
            <div
              style={{
                width: '72px',
                height: '72px',
                background: 'linear-gradient(135deg, rgba(6,182,212,0.2), rgba(168,85,247,0.2))',
                border: '1px solid rgba(6,182,212,0.35)',
                borderRadius: '18px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 20px',
                boxShadow: '0 0 30px rgba(6,182,212,0.2)',
              }}
            >
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 2L2 7l10 5 10-5-10-5z"
                  stroke="url(#g1)"
                  strokeWidth="1.5"
                  strokeLinejoin="round"
                />
                <path
                  d="M2 17l10 5 10-5"
                  stroke="url(#g2)"
                  strokeWidth="1.5"
                  strokeLinejoin="round"
                />
                <path
                  d="M2 12l10 5 10-5"
                  stroke="url(#g3)"
                  strokeWidth="1.5"
                  strokeLinejoin="round"
                />
                <defs>
                  <linearGradient id="g1" x1="2" y1="7" x2="22" y2="7" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#06b6d4" />
                    <stop offset="1" stopColor="#a855f7" />
                  </linearGradient>
                  <linearGradient id="g2" x1="2" y1="17" x2="22" y2="17" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#06b6d4" />
                    <stop offset="1" stopColor="#a855f7" />
                  </linearGradient>
                  <linearGradient id="g3" x1="2" y1="12" x2="22" y2="12" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#06b6d4" />
                    <stop offset="1" stopColor="#a855f7" />
                  </linearGradient>
                </defs>
              </svg>
            </div>

            <h1
              style={{
                margin: '0 0 6px',
                fontSize: '26px',
                fontWeight: '700',
                background: 'linear-gradient(135deg, #38bdf8 0%, #a855f7 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                letterSpacing: '-0.5px',
              }}
            >
              OpenPlexus AI
            </h1>
            <p style={{ margin: 0, fontSize: '13px', color: 'rgba(148,163,184,0.8)', letterSpacing: '0.3px' }}>
              Sisteme erişmek için giriş yapın
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} noValidate>
            {/* Kullanıcı Adı */}
            <div style={{ marginBottom: '20px' }}>
              <label
                htmlFor="login-username"
                style={{ display: 'block', fontSize: '13px', color: '#94a3b8', marginBottom: '8px', fontWeight: '500' }}
              >
                Kullanıcı Adı
              </label>
              <div style={{ position: 'relative' }}>
                <span
                  style={{
                    position: 'absolute',
                    left: '14px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    color: '#475569',
                    pointerEvents: 'none',
                  }}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                </span>
                <input
                  id="login-username"
                  ref={usernameRef}
                  type="text"
                  value={username}
                  onChange={(e) => { setUsername(e.target.value); setError(''); }}
                  placeholder="Kullanıcı adınızı girin"
                  autoComplete="username"
                  required
                  style={{
                    width: '100%',
                    boxSizing: 'border-box',
                    padding: '13px 14px 13px 42px',
                    background: 'rgba(15,23,42,0.8)',
                    border: `1px solid ${error ? 'rgba(239,68,68,0.5)' : 'rgba(255,255,255,0.08)'}`,
                    borderRadius: '12px',
                    color: '#f1f5f9',
                    fontSize: '14px',
                    outline: 'none',
                    transition: 'all 0.2s',
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = 'rgba(6,182,212,0.5)';
                    e.target.style.boxShadow = '0 0 0 3px rgba(6,182,212,0.1)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = error ? 'rgba(239,68,68,0.5)' : 'rgba(255,255,255,0.08)';
                    e.target.style.boxShadow = 'none';
                  }}
                />
              </div>
            </div>

            {/* Şifre */}
            <div style={{ marginBottom: '28px' }}>
              <label
                htmlFor="login-password"
                style={{ display: 'block', fontSize: '13px', color: '#94a3b8', marginBottom: '8px', fontWeight: '500' }}
              >
                Şifre
              </label>
              <div style={{ position: 'relative' }}>
                <span
                  style={{
                    position: 'absolute',
                    left: '14px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    color: '#475569',
                    pointerEvents: 'none',
                  }}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                  </svg>
                </span>
                <input
                  id="login-password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => { setPassword(e.target.value); setError(''); }}
                  placeholder="Şifrenizi girin"
                  autoComplete="current-password"
                  required
                  style={{
                    width: '100%',
                    boxSizing: 'border-box',
                    padding: '13px 42px 13px 42px',
                    background: 'rgba(15,23,42,0.8)',
                    border: `1px solid ${error ? 'rgba(239,68,68,0.5)' : 'rgba(255,255,255,0.08)'}`,
                    borderRadius: '12px',
                    color: '#f1f5f9',
                    fontSize: '14px',
                    outline: 'none',
                    transition: 'all 0.2s',
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = 'rgba(6,182,212,0.5)';
                    e.target.style.boxShadow = '0 0 0 3px rgba(6,182,212,0.1)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = error ? 'rgba(239,68,68,0.5)' : 'rgba(255,255,255,0.08)';
                    e.target.style.boxShadow = 'none';
                  }}
                />
                {/* Göster/Gizle */}
                <button
                  type="button"
                  id="toggle-password-visibility"
                  onClick={() => setShowPassword((p) => !p)}
                  style={{
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
                  }}
                  onMouseEnter={(e) => ((e.target as HTMLButtonElement).style.color = '#06b6d4')}
                  onMouseLeave={(e) => ((e.target as HTMLButtonElement).style.color = '#475569')}
                  aria-label={showPassword ? 'Şifreyi gizle' : 'Şifreyi göster'}
                >
                  {showPassword ? (
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
                      <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" />
                      <line x1="1" y1="1" x2="23" y2="23" />
                    </svg>
                  ) : (
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Hata Mesajı */}
            <div
              style={{
                height: '32px',
                marginTop: '-16px',
                marginBottom: '16px',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              {error && (
                <>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ef4444" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                  <span style={{ fontSize: '13px', color: '#ef4444' }}>{error}</span>
                </>
              )}
            </div>

            {/* Giriş Butonu */}
            <button
              id="login-submit-btn"
              type="submit"
              disabled={isLoading || !username || !password}
              style={{
                width: '100%',
                padding: '14px',
                background:
                  isLoading || !username || !password
                    ? 'rgba(30,41,59,0.5)'
                    : 'linear-gradient(135deg, #06b6d4 0%, #7c3aed 100%)',
                border: 'none',
                borderRadius: '12px',
                color: isLoading || !username || !password ? '#475569' : '#fff',
                fontSize: '15px',
                fontWeight: '600',
                cursor: isLoading || !username || !password ? 'not-allowed' : 'pointer',
                transition: 'all 0.25s ease',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                letterSpacing: '0.3px',
                boxShadow:
                  isLoading || !username || !password
                    ? 'none'
                    : '0 4px 20px rgba(6,182,212,0.35)',
              }}
              onMouseEnter={(e) => {
                const btn = e.currentTarget;
                if (!btn.disabled) btn.style.transform = 'translateY(-1px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
              }}
            >
              {isLoading ? (
                <>
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    style={{ animation: 'spin 0.8s linear infinite' }}
                  >
                    <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                  </svg>
                  Doğrulanıyor...
                </>
              ) : (
                <>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                    <polyline points="10 17 15 12 10 7" />
                    <line x1="15" y1="12" x2="3" y2="12" />
                  </svg>
                  Giriş Yap
                </>
              )}
            </button>
          </form>

          {/* Alt bilgi */}
          {/* Alt bilgi */}
          <div style={{ marginTop: '24px', textAlign: 'center' }}>
            <span style={{ fontSize: '13px', color: '#64748b' }}>Hesabın yok mu? </span>
            {onSwitchToRegister && (
              <button
                id="switch-to-register-btn"
                onClick={onSwitchToRegister}
                style={{
                  border: 'none', cursor: 'pointer',
                  fontSize: '13px', fontWeight: '600',
                  background: 'linear-gradient(135deg, #38bdf8, #a855f7)',
                  WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                  padding: 0,
                } as React.CSSProperties}
              >
                Kayıt Ol
              </button>
            )}
          </div>

          <div style={{ marginTop: '16px', textAlign: 'center' }}>
            <div style={{
              display: 'inline-flex', alignItems: 'center', gap: '6px',
              fontSize: '12px', color: 'rgba(100,116,139,0.7)',
              background: 'rgba(15,23,42,0.5)',
              border: '1px solid rgba(255,255,255,0.05)',
              borderRadius: '8px', padding: '6px 12px',
            }}>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
              Güvenli bağlantı — OpenPlexus AI Agent v2.0
            </div>
          </div>
        </div>
      </div>

      {/* CSS Animasyonları */}
      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) scale(1); opacity: 0.4; }
          50% { transform: translateY(-20px) scale(1.2); opacity: 0.8; }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          15% { transform: translateX(-8px); }
          30% { transform: translateX(8px); }
          45% { transform: translateX(-6px); }
          60% { transform: translateX(6px); }
          75% { transform: translateX(-3px); }
          90% { transform: translateX(3px); }
        }
        input::placeholder { color: rgba(100,116,139,0.5); }
      `}</style>
    </div>
  );
};

export default LoginPage;
