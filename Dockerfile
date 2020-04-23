FROM opencadc/astropy:3.8-slim

WORKDIR /usr/src/app


ARG OPENCADC_BRANCH=master
ARG OPENCADC_REPO=opencadc
ARG OMC_REPO=opencadc-metadata-curation

RUN git clone https://github.com/${OPENCADC_REPO}/caom2tools.git --branch ${OPENCADC_BRANCH} --single-branch && \
    pip install ./caom2tools/caom2 && \
    pip install ./caom2tools/caom2utils

RUN git clone https://github.com/${OMC_REPO}/caom2pipe.git && \
  pip install ./caom2pipe
  
RUN pip install git+https://github.com/${OMC_REPO}/cgps2caom2.git

COPY ./docker-entrypoint.sh ./

ENTRYPOINT ["./docker-entrypoint.sh"]
