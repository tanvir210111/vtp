/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return [
      {
        source: "/storage/:path*",
        destination: "http://localhost:8000/storage/:path*",
      },
    ];
  },
};

export default nextConfig;
