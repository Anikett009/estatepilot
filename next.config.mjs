/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: false, // Prevent strict mode from causing issues
  
    async rewrites() {
      return [
        {
          source: "/ai-helper/:path*", // The route inside Next.js
          destination: "http://127.0.0.1:8501/:path*", // Streamlit backend
        },
      ];
    },
  };
  
  export default nextConfig;
  