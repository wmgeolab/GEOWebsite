const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  mode: "production",
  entry: { main: "./cms/assets/js/main.js", map: "./cms/assets/js/map.js" },
  output: {
    filename: "[name]-[fullhash].js",
    path: path.resolve(__dirname, "cms/dist/webpack_bundles"),
    clean: true,
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: "[name]-[fullhash].css" }),
    new BundleTracker({ filename: "./cms/webpack-stats.json" }),
  ],
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
};
