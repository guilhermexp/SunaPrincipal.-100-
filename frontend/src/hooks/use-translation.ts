import { useState, useEffect } from 'react';
import { getTranslation, getDefaultLanguage, Language } from '@/lib/translations';

export function useTranslation() {
  const [language, setLanguage] = useState<Language>('pt-BR');

  useEffect(() => {
    // Get saved language preference or use default
    const savedLang = localStorage.getItem('suna-language') as Language;
    setLanguage(savedLang || getDefaultLanguage());
  }, []);

  const t = (key: string): string => {
    return getTranslation(key, language);
  };

  const changeLanguage = (newLang: Language) => {
    setLanguage(newLang);
    localStorage.setItem('suna-language', newLang);
  };

  return {
    t,
    language,
    changeLanguage,
  };
}