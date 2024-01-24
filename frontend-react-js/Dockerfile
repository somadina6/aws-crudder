FROM node:16.18

WORKDIR /frontend-react-js

COPY package*.json .

RUN npm install --no-audit --no-fund

COPY . .

ENV PORT=3000

EXPOSE ${PORT}

CMD ["npm", "start"]