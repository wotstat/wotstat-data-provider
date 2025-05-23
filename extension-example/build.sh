
# Название мода
MOD_NAME="example.data-provider-extension"

# Получение агрументов командной строки
while getopts "v:" flag
do
  case "${flag}" in
    v) v=${OPTARG};;
  esac
done


# Удаление старой сборки и создание новой
rm -rf ./build
mkdir ./build
cp -r ./res ./build

# Компиляция всех файлов .py в .pyc
python2 -m compileall ./build

# Замена {{VERSION}} на переданное значение в аргументах
meta=$(<meta.xml)
meta="${meta/\{\{VERSION\}\}/$v}"

# Запись нового meta.xml
cd ./build
echo "$meta" > ./meta.xml


# Удаление старой wotmod сборки и создание новой
target=$MOD_NAME"_$v.wotmod"

rm -rf $target
zip -dvr -0 -X $target res -i "*.pyc"
zip -vr -0 -X $target meta.xml

# Перемещение сборки в корень проекта
cd ../
cp ./build/$target $target
rm -rf ./build

cp $target $MOD_NAME"_$v.mtmod"
