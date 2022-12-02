FROM node:19.2-alpine
WORKDIR /front
COPY package*.json ./
RUN npm install
COPY index.html tsconfig.json docker.dev.config.js ./
#EXPOSE 5173
#CMD ["npm", "run", "dev"]
