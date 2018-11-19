#!/bin/bash

curl -sL https://deb.nodesource.com/setup_9.x | bash -
cd ../web_service/UI/static
npm init -y
npm i webpack --save-dev
npm i babel-core babel-loader babel-preset-es2015 babel-preset-react --save-dev
npm i bootstrap cytoscape fontawesome jquery react react-bootstrap react-dom --save-dev
npm run build
rm package-lock.json
cd ../../../setup
