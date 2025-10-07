/** @type {import('next').NextConfig} */
const nextConfig = {
  devIndicators: false,
  // Enable standalone output for Docker
  output: 'standalone',
  // Proxy /chat requests to the backend server
  async rewrites() {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
    return [
      {
        source: "/chat",
        destination: `${backendUrl}/chat`,
      },
    ];
  },
};

export default nextConfig;
