import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        simpsons: {
          yellow: "#FFD521",
          black: "#000000",
          blue: "#70D1FE",
          brown: "#8B4513",
        },
      },
    },
  },
  plugins: [],
};

export default config;
