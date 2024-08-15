import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
 
#------メインウィンドウの設定------#
root = tk.Tk()
root.title('ToDoリスト')
root.geometry('400x600')

#------ウィジェットの追加------#

#タイトルラベル
title_label = tk.Label(root, text='ToDoリスト', font=('Helvetica', 16)) 
title_label.pack(pady=10)

#文字入力ウィジェット（タスク入力）
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

#優先度の選択ボタン
priority_level = tk.StringVar(value='中')

high_priority = tk.Radiobutton(root, text='高', variable=priority_level, value='高')
high_priority.pack()

medium_priority = tk.Radiobutton(root, text='中', variable=priority_level, value='中')
medium_priority.pack()

low_priority = tk.Radiobutton(root, text='低', variable=priority_level, value='低')
low_priority.pack()

#期限の選択カレンダー
deadline_label = tk.Label(root, text='期限:')
deadline_label.pack(pady=5)

deadline_entry = ttk.Entry(root)
deadline_entry.pack(pady=5)

#タスクリストボックス
task_listbox = tk.Listbox(root, width=40, height=10, selectmode='extended')
task_listbox.pack(pady=10)

#スクロールバーの設定
scrollbar = tk.Scrollbar(root, orient='vertical', command=task_listbox.yview)
scrollbar.pack(side='right', fill='y') #画面右側にｙ軸方向のスクロールバーを配置する
task_listbox.config(yscrollcommand=scrollbar.set) #リストボックスのスクロールにスクロールバーを連動させる

#------タスクの保存場所------#

tasks = []

#------タスクの関数------#

#タスクの追加機能
def add_task():
    task = task_entry.get()
    priority = priority_level.get()
    deadline = deadline_entry.get()
    if task != '' and deadline != '':
        try:
            datetime.strptime(deadline, '%Y-%m-%d') # 期限が有効か確認
            tasks.append((task, priority, deadline))
            update_task_listbox()
            task_entry.delete(0, tk.END)
            deadline_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror('エラー', '期限はYYYY-MM-DDで入力して下さい。')
    else:
        messagebox.showwarning('警告', 'タスクと期限の両方を入力して下さい。')

#タスクリストボックスの更新機能
def update_task_listbox():
    task_listbox.delete(0, tk.END)
    #優先度に基づいてタスクをソートする
    sorted_tasks = sorted(tasks, key=lambda x: (('高', '中', '低').index(x[1]), datetime.strptime(x[2], '%Y-%m-%d')))
    for task, priority, deadline in sorted_tasks:
        task_listbox.insert(tk.END, f'{priority}-{task} (期限:{deadline})')
        
#タスクの選択削除機能
def delete_selected_task():
    selected_task_indices = task_listbox.curselection()
    if selected_task_indices:
        for index in selected_task_indices[::-1]:
            del tasks[index]
        update_task_listbox()
            
#タスクの一括編集機能
def edit_selected_task():
    selected_task_indices = task_listbox.curselection()
    if not selected_task_indices:
        messagebox.showwarning('警告', '編集するタスクを選択してください。')
        return
    new_task = task_entry.get()
    new_priority = priority_level.get()
    new_deadline = deadline_entry.get()
    if new_task == '' or new_deadline == '':
        messagebox.showwarning('警告', '新しいタスク内容と期限を入力してください。')
        return
    try:
        datetime.strptime(new_deadline, '%Y-%m-%d') # 期限が有効か確認
        
        for index in selected_task_indices:
            tasks[index] = (new_task, new_priority, new_deadline)
        update_task_listbox()
        task_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror('エラー', '期限はYYYY-MM-DDで入力して下さい。')
    
#------ボタンの設定------#

#追加ボタン
add_button = tk.Button(root, text='タスクを追加' ,command=add_task)
add_button.pack(pady=5)

#選択削除ボタン
delete_selected_button = tk.Button(root, text='選択削除', command=delete_selected_task)
delete_selected_button.pack(pady=5)

#一括編集ボタン
edit_selected_button = tk.Button(root, text='一括編集', command=edit_selected_task)
edit_selected_button.pack(pady=5)

#------メインループの開始------#
root.mainloop()