By actowed <3



1) Установить Pycharm community edition! -> https://www.jetbrains.com/pycharm/download/?section=windows (ВАЖНО! Community edition находится по этой ссылке чуть ниже, чем professional edition!!!)



2) После установки открыть папку как (Open as pycharm folder)

![photo_5_2024-12-31_18-35-27](https://github.com/user-attachments/assets/47edf611-49f5-4ba6-a7da-1b596fea5e8b)



3)Открыть настройки и создать виртуальное окружение
![photo_4_2024-12-31_18-35-27](https://github.com/user-attachments/assets/fea4ad54-50a3-4961-8140-58ad4b81c223)
![photo_1_2024-12-31_18-35-27](https://github.com/user-attachments/assets/8b80ff25-c2c4-4fd0-9951-6dc94c8281a7)



4)Как все установится, открыть терминал и прописать следующую команду:

pip install -r requirements.txt

![image](https://github.com/user-attachments/assets/5fa2ac23-7811-47d4-8178-ecc0af663f94)


4.1)Если этот вариант не сработал, открываем файл из Pycharm и сверху должна быть кнопка вроде install requirements from requirements.txt , нажмаем ее и идем к шагу 5
![photo_3_2024-12-31_18-35-27](https://github.com/user-attachments/assets/0520b1f4-7ec3-4740-8142-7049971dca49)



5) Как только все установилось, запускаем программу на кнопку вверху
![photo_2_2024-12-31_18-35-27](https://github.com/user-attachments/assets/9118f0ee-cc55-4b05-bce1-fc4887522885)



Внешний вид программы:
![image](https://github.com/user-attachments/assets/f22a9e48-f734-400d-af96-32604b047f98)



Что прописывать в "Запрещенные зоны":
(По умолчанию будут замазываться генеталии и грудь (только женские))

"FEMALE_GENITALIA_COVERED",
    "FACE_FEMALE",
    "BUTTOCKS_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_BREAST_EXPOSED",
    "ANUS_EXPOSED",
    "FEET_EXPOSED",
    "BELLY_COVERED",
    "FEET_COVERED",
    "ARMPITS_COVERED",
    "ARMPITS_EXPOSED",
    "FACE_MALE",
    "BELLY_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "ANUS_COVERED",
    "FEMALE_BREAST_COVERED",
    "BUTTOCKS_COVERED",

Что такое ИНТЕНСИВНОСТЬ ОБРАБОТКИ и МИНИМАЛЬНАЯ ВЕРОЯТНОСТЬ?


МИНИМАЛЬНАЯ ВЕРОЯТНОСТЬ: Программа с определенной вероятностью определяет что она видит на кадре, при меньшей вероятности возникает более частое замазывание как нужных, так и ненужных фрагментов кадра

ИНТКНСИВНОСТЬ ОБРАБОТКИ:Параметр, который показывает, как сильно будет изменено изображение в соответсвующей области на кадре

Режимы blur и pixel

Blur - простое размытие по гауссу

Pixel - пикселизация


Прогресс обрабоитки отслеживатся в терминале Pycharm  

![image](https://github.com/user-attachments/assets/7f4f9931-8cd1-4724-9f90-75952ef6fd9f)


Какое видео сейчас обрабатывается отображается в самой программе:

![image](https://github.com/user-attachments/assets/6319623b-b829-43f5-9b59-515aa5bd5cef)


Программа поддерживает обработку нескольких видео 

!!!ВАЖНО!!!

Папка обработаных видео не должна быть в папке с исходными видео, иначе процесс зациклится!!!

То есть должно быть так:
![image](https://github.com/user-attachments/assets/edb27c3a-f55a-4f0f-9438-7daec81a8384)


НО НЕ ТАК!!!:

![image](https://github.com/user-attachments/assets/96be4133-f45b-4838-a82d-83acce604769)



Результат работы:
![image](https://github.com/user-attachments/assets/8e899155-8a1d-4c3c-a80f-78453b6026ac)






