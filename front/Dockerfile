FROM node:16 as build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine


RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /app/dist /usr/share/nginx/html

COPY mime.types /etc/nginx/mime.types


EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
