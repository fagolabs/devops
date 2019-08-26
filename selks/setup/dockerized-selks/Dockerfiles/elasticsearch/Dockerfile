FROM elasticsearch:6.7.0

RUN usermod -u 9999 elasticsearch
RUN groupmod -g 9999 elasticsearch

EXPOSE 9200 9300
USER elasticsearch
CMD ["eswrapper"]
