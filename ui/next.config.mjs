/** @type {import('next').NextConfig} */
const nextConfig = {
  devIndicators: false,
  // Enable standalone output for Docker
  output: 'standalone',
  // API routes handle proxying to backend (see app/api/*)
  // No rewrites needed - using Next.js API routes instead
};

export default nextConfig;
