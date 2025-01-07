#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render

# Baixar o Google Chrome, se ainda não estiver instalado
if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Certifique-se de retornar ao diretório original
else
  echo "...Using Chrome from cache"
fi

# Adiciona o Chrome ao PATH para garantir que o Selenium consiga encontrá-lo
export PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome"

