FROM frrouting/frr:v8.3.0

RUN apk add --update-cache \ 
        tshark \
    && rm -rf /var/cache/apk/*

CMD /bin/sh
