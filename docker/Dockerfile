FROM node:21-alpine

RUN npm install -g --ignore-scripts docsify-cli@latest

EXPOSE 3000

CMD ["docsify", "serve", "/docs", "--port", "3000", "--host", "0.0.0.0"]
