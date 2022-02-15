const path = require('path');

module.exports = {
  entry: './cms/school_app/static/myapp/assets/js/main.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
  },
};