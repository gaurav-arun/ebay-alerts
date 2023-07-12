FROM node

WORKDIR /app

COPY alerts_frontend/package.json .

RUN npm install

COPY .. .

EXPOSE 3000

CMD [ "npm", "start" ]
