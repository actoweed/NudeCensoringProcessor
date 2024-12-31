import os
import cv2
import numpy as np
from tkinter import Tk, filedialog, Label, Entry, Button, StringVar, IntVar, DoubleVar, OptionMenu, Text, Scrollbar
from tqdm import tqdm
from nudenet import NudeDetector

# Функция для вывода сообщений в Text widget
def log_message(message):
    text_box.insert('end', message + '\n')
    text_box.yview('end')  # Прокручивает текст вниз, чтобы показать последние сообщения
    text_box.update_idletasks()  # Обновляем виджет для отображения

# Функция для обработки кадров
def process_frame(frame, regions, mode='blur', rate=16, forbidden_zones=None):
    if forbidden_zones is None:
        forbidden_zones = []
    frame = np.ascontiguousarray(frame, dtype=np.uint8)
    frame_height, frame_width = frame.shape[:2]

    for region in regions:
        if region['class'] in forbidden_zones:
            x1, y1, width, height = region['box']
            x2, y2 = x1 + width, y1 + height

            # Увеличение области бокса
            margin = 10
            x1 = max(0, x1 - margin)
            y1 = max(0, y1 - margin)
            x2 = min(frame_width, x2 + margin)
            y2 = min(frame_height, y2 + margin)

            reg = frame[y1:y2, x1:x2]

            if mode == 'blur':
                proc_region = cv2.GaussianBlur(reg, (99, 99), rate)
            elif mode == 'pixel':
                w, h = x2 - x1, y2 - y1

                # Проверка, что размер для resize не равен нулю
                new_w = max(1, w // rate)  # Минимальный размер 1 пиксель
                new_h = max(1, h // rate)  # Минимальный размер 1 пиксель
                proc_reg = cv2.resize(reg, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
                proc_region = cv2.resize(proc_reg, (w, h), interpolation=cv2.INTER_NEAREST)

            frame[y1:y2, x1:x2] = proc_region
    return frame

# Функция для обработки видео
def process_videos(input_folder, output_folder, mode, rate, min_prob, forbidden_zones):
    detector = NudeDetector()
    for video_file in os.listdir(input_folder):
        if not video_file.endswith(('.mp4', '.avi', '.mkv', '.mov')):
            continue

        video_input_path = os.path.join(input_folder, video_file)
        video_output_path = os.path.join(output_folder, f"processed_{video_file}")

        temp_dir = "temp_frames"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        cap = cv2.VideoCapture(video_input_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        log_message(f"Обработка {frame_count} кадров из видео '{video_file}'...")

        for i in tqdm(range(frame_count), desc="Извлечение кадров"):
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imwrite(f"{temp_dir}/frame_{i:06d}.jpg", frame)

        cap.release()

        for frame_file in tqdm(sorted(os.listdir(temp_dir)), desc="Обработка кадров"):
            frame_path = os.path.join(temp_dir, frame_file)
            frame = cv2.imread(frame_path)

            regions = detector.detect(frame)
            filtered_regions = [r for r in regions if r['score'] >= min_prob]
            frame = process_frame(frame, filtered_regions, mode=mode, rate=rate, forbidden_zones=forbidden_zones)
            cv2.imwrite(frame_path, frame)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_output_path, fourcc, fps, (width, height))

        for frame_file in tqdm(sorted(os.listdir(temp_dir)), desc="Сборка видео"):
            frame_path = os.path.join(temp_dir, frame_file)
            frame = cv2.imread(frame_path)
            out.write(frame)

        out.release()

        for frame_file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, frame_file))
        os.rmdir(temp_dir)

        log_message(f"Видео '{video_output_path}' успешно обработано!")

# Графический интерфейс
def start_processing():
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()
    mode = mode_var.get()
    rate = rate_var.get()
    min_prob = min_prob_var.get()
    forbidden_zones = forbidden_zones_var.get().split(',')

    if not input_folder or not output_folder:
        log_message("Укажите входную и выходную папки!")
        return

    log_message("Начало обработки...")
    process_videos(input_folder, output_folder, mode, rate, min_prob, forbidden_zones)

# Настройка графического интерфейса
app = Tk()
app.title("NudeCensoring Processor")

# Поля ввода
input_folder_var = StringVar()
output_folder_var = StringVar()
mode_var = StringVar(value='blur')
rate_var = IntVar(value=16)
min_prob_var = DoubleVar(value=0.5)
forbidden_zones_var = StringVar(value='FEMALE_BREAST_EXPOSED,FEMALE_GENITALIA_EXPOSED')

# Входная папка
Label(app, text="Входная папка с видео:").grid(row=0, column=0)
Entry(app, textvariable=input_folder_var, width=50).grid(row=0, column=1)
Button(app, text="Обзор", command=lambda: input_folder_var.set(filedialog.askdirectory())).grid(row=0, column=2)

# Выходная папка
Label(app, text="Выходная папка:").grid(row=1, column=0)
Entry(app, textvariable=output_folder_var, width=50).grid(row=1, column=1)
Button(app, text="Обзор", command=lambda: output_folder_var.set(filedialog.askdirectory())).grid(row=1, column=2)

# Режим обработки
Label(app, text="Режим обработки:").grid(row=2, column=0)
OptionMenu(app, mode_var, 'blur', 'pixel').grid(row=2, column=1)

# Интенсивность обработки (RATE)
Label(app, text="Интенсивность обработки (RATE):").grid(row=3, column=0)
Entry(app, textvariable=rate_var).grid(row=3, column=1)

# Минимальная вероятность (MIN_PROB)
Label(app, text="Минимальная вероятность (MIN_PROB):").grid(row=4, column=0)
Entry(app, textvariable=min_prob_var).grid(row=4, column=1)

# Запрещённые зоны
Label(app, text="Запрещённые зоны (через запятую):").grid(row=5, column=0)
Entry(app, textvariable=forbidden_zones_var, width=50).grid(row=5, column=1)

# Кнопка начала обработки
Button(app, text="Начать обработку", command=start_processing).grid(row=6, column=1)

# Виджет Text для вывода логов
text_box = Text(app, height=15, width=80)
text_box.grid(row=7, column=0, columnspan=3)
scrollbar = Scrollbar(app, command=text_box.yview)
scrollbar.grid(row=7, column=3, sticky='ns')
text_box.config(yscrollcommand=scrollbar.set)

# Запуск приложения
app.mainloop()
