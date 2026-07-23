import { create } from 'zustand';

interface User {
  username: string;
  passwordHash: string;
}

interface AuthState {
  isAuthenticated: boolean;
  username: string | null;
  login: (username: string, password: string) => boolean;
  register: (username: string, password: string) => { success: boolean; error?: string };
  logout: () => void;
}

const STORAGE_KEY  = 'auth_token';
const STORAGE_USER = 'auth_user';
const STORAGE_USERS = 'auth_users';

// Basit hash (XOR + base64) — production'da bcrypt kullanılmalı
const hashPassword = (password: string): string =>
  btoa(
    password
      .split('')
      .map((c, i) => String.fromCharCode(c.charCodeAt(0) ^ (42 + (i % 7))))
      .join('')
  );

// Kayıtlı kullanıcıları yükle, Admin/Admin her zaman mevcut
const loadUsers = (): User[] => {
  const stored = localStorage.getItem(STORAGE_USERS);
  const users: User[] = stored ? JSON.parse(stored) : [];
  const hasAdmin = users.some((u) => u.username === 'Admin');
  if (!hasAdmin) {
    users.push({ username: 'Admin', passwordHash: hashPassword('Admin') });
    localStorage.setItem(STORAGE_USERS, JSON.stringify(users));
  }
  return users;
};

const saveUsers = (users: User[]) =>
  localStorage.setItem(STORAGE_USERS, JSON.stringify(users));

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: !!localStorage.getItem(STORAGE_KEY),
  username: localStorage.getItem(STORAGE_USER),

  login: (username: string, password: string): boolean => {
    const users = loadUsers();
    const hash = hashPassword(password);
    const found = users.find(
      (u) => u.username === username && u.passwordHash === hash
    );
    if (found) {
      const token = btoa(`${username}:${Date.now()}`);
      localStorage.setItem(STORAGE_KEY, token);
      localStorage.setItem(STORAGE_USER, username);
      set({ isAuthenticated: true, username });
      return true;
    }
    return false;
  },

  register: (username: string, password: string) => {
    if (!username.trim() || !password.trim()) {
      return { success: false, error: 'Kullanıcı adı ve şifre boş olamaz.' };
    }
    if (username.length < 3) {
      return { success: false, error: 'Kullanıcı adı en az 3 karakter olmalı.' };
    }
    if (password.length < 4) {
      return { success: false, error: 'Şifre en az 4 karakter olmalı.' };
    }

    const users = loadUsers();
    const exists = users.some(
      (u) => u.username.toLowerCase() === username.toLowerCase()
    );
    if (exists) {
      return { success: false, error: 'Bu kullanıcı adı zaten kullanılıyor.' };
    }

    const newUser: User = { username, passwordHash: hashPassword(password) };
    users.push(newUser);
    saveUsers(users);

    // Kayıt sonrası otomatik giriş
    const token = btoa(`${username}:${Date.now()}`);
    localStorage.setItem(STORAGE_KEY, token);
    localStorage.setItem(STORAGE_USER, username);
    set({ isAuthenticated: true, username });

    return { success: true };
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(STORAGE_USER);
    localStorage.removeItem('activeSessionId');
    set({ isAuthenticated: false, username: null });
  },
}));
