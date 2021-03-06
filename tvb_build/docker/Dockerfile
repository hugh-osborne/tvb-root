FROM continuumio/miniconda3

RUN apt-get -y update && apt-get -y install build-essential gcc
RUN apt-get -y install texlive-base texlive-formats-extra
RUN apt-get -y install octave postgresql

USER postgres
RUN service postgresql start && createdb -O postgres tvb-test && psql --command "ALTER USER postgres WITH PASSWORD 'postgres';"

USER root
RUN conda update -n base -c defaults conda

RUN conda create -y --name tvb-docs python=3.7 nomkl numba scipy numpy networkx scikit-learn cython pip numexpr psutil
RUN conda install -y --name tvb-docs pytest pytest-cov pytest-benchmark matplotlib
RUN conda install -y --name tvb-docs psycopg2 pytables scikit-image==0.14.2 simplejson cherrypy docutils
RUN conda install -y --name tvb-docs -c conda-forge jupyterlab
RUN /opt/conda/envs/tvb-docs/bin/pip install --upgrade pip
RUN /opt/conda/envs/tvb-docs/bin/pip install h5py>=2.10 formencode cfflib jinja2 nibabel sqlalchemy==1.1.14 sqlalchemy-migrate==0.11.0 allensdk BeautifulSoup4 subprocess32
RUN /opt/conda/envs/tvb-docs/bin/pip install tvb-gdist typing sphinx==1.2.3 docutils==0.12

RUN conda create -y --name tvb-run python=3.7 nomkl numba scipy numpy networkx scikit-learn cython pip numexpr psutil
RUN conda install -y --name tvb-run pytest pytest-cov pytest-benchmark matplotlib
RUN conda install -y --name tvb-run psycopg2 pytables scikit-image==0.14.2 simplejson cherrypy docutils
RUN conda install -y --name tvb-run -c conda-forge jupyterlab
RUN /opt/conda/envs/tvb-run/bin/pip install --upgrade pip
RUN /opt/conda/envs/tvb-run/bin/pip install h5py>=2.10 formencode cfflib jinja2 nibabel sqlalchemy==1.1.14 sqlalchemy-migrate==0.11.0 allensdk BeautifulSoup4 subprocess32
RUN /opt/conda/envs/tvb-run/bin/pip install tvb-gdist typing

# Jupyther notebook configurations: set password
# tvb42
RUN /bin/bash -c "source activate tvb-run"; \
    /opt/conda/envs/tvb-run/bin/jupyter notebook --generate-config; \
    echo "c.NotebookApp.password='sha1:12bff019c253:9daecd92c2e9bdb10b3b8a06767a74a0fe078d7c'">>/root/.jupyter/jupyter_notebook_config.py

WORKDIR /root

RUN wget https://zenodo.org/record/3497545/files/tvb_data_2_0_1.zip?download=1 -O tvb_data.zip; \
    unzip tvb_data.zip; rm tvb_data.zip; \
    cd tvb_data; \
    /opt/conda/envs/tvb-run/bin/python setup.py develop;\
    /opt/conda/envs/tvb-docs/bin/python setup.py develop

# make sure a copy of tvb-root exists inside, for users without Github clone
RUN git clone --depth 1 https://github.com/the-virtual-brain/tvb-root.git; \
    cd tvb-root/tvb_build; \
    /bin/bash -c "source activate tvb-run && /bin/bash install_full_tvb.sh"; \
    /bin/bash -c "source activate tvb-docs && /bin/bash install_full_tvb.sh"

RUN mkdir /root/.tvb-temp; mkdir /root/.tvb-temp/logs; mkdir /root/TVB_DATA

COPY .tvb.configuration /root/.tvb.configuration

WORKDIR /root/tvb-root
# MOUNT -v [local- tvb-root - clone]:/root/tvb-root

# For building static help for web
#CMD ["bash","-c","source activate tvb-docs && cd tvb_build && python build_step1.py"]

# For building the Pypi packages
#CMD ["bash","-c","source activate tvb-run && cd tvb_build && bash package_for_pip.sh"]

# For running all unit-tests
# inspect output in local tvb-root/tvb_bin/TEST_OUT folder
#<testsuite errors="100" failures="248" hostname="747eee3aaab5" name="pytest" skipped="3" tests="463"
#<testsuite errors="100" failures="237" hostname="fe4fc3f6b6c7" name="pytest" skipped="3" tests="463"
#CMD ["bash","-c","source activate tvb-run && cd tvb_bin && service postgresql start && bash run_tests.sh postgres"]

# For running Jupyter notebooks
# bind port 8888:8888
#CMD ["bash","-c","source activate tvb-run && cd tvb_documentation && jupyter notebook --ip 0.0.0.0 --no-browser --allow-root"]

# For running TVB Web GUI
# bind port 8080
# MOUNT -v [local- ~/TVB ]:/root/TVB_DATA
#CMD ["bash","-c","source activate tvb-run && cd tvb_bin && python -m tvb.interfaces.web.run WEB_PROFILE"]

CMD ["bash","-c","source activate tvb-run && /bin/bash"]