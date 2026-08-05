FROM node:21-alpine

# Install docsify-cli (--ignore-scripts because docsify's post-install
# invokes husky which fails on the alpine base image)
RUN npm install -g --ignore-scripts docsify-cli@latest

EXPOSE 3000

# Serve whatever is mounted at /docs
CMD ["docsify", "serve", "/docs", "--port", "3000", "--host", "0.0.0.0"]
