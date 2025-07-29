FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

EXPOSE 8080

# Run without linting in development
CMD ["npm", "run", "serve", "--", "--skip-plugins", "@vue/cli-plugin-eslint"]