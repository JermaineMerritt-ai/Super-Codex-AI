/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    SOVEREIGN_API_URL: process.env.SOVEREIGN_API_URL || 'http://localhost:8080',
  },
}

module.exports = nextConfig