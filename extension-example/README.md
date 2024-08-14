# Мод-расширение

Если вам недостаточно данных которые передаёт `data-provider`, вы можете создать свой собственный мод-расширение, который по простому интерфейсу подключится к `data-provider` и будет передавать данные виджетам по общему каналу связи.

![](/.github/demo-extension.png)

## Описание
Этот пример предоставляет полностью рабочий мод, который создаёт триггер и состояние. 

Триггер срабатывает при нажатии на кнопку `T` и отправляет время с момента запуска игры `BigWorld.time()` в триггер `demoExtension.demo.trigger`.  
Состояние считает число нажатий пробела и отправляет его в состояние `demoExtension.demo.state`.

## Код мода
Точка входа в мод (которую запускают танки) [extension-example/res/scripts/client/gui/mods/mod_dataProviderExtension.py](./res/scripts/client/gui/mods/mod_dataProviderExtension.py).

> [!IMPORTANT]
> Обратите внимание, что моды должны начинаться с префикса `mod_`

Файл `dataProviderTyping.py` содержит интерфейсы `data-provider`, они нужны исключительно для подсказок кода в редакторе.

![](/.github/intellisens-mod.png)

## Компиляция
### На Unix системах
```bash
./build.sh -v 1.0.0
```

### На Windows
Запустите `build.bat` и в открывшемся окне введите целевую версию мода.


У вас должны быть установлены:
- `python 2.7` и доступен в `cmd` по имени `python`  
  Eсли исполняемый файл называется `python2`, то замените на `python2` в `build.bat` [*Step 4*](./build.bat#L16)
- `7zip` находится в папке `C:\Program Files\7-Zip\7z.exe`  
  Eсли у вас другая папка, то замените путь в `build.bat` [*Step 9*](./build.bat#L37)

## Виджет
Пример виджета называется `widget.html`, просто откройте его в браузере.

Для простоты он сделан в виде одного `html` файла, однако, если вы используете полноценный npm проект, то можете создать файл `demoExtension.d.ts` в котором объявить интерфейс расширения.

```typescript
import { State, Trigger } from "wotstat-widgets-sdk"

declare global {
  interface WidgetsSdkExtensions {
    demoExtension: {
      demo: {
        state: State<number>
        trigger: Trigger<string>
      }
    }
  }
}
```

Это позволит редактору кода выдавать подсказки и автодополнение.

![](/.github/intellisens.png)