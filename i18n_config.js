// Frontend i18n configuration (Next.js with next-i18next)
// next-i18next.config.js

module.exports = {
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ko', 'ja', 'es', 'fr', 'de', 'zh'],
    localeDetection: true,
  },
  reloadOnPrerender: process.env.NODE_ENV === 'development',
}

// Usage in components:
// import { useTranslation } from 'next-i18next'
// const { t } = useTranslation('common')
// <h1>{t('square.title')}</h1>

// Backend i18n helper
// app/i18n/__init__.py

import json
from pathlib import Path
from typing import Dict

class I18n:
    def __init__(self):
        self.translations: Dict[str, Dict] = {}
        self.load_translations()
    
    def load_translations(self):
        locale_dir = Path(__file__).parent / "locales"
        for locale_file in locale_dir.glob("*.json"):
            locale = locale_file.stem
            with open(locale_file, 'r', encoding='utf-8') as f:
                self.translations[locale] = json.load(f)
    
    def get(self, key: str, locale: str = "en") -> str:
        keys = key.split('.')
        value = self.translations.get(locale, self.translations['en'])
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, key)
            else:
                return key
        
        return value if isinstance(value, str) else key

i18n = I18n()

# Usage in FastAPI:
# from app.i18n import i18n
# error_message = i18n.get('errors.notFound', locale=user.preferred_language)
