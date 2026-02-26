import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        cream: '#FDF8F3',
        sand: '#F5E6D3',
        terracotta: '#C4A484',
        warm: '#E8D5C4',
        softBrown: '#8B7355',
      },
    },
  },
  plugins: [],
}
export default config
