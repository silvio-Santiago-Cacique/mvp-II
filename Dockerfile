FROM nginx:latest

LABEL key="MVPAPI2"

COPY . /usr/share/nginx/html

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]