SHELL := /bin/bash

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
BUILD_DIR= ${ROOT_DIR}/build
BUILD_TMP_DIR= ${BUILD_DIR}/_build
VENV_DIR= ${BUILD_TMP_DIR}/_venv

ALL_PACKAGES := $(wildcard *)

EXCLUSIONS := LICENSE Makefile README.md build dns_map docker terraform security_group_map pypi_infra h_flow network
SRC_FILES := $(filter-out $(EXCLUSIONS), $(ALL_PACKAGES))

#apt install python3.8 python3.8-venv python3-venv
install-pip:
	sudo apt-get update
	sudo apt-get -y install python3-pip
	sudo pip3 install --upgrade pip

create_build_env:
	mkdir -p ${BUILD_TMP_DIR} &&\
	pip3 install wheel &&\
	pip3 install --upgrade setuptools

init_venv_dir: create_build_env
	python3.8 -m venv ${VENV_DIR} &&\
	source ${VENV_DIR}/bin/activate &&\
	pip3 install --upgrade pip &&\
	pip3 install -U setuptools

prepare_package_wheel-%: init_venv_dir
	${BUILD_DIR}/create_wheel.sh $(subst prepare_package_wheel-,,$@)

install_wheel-%: init_venv_dir raw_install_wheel-%
	echo "done installing $(subst install_wheel-,,$@)"
raw_install_wheel-%: package_source-%
	pip3 install --force-reinstall ${BUILD_TMP_DIR}/$(subst raw_install_wheel-,,$@)/dist/*.whl

recursive_install_from_source_local_venv-%: init_venv_dir
	source ${VENV_DIR}/bin/activate &&\
	${BUILD_DIR}/recursive_install_from_source.sh --root_dir ${ROOT_DIR} --package_name horey.$(subst recursive_install_from_source_local_venv-,,$@)

package_source-%:
	${BUILD_DIR}/create_wheel.sh $(subst package_source-,,$@)

install_from_source-%: init_venv_dir raw_install_from_source-%
raw_install_from_source-%: package_source-%
	source ${VENV_DIR}/bin/activate &&\
	pip3 install --force-reinstall ${BUILD_TMP_DIR}/$(subst raw_install_from_source-,,$@)/dist/*.whl

recursive_install_from_source-%: create_build_env
	${BUILD_DIR}/recursive_install_from_source.sh --root_dir ${ROOT_DIR} --package_name horey.$(subst recursive_install_from_source-,,$@)

install_pylint:
	source ${VENV_DIR}/bin/activate &&\
	pip3 install pylint

pylint: init_venv_dir install_pylint raw_pylint
raw_pylint:
	source ${VENV_DIR}/bin/activate &&\
	pylint  --rcfile=${BUILD_DIR}/.pylintrc ${ROOT_DIR}/aws_api/horey/aws_api/aws_clients/s3_client.py

install_test_deps-%: init_venv_dir
	source ${VENV_DIR}/bin/activate &&\
	pip3 install -r ${ROOT_DIR}/$(subst install_test_deps-,,$@)/tests/requirements.txt

test-configuration_policy: recursive_install_from_source_local_venv-configuration_policy install_test_deps-configuration_policy raw_test-configuration_policy

test-%: recursive_install_from_source_local_venv-% install_test_deps-% raw_test-%
raw_test-%:
	source ${VENV_DIR}/bin/activate &&\
	pytest ${ROOT_DIR}/$(subst raw_test-,,$@)/tests/*.py -s

clean:
	rm -rf ${BUILD_TMP_DIR}/*

#test_azure_api: recursive_install_from_source_local_venv-azure_api
test_azure_api: install_from_source-azure_api
	source ${VENV_DIR}/bin/activate &&\
	cd ${ROOT_DIR}/azure_api/tests &&\
	python3.8 test_azure_api_init_and_cache.py

test_aws_api: recursive_install_from_source_local_venv-aws_api
	source ${VENV_DIR}/bin/activate &&\
	cd ${ROOT_DIR}/aws_api/tests &&\
	python3.8 test_aws_api_init_and_cache.py

install_azure_api_prerequisites:
	source ${VENV_DIR}/bin/activate &&\
	sudo pip3 install --upgrade pip

test_zabbix_api: install_from_source-zabbix_api
	source ${VENV_DIR}/bin/activate &&\
	cd ${ROOT_DIR}/zabbix_api/tests &&\
	python3.8 test_zabbix_api.py

zip_env:
	cd "/Users/alexey.beley/private/horey/provision_constructor/tests/provision_constructor_deployment" &&\
	zip -r ${ROOT_DIR}/myfiles.zip "provision_constructor_deployment_dir"

unzip_env:
	unzip myfiles.zip -d /tmp/