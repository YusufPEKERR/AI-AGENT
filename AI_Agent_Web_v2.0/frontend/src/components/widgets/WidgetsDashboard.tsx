import React, { useState, useEffect } from 'react';
import { 
  CloudSun, Sun, CloudRain, Cloud, CloudLightning, Snowflake, Wind, Droplets, 
  Search, RefreshCw, Clock, TrendingUp, DollarSign, Cpu, Hash, Binary, Sparkles,
  MapPin, Gauge, Compass, ShieldAlert, CheckCircle, ArrowUpRight, ArrowDownRight
} from 'lucide-react';

interface CityCoordinates {
  name: string;
  country: string;
  lat: number;
  lon: number;
}

const PRESET_CITIES: CityCoordinates[] = [
  { name: 'İstanbul', country: 'Türkiye', lat: 41.0082, lon: 28.9784 },
  { name: 'Ankara', country: 'Türkiye', lat: 39.9334, lon: 32.8597 },
  { name: 'İzmir', country: 'Türkiye', lat: 38.4237, lon: 27.1428 },
  { name: 'Antalya', country: 'Türkiye', lat: 36.8969, lon: 30.7133 },
  { name: 'Bursa', country: 'Türkiye', lat: 40.1885, lon: 29.0610 },
  { name: 'Londra', country: 'Birleşik Krallık', lat: 51.5074, lon: -0.1278 },
  { name: 'New York', country: 'ABD', lat: 40.7128, lon: -74.0060 },
  { name: 'Tokyo', country: 'Japonya', lat: 35.6762, lon: 139.6503 },
];

interface WeatherData {
  temp: number;
  humidity: number;
  windSpeed: number;
  weatherCode: number;
  apparentTemp: number;
  pressure: number;
  daily: {
    time: string[];
    maxTemp: number[];
    minTemp: number[];
    code: number[];
  };
}

export const WidgetsDashboard: React.FC = () => {
  const [selectedCity, setSelectedCity] = useState<CityCoordinates>(PRESET_CITIES[0]);
  const [searchQuery, setSearchQuery] = useState('');
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loadingWeather, setLoadingWeather] = useState(false);
  const [weatherError, setWeatherError] = useState('');

  // World Clocks state
  const [currentTime, setCurrentTime] = useState(new Date());

  // Utility tool state
  const [base64Input, setBase64Input] = useState('');
  const [base64Output, setBase64Output] = useState('');
  const [base64Mode, setBase64Mode] = useState<'encode' | 'decode'>('encode');

  // Live Timer tick
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Fetch Weather from Open-Meteo API
  const fetchWeather = async (city: CityCoordinates) => {
    setLoadingWeather(true);
    setWeatherError('');
    try {
      const res = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${city.lat}&longitude=${city.lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto`
      );
      if (!res.ok) throw new Error('Hava durumu verisi alınamadı.');
      const data = await res.json();
      setWeather({
        temp: Math.round(data.current.temperature_2m),
        humidity: data.current.relative_humidity_2m,
        windSpeed: Math.round(data.current.wind_speed_10m),
        weatherCode: data.current.weather_code,
        apparentTemp: Math.round(data.current.apparent_temperature),
        pressure: Math.round(data.current.surface_pressure),
        daily: {
          time: data.daily.time,
          maxTemp: data.daily.temperature_2m_max.map((t: number) => Math.round(t)),
          minTemp: data.daily.temperature_2m_min.map((t: number) => Math.round(t)),
          code: data.daily.weather_code
        }
      });
    } catch (err: any) {
      setWeatherError(err.message || 'Hava durumu yüklenirken bir hata oluştu');
    } finally {
      setLoadingWeather(false);
    }
  };

  useEffect(() => {
    fetchWeather(selectedCity);
  }, [selectedCity]);

  // Search City via Open-Meteo Geocoding
  const handleCitySearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setLoadingWeather(true);
    try {
      const res = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(searchQuery)}&count=1&language=tr&format=json`);
      const data = await res.json();
      if (data.results && data.results.length > 0) {
        const found = data.results[0];
        const newCity: CityCoordinates = {
          name: found.name,
          country: found.country || '',
          lat: found.latitude,
          lon: found.longitude
        };
        setSelectedCity(newCity);
        setSearchQuery('');
      } else {
        setWeatherError('Şehir bulunamadı!');
      }
    } catch (err) {
      setWeatherError('Şehir aramasında hata oluştu.');
    } finally {
      setLoadingWeather(false);
    }
  };

  // Weather Code Helper
  const getWeatherInfo = (code: number) => {
    if (code === 0) return { label: 'Açık / Güneşli', icon: <Sun className="w-10 h-10 text-amber-400 animate-spin-slow" />, bg: 'from-amber-500/20 to-orange-500/10' };
    if (code >= 1 && code <= 3) return { label: 'Parçalı Bulutlu', icon: <CloudSun className="w-10 h-10 text-cyan-300" />, bg: 'from-cyan-500/20 to-blue-500/10' };
    if (code >= 45 && code <= 48) return { label: 'Sisli', icon: <Cloud className="w-10 h-10 text-slate-400" />, bg: 'from-slate-500/20 to-slate-700/10' };
    if (code >= 51 && code <= 67) return { label: 'Yağmurlu', icon: <CloudRain className="w-10 h-10 text-blue-400" />, bg: 'from-blue-600/20 to-indigo-600/10' };
    if (code >= 71 && code <= 77) return { label: 'Kar Yağışlı', icon: <Snowflake className="w-10 h-10 text-sky-200" />, bg: 'from-sky-400/20 to-cyan-500/10' };
    if (code >= 80 && code <= 82) return { label: 'Sağanak Yağış', icon: <CloudRain className="w-10 h-10 text-blue-500" />, bg: 'from-blue-500/25 to-purple-500/10' };
    if (code >= 95) return { label: 'Gökgürültülü Fırtına', icon: <CloudLightning className="w-10 h-10 text-purple-400" />, bg: 'from-purple-600/25 to-pink-600/10' };
    return { label: 'Bulutlu', icon: <Cloud className="w-10 h-10 text-slate-300" />, bg: 'from-slate-500/20 to-blue-500/10' };
  };

  // Base64 Converter logic
  const handleBase64Convert = (text: string, mode: 'encode' | 'decode') => {
    setBase64Input(text);
    try {
      if (!text) {
        setBase64Output('');
        return;
      }
      if (mode === 'encode') {
        setBase64Output(btoa(unescape(encodeURIComponent(text))));
      } else {
        setBase64Output(decodeURIComponent(escape(atob(text))));
      }
    } catch {
      setBase64Output('Hata: Geçersiz Base64 formatı');
    }
  };

  // World Clocks config
  const getTimeString = (timeZone: string) => {
    return new Intl.DateTimeFormat('tr-TR', {
      timeZone,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }).format(currentTime);
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl backdrop-blur-md">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-gradient-to-tr from-cyan-500/20 to-purple-500/20 border border-cyan-500/30 text-cyan-400">
              <CloudSun className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                Hava Durumu & Canlı Araçlar
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                  Live Widgets
                </span>
              </h2>
              <p className="text-xs text-slate-400">Anlık şehir hava tahminleri, finans kurları, dünya saatleri ve geliştirici araçları.</p>
            </div>
          </div>
        </div>

        {/* Quick Search */}
        <form onSubmit={handleCitySearch} className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Şehir ara (Örn: Ankara, Berlin)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-3 py-2 bg-slate-950/80 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 w-64 transition-all"
            />
          </div>
          <button
            type="submit"
            className="px-3 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-semibold shadow-md transition-all"
          >
            Ara
          </button>
        </form>
      </div>

      {/* Preset Cities Selector */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 custom-scrollbar">
        <span className="text-xs font-medium text-slate-400 shrink-0 flex items-center gap-1">
          <MapPin className="w-3.5 h-3.5 text-cyan-400" /> Hızlı Şehirler:
        </span>
        {PRESET_CITIES.map((c) => {
          const isSelected = selectedCity.name === c.name;
          return (
            <button
              key={c.name}
              onClick={() => setSelectedCity(c)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all shrink-0 ${
                isSelected
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold shadow-lg shadow-cyan-500/20'
                  : 'bg-slate-900/80 text-slate-300 hover:bg-slate-800 border border-slate-800'
              }`}
            >
              {c.name}
            </button>
          );
        })}
      </div>

      {/* Main Grid Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Weather Main Card (2 Cols wide on large screens) */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Current Weather Box */}
          <div className={`relative overflow-hidden rounded-2xl bg-gradient-to-br border border-slate-800 p-6 backdrop-blur-lg ${
            weather ? getWeatherInfo(weather.weatherCode).bg : 'from-slate-900 to-slate-950'
          }`}>
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="flex items-center gap-2 text-slate-400 text-xs font-medium">
                  <MapPin className="w-4 h-4 text-cyan-400" />
                  <span>{selectedCity.country}</span>
                </div>
                <h3 className="text-3xl font-extrabold text-white mt-1">{selectedCity.name}</h3>
              </div>
              <button
                onClick={() => fetchWeather(selectedCity)}
                className="p-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 text-slate-300 transition-all border border-slate-700/50"
                title="Yenile"
              >
                <RefreshCw className={`w-4 h-4 ${loadingWeather ? 'animate-spin' : ''}`} />
              </button>
            </div>

            {loadingWeather ? (
              <div className="py-12 flex flex-col items-center justify-center text-slate-400 gap-2">
                <RefreshCw className="w-8 h-8 animate-spin text-cyan-400" />
                <span className="text-xs">Hava durumu verisi çekiliyor...</span>
              </div>
            ) : weatherError ? (
              <div className="py-8 text-center text-red-400 text-xs flex items-center justify-center gap-2">
                <ShieldAlert className="w-4 h-4" />
                <span>{weatherError}</span>
              </div>
            ) : weather ? (
              <div className="space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                  {/* Temp & Icon */}
                  <div className="flex items-center gap-4">
                    <div className="p-3 rounded-2xl bg-slate-950/40 border border-white/10 backdrop-blur-sm">
                      {getWeatherInfo(weather.weatherCode).icon}
                    </div>
                    <div>
                      <div className="text-5xl font-black tracking-tight text-white">
                        {weather.temp}°C
                      </div>
                      <div className="text-sm font-semibold text-cyan-300 mt-1">
                        {getWeatherInfo(weather.weatherCode).label}
                      </div>
                      <div className="text-xs text-slate-400 mt-0.5">
                        Hissedilen: <span className="text-slate-200 font-medium">{weather.apparentTemp}°C</span>
                      </div>
                    </div>
                  </div>

                  {/* Weather Sub Metrics Grid */}
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 bg-slate-950/50 p-4 rounded-xl border border-slate-800/80 backdrop-blur-sm">
                    <div className="space-y-1">
                      <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
                        <Droplets className="w-3.5 h-3.5 text-cyan-400" />
                        <span>Nem Oranı</span>
                      </div>
                      <div className="text-sm font-bold text-slate-100">%{weather.humidity}</div>
                    </div>

                    <div className="space-y-1">
                      <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
                        <Wind className="w-3.5 h-3.5 text-emerald-400" />
                        <span>Rüzgar Hızı</span>
                      </div>
                      <div className="text-sm font-bold text-slate-100">{weather.windSpeed} km/h</div>
                    </div>

                    <div className="space-y-1 col-span-2 sm:col-span-1">
                      <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
                        <Gauge className="w-3.5 h-3.5 text-purple-400" />
                        <span>Basınç</span>
                      </div>
                      <div className="text-sm font-bold text-slate-100">{weather.pressure} hPa</div>
                    </div>
                  </div>
                </div>

                {/* 7-Day Forecast */}
                {weather.daily && (
                  <div>
                    <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-amber-400" /> 7 Günlük Hava Tahmini
                    </h4>
                    <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2">
                      {weather.daily.time.slice(0, 7).map((t, idx) => {
                        const dateObj = new Date(t);
                        const dayName = idx === 0 ? 'Bugün' : dateObj.toLocaleDateString('tr-TR', { weekday: 'short' });
                        const code = weather.daily.code[idx];
                        const info = getWeatherInfo(code);
                        return (
                          <div
                            key={t}
                            className="bg-slate-950/60 border border-slate-800/80 p-2.5 rounded-xl text-center flex flex-col items-center justify-between space-y-1.5 hover:border-cyan-500/40 transition-all"
                          >
                            <span className="text-[11px] font-semibold text-slate-300">{dayName}</span>
                            <div className="scale-75 my-[-4px]">
                              {info.icon}
                            </div>
                            <div className="text-[10px] text-slate-400 truncate w-full px-1">{info.label}</div>
                            <div className="text-xs font-bold text-slate-100">
                              {weather.daily.maxTemp[idx]}° <span className="text-slate-500 font-normal">{weather.daily.minTemp[idx]}°</span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            ) : null}
          </div>

          {/* DevSecOps & SysAdmin Quick Utility Converter */}
          <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-slate-100 font-bold text-sm">
                <Binary className="w-4 h-4 text-cyan-400" />
                <span>Base64 Encoder / Decoder Araçları</span>
              </div>
              <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800">
                <button
                  onClick={() => { setBase64Mode('encode'); handleBase64Convert(base64Input, 'encode'); }}
                  className={`px-2.5 py-1 text-[11px] font-semibold rounded-md transition-all ${
                    base64Mode === 'encode' ? 'bg-cyan-600 text-white' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  Encode
                </button>
                <button
                  onClick={() => { setBase64Mode('decode'); handleBase64Convert(base64Input, 'decode'); }}
                  className={`px-2.5 py-1 text-[11px] font-semibold rounded-md transition-all ${
                    base64Mode === 'decode' ? 'bg-cyan-600 text-white' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  Decode
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-[11px] text-slate-400 font-medium">Girdi Metni:</label>
                <textarea
                  rows={3}
                  value={base64Input}
                  onChange={(e) => handleBase64Convert(e.target.value, base64Mode)}
                  placeholder="Metin veya Base64 giriniz..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-cyan-500/50 resize-none font-mono"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] text-slate-400 font-medium">Sonuç:</label>
                <div className="w-full bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-xs font-mono text-cyan-300 break-all min-h-[78px] overflow-y-auto max-h-[78px]">
                  {base64Output || <span className="text-slate-600 italic">Dönüştürülen metin burada görünecek...</span>}
                </div>
              </div>
            </div>
          </div>

        </div>

        {/* Right Column: World Clocks & Market Ticker */}
        <div className="space-y-6">
          
          {/* World Clocks Widget */}
          <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl space-y-4">
            <div className="flex items-center gap-2 text-slate-100 font-bold text-sm border-b border-slate-800 pb-3">
              <Clock className="w-4 h-4 text-purple-400" />
              <span>Dünya Saatleri (World Clocks)</span>
            </div>

            <div className="space-y-2.5">
              {[
                { city: 'İstanbul', zone: 'Europe/Istanbul', flag: '🇹🇷', offset: 'UTC+3' },
                { city: 'Londra', zone: 'Europe/London', flag: '🇬🇧', offset: 'UTC+0' },
                { city: 'New York', zone: 'America/New_York', flag: '🇺🇸', offset: 'UTC-4' },
                { city: 'Tokyo', zone: 'Asia/Tokyo', flag: '🇯🇵', offset: 'UTC+9' },
                { city: 'Frankfurt', zone: 'Europe/Berlin', flag: '🇩🇪', offset: 'UTC+2' },
              ].map((c) => (
                <div
                  key={c.city}
                  className="flex items-center justify-between p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/60 hover:border-purple-500/30 transition-all"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{c.flag}</span>
                    <div>
                      <div className="text-xs font-semibold text-slate-200">{c.city}</div>
                      <div className="text-[10px] text-slate-500">{c.offset}</div>
                    </div>
                  </div>
                  <div className="text-sm font-mono font-bold text-purple-300">
                    {getTimeString(c.zone)}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Financial Live Ticker Widget */}
          <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2 text-slate-100 font-bold text-sm">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                <span>Piyasa Kurları & Kripto</span>
              </div>
              <span className="text-[10px] text-emerald-400 bg-emerald-950/60 border border-emerald-800/50 px-2 py-0.5 rounded-full font-mono">
                Live Indicative
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2.5">
              {[
                { pair: 'USD / TRY', price: '38.42 ₺', change: '+0.15%', up: true },
                { pair: 'EUR / TRY', price: '42.10 ₺', change: '-0.08%', up: false },
                { pair: 'GBP / TRY', price: '49.85 ₺', change: '+0.32%', up: true },
                { pair: 'BTC / USD', price: '$89,450', change: '+2.40%', up: true },
                { pair: 'ETH / USD', price: '$3,420', change: '+1.15%', up: true },
                { pair: 'Gram Altın', price: '3,120 ₺', change: '+0.45%', up: true },
              ].map((m) => (
                <div key={m.pair} className="p-3 bg-slate-950/60 border border-slate-800/60 rounded-xl space-y-1">
                  <div className="text-[11px] font-semibold text-slate-400">{m.pair}</div>
                  <div className="text-sm font-bold text-slate-100 font-mono">{m.price}</div>
                  <div className={`text-[10px] font-semibold flex items-center gap-0.5 ${
                    m.up ? 'text-emerald-400' : 'text-rose-400'
                  }`}>
                    {m.up ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                    <span>{m.change}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* DevSecOps Motivational Quote / Tip Card */}
          <div className="bg-gradient-to-br from-cyan-950/40 to-purple-950/30 border border-cyan-500/20 p-5 rounded-2xl space-y-2">
            <div className="flex items-center gap-2 text-cyan-400 text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-4 h-4" /> SysAdmin & DevSecOps İpucu
            </div>
            <p className="text-xs text-slate-300 leading-relaxed italic">
              "Otomasyon ve proaktif izleme, sistem dayanıklılığının anahtarıdır. Tüm loglarınızı merkezi olarak toplayın ve güvenlik yamalarını güncel tutun."
            </p>
          </div>

        </div>

      </div>
    </div>
  );
};

export default WidgetsDashboard;
