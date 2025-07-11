import { translations as ptBR } from './pt-BR';

export type Language = 'pt-BR' | 'en';

export const translations = {
  'pt-BR': ptBR,
  'en': ptBR, // Temporarily use PT-BR for English until we have proper English translations
};

// Get browser language preference
export function getDefaultLanguage(): Language {
  if (typeof window === 'undefined') return 'pt-BR';
  
  const browserLang = navigator.language || navigator.languages[0];
  
  // Check if it's Portuguese
  if (browserLang.startsWith('pt')) {
    return 'pt-BR';
  }
  
  // Default to Portuguese for now
  return 'pt-BR';
}

// Get translation helper
export function getTranslation(key: string, language: Language = 'pt-BR'): string {
  const keys = key.split('.');
  let value: any = translations[language];
  
  for (const k of keys) {
    if (value && typeof value === 'object' && k in value) {
      value = value[k];
    } else {
      return key; // Return the key itself if translation not found
    }
  }
  
  return typeof value === 'string' ? value : key;
}