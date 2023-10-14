ARG NGINX_VERSION=1.25.2

FROM nginx:${NGINX_VERSION} as builder


RUN apt-get update && \
    apt-get install -y \
        openssh-client \
        mercurial \
        wget \
        libxml2 \
        libxslt1-dev \
        libpcre3 \
        libpcre3-dev \
        zlib1g \
        zlib1g-dev \
        openssl \
        libssl-dev \
        libtool \
        automake \
        gcc \
        g++ \
        make && \
    rm -rf /var/cache/apt

RUN curl http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -o /tmp/nginx-${NGINX_VERSION}.tar.gz && \
    cd /tmp && \
    tar xvzf nginx-${NGINX_VERSION}.tar.gz

RUN hg clone http://mdounin.ru/hg/ngx_http_auth_request_module /tmp/ngx_http_auth_request_module

COPY ngx_http_auth_request_module_config /tmp/ngx_http_auth_request_module/config

RUN cd /tmp/nginx-${NGINX_VERSION} && \
    ./configure --with-compat --add-dynamic-module=/tmp/ngx_http_auth_request_module && \
    make modules

FROM nginx:${NGINX_VERSION}-alpine

COPY --from=builder /tmp/nginx-${NGINX_VERSION}/objs/ngx_http_auth_request_module.so /etc/nginx/modules/

LABEL authors="Red"
WORKDIR '/app'

COPY app /app
RUN chown -R 33:33 /app
RUN chmod -R 755 /app

COPY default.conf /etc/nginx/templates/default.conf.template

RUN mkdir /tmp/files

ENV NGINX_PORT=80
ENV NGINX_SERVER_NAME=0.0.0.0
ENV INTERNAL_API_HOST=localhost
ENV INTERNAL_API_PORT=8000

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
