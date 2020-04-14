const path = require('path');

module.exports = {
  displayName: 'Online Client',
  rootDir: path.resolve(__dirname),
  testMatch: ['<rootDir>/src/**/*.test.js'],
  coverageReporters: ['cobertura'],
  reporters: [
    'default',
    [
      'jest-junit',
      {
        outputDirectory: 'coverage/junit',
        outputName: 'coverage-junit.xml',
        classNameTemplate: '{classname}',
        titleTemplate: '{title}',
      },
    ],
    [
      'jest-html-reporters',
      {
        publicPath: 'coverage/html',
        filename: 'jest-result.html',
        expand: true,
      },
    ],
  ],
};
