/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/gene/:path*',
        destination: 'http://localhost:8000/api/gene/:path*',
      },
    ];
  },
}

module.exports = nextConfig
