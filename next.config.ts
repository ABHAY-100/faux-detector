import { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  webpack: (config) => {
    config.output = {
      ...config.output,
      filename: '[name].js',
      chunkFilename: '[name].js',
    };
    return config;
  },
};

export default nextConfig;
