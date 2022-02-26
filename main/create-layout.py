import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
# tkinter 대형 도서관의 ttk라는 도서관을 사용하겠다.
from tkinter import *
from tkinter import filedialog
from PIL import Image
import os

root = Tk()
root.title("Merge Images")

# 파일 추가
def add_file():
    files = filedialog.askopenfilenames(title="Select images to merge", \
        filetypes=(("PNG File", "*.png"), ("All Files", "*")), \
        initialdir=r"")
    
    # 사용자가 선택한 파일 목록
    for file in files:
        list_file.insert(END, file)

# 선택 삭제
def del_file():
    # print(list_file.curselection())
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# 저장 경로 (폴더)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected is None: # 사용자가 X를 누르거나 취소를 누를 때
        return 
    # print(folder_selected)
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# 시작
def start():
    # 각 옵션들의 값을 확인
    print("Width:", cmb_width.get())
    print("Space:", cmb_space.get())
    print("Format:", cmb_format.get())

    # 파일 목록 확인 경고 메세지
    if list_file.size() == 0:
        msgbox.showwarning("Warning🔥", "Please Add at least one image")
        return
    # 저장 경로 확인 경고 메세지
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("Warning🔥", "Please select the destination directory")
        return
    
    # 이미지 합치기
    merge_image()
    
def merge_image():
    # print(list_file.get(0,END)) #모든 파일 목록을 가져 오기
    images = [Image.open(file) for file in list_file.get(0,END)]
    
    widths, heights = zip(*(image.size for image in images))
    
    max_width, total_height = max(widths), sum(heights)

    # 스케치북 준비
    result_img = Image.new("RGB", (max_width, total_height), (255,255,255)) # 배경 흰색
    y_offset = 0 # y 위치

    for idx, img in enumerate(images):
        # 이미지 합성
        result_img.paste(img, (0, y_offset))
        y_offset += img.size[1]

        # 실제 percent 정보를 계산
        progress = (idx+1) / len(images) * 100 
        p_var.set(progress)
        progress_bar.update()
    
    dest_path = os.path.join(txt_dest_path.get(), "merge.jpg")
    result_img.save(dest_path)
    msgbox.showinfo("Notification", "Task Completed")

# 파일 프레임
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5) # 간격 띄우기 

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="Add Files", command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="Delete List", command=del_file)
btn_del_file.pack(side="right")

# 리스트 프레일
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill = "y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# 저장 경로 프레임
path_frame = LabelFrame(root, text="Path")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경

# 찾아보기 버튼
btn_dest_path = Button(path_frame, text="Directory", width=7, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# 옵션 프레임
frame_option = LabelFrame(root, text="Option")
frame_option.pack(padx=5, pady=5, ipady=5)

# 1. 가로 넓이 옵션
# 가로 넓의 레이블
lbl_with = Label(frame_option, text="Width", width= 5)
lbl_with.pack(side="left", padx=5, pady=5)

# 가로 넓이 콤보
opt_width = ["Original", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width = 8)
cmb_width.current(0) # 콤보 박스에서 가장 먼저 나타낼 값의 인덱스 위치 
cmb_width.pack(side="left", padx=5, pady=5)

# 2. 간격 옵션
# 간격 옵션 레이블
lbl_space = Label(frame_option, text="Space", width= 5)
lbl_space.pack(side="left", padx=5, pady=5)

# 간격 옵션 콤보
opt_space = ["None", "Small", "Medium", "Large"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width = 8)
cmb_space.current(0) # 콤보 박스에서 가장 먼저 나타낼 값의 인덱스 위치 
cmb_space.pack(side="left", padx=5, pady=5)

# 3. 파일 포맷 옵션
# 파일 포맷 옵션 레이블
lbl_format = Label(frame_option, text="Format", width=5)
lbl_format.pack(side="left", padx=5, pady=6)

# 파일 포맷 옵션 콤보
opt_format = ["PNG", "JPG", "BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width= 8)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

# 진행 상황 Progress Bar
frame_progress = LabelFrame(root, text="Progress")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

# 실행 프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="Close", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="Merge", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False) #x, y 축
root.mainloop()