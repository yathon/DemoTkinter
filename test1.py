# -*- coding:utf-8 -*-

"""
------------------------------
鼠标左键单击按下1/Button-1/ButtonPress-1 
鼠标左键单击松开ButtonRelease-1 
鼠标右键单击3 
鼠标左键双击Double-1/Double-Button-1 
鼠标右键双击Double-3 
鼠标滚轮单击2 
鼠标滚轮双击Double-2 
鼠标移动B1-Motion 
鼠标移动到区域Enter 
鼠标离开区域Leave 
获得键盘焦点FocusIn 
失去键盘焦点FocusOut 
键盘事件Key 
回车键Return 
控件尺寸变Configure
------------------------------
"""

import traceback
import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import pickle


class ContractorDialog(tkinter.simpledialog.Dialog):
    def __init__(
            self,
            parent=None,
            title='',
            name='',
            phone='',
            email='',
            postcode='',
            address='',
            remark=''
    ):
        if not title:
            title = '新增联系人'

        if not parent:
            parent = tkinter._default_root

        self.contract_info = {
            'name': name,
            'phone': phone,
            'email': email,
            'postcode': postcode,
            'address': address,
            'remark': remark
        }

        self.input_name = None
        self.input_phone = None
        self.input_email = None
        self.input_postcode = None
        self.input_address = None
        self.input_remark = None

        tkinter.simpledialog.Dialog.__init__(self, parent=parent, title=title)

    def body(self, master):
        # 姓名
        lb_name = tk.Label(master, text='姓名：')
        lb_name.grid(row=0, column=0, sticky=tk.S + tk.N + tk.E)

        self.input_name = tk.Entry(master, width=40)
        self.input_name.grid(row=0, column=1, sticky=tk.S + tk.N + tk.W)
        self.input_name.insert(0, self.contract_info['name'])

        # 电话
        lb_phone = tk.Label(master, text='电话：')
        lb_phone.grid(row=1, column=0, sticky=tk.S + tk.N + tk.E)

        self.input_phone = tk.Entry(master, width=40)
        self.input_phone.grid(row=1, column=1, sticky=tk.S + tk.N + tk.W)
        self.input_phone.insert(0, self.contract_info['phone'])

        # 邮箱
        lb_email = tk.Label(master, text='邮箱：')
        lb_email.grid(row=2, column=0, sticky=tk.S + tk.N + tk.E)

        self.input_email = tk.Entry(master, width=40)
        self.input_email.grid(row=2, column=1, sticky=tk.S + tk.N + tk.W)
        self.input_email.insert(0, self.contract_info['email'])

        # 邮编
        lb_postcode = tk.Label(master, text='邮编：')
        lb_postcode.grid(row=3, column=0, sticky=tk.S + tk.N + tk.E)

        self.input_postcode = tk.Entry(master, width=40)
        self.input_postcode.grid(row=3, column=1, sticky=tk.S + tk.N + tk.W)
        self.input_postcode.insert(0, self.contract_info['postcode'])

        # 地址
        lb_address = tk.Label(master, text='地址：')
        lb_address.grid(row=4, column=0, sticky=tk.S + tk.N + tk.E)

        self.input_address = tk.Entry(master, width=40)
        self.input_address.grid(row=4, column=1, sticky=tk.S + tk.N + tk.W)
        self.input_address.insert(0, self.contract_info['address'])

        # 备注
        lb_remark = tk.Label(master, text='备注：')
        lb_remark.grid(row=5, column=0, sticky=tk.S + tk.N + tk.E)

        self.input_remark = tk.Entry(master, width=40)
        self.input_remark.grid(row=5, column=1, sticky=tk.S + tk.N + tk.W)
        self.input_remark.insert(0, self.contract_info['remark'])

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text='保存', width=10, command=self.save, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text='取消', width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.save)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def save(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def validate(self):
        if not self.input_name.get():
            tk.messagebox.showwarning('提示', '姓名不能为空')
            return False
        if not self.input_phone.get():
            tk.messagebox.showwarning('提示', '电话不能为空')
            return False
        if not self.input_email.get():
            tk.messagebox.showwarning('提示', '邮箱不能为空')
            return False
        if not self.input_postcode.get():
            tk.messagebox.showwarning('提示', '邮编不能为空')
            return False
        if not self.input_address.get():
            tk.messagebox.showwarning('提示', '地址不能为空')
            return False
        return True

    def apply(self):
        self.contract_info['name'] = self.input_name.get()
        self.contract_info['phone'] = self.input_phone.get()
        self.contract_info['email'] = self.input_email.get()
        self.contract_info['postcode'] = self.input_postcode.get()
        self.contract_info['address'] = self.input_address.get()
        self.contract_info['remark'] = self.input_remark.get()


class Contractor(object):
    """ """

    columns = ['name', 'phone', 'email', 'postcode', 'address', 'remark']
    column_name = ['姓名', '电话', '邮箱', '邮编', '地址', '备注']
    column_width = [80, 110, 180, 60, 200, 120]
    column_anchor = ['center', 'center', 'center', 'center', 'w', 'center']

    def __init__(self):
        self.app = tk.Tk()

        self.table = None
        self.data = []
        self.data_query = []
        self.data_other = []
        self.scrollbar = None
        self.index = 1
        self.app.title('我的程序-通讯录管理系统')

        self.cursor_y = 0
        self.table_row_height = 18

        self.img = None
        self.login_notice = None

        self.query_name = None
        self.query_phone = None
        self.query_email = None
        self.query_postcode = None
        self.query_address = None

        self.query_entry = None
        self.query_by = tk.IntVar()
        self.query_by.set(0)

        self.login()
        # self.main_frame()

    def login(self):
        item_list = []
        # 基础属性
        width = 300
        height = 240
        self.app.geometry(f'{width}x{height}+300+300')
        self.app.maxsize(width=width, height=height)
        self.app.minsize(width=width, height=height)

        # 图片
        _img = Image.open('cat.jpg')
        self.img = ImageTk.PhotoImage(_img.resize((296, 100), Image.ANTIALIAS))
        img_login = tk.Label(self.app, image=self.img)
        img_login.grid(row=0, columnspan=2, sticky=tk.S + tk.N + tk.E + tk.W)
        item_list.append(img_login)

        # 用户名
        lb_uname = tk.Label(self.app, text='用户名：')
        lb_uname.grid(row=1, column=0, sticky=tk.S + tk.N + tk.E)
        item_list.append(lb_uname)

        input_uname = tk.Entry(self.app, width=20)
        input_uname.grid(row=1, column=1, sticky=tk.S + tk.N + tk.W)
        input_uname.focus_set()
        item_list.append(input_uname)

        # 密码
        lb_pwd = tk.Label(self.app, text='密    码：')
        lb_pwd.grid(row=2, column=0, sticky=tk.S + tk.N + tk.E)
        item_list.append(lb_pwd)

        input_pwd = tk.Entry(self.app, width=20, show='*')
        input_pwd.grid(row=2, column=1, sticky=tk.S + tk.N + tk.W)
        item_list.append(input_pwd)

        notice = tk.StringVar()

        def usr_login(event=None):
            usr_name = input_uname.get()
            usr_pwd = input_pwd.get()

            if (not usr_name) or (not usr_pwd):
                notice.set('用户名/密码不能为空')
                self.login_notice.update()
                return

            try:
                with open('users.info', 'rb') as usr_file:
                    usrs_info = pickle.load(usr_file)
            except FileNotFoundError:
                with open('users.info', 'wb') as usr_file:
                    usrs_info = {'admin': 'admin'}
                    pickle.dump(usrs_info, usr_file)
                    usr_file.close()

            if usr_name in usrs_info:
                if usr_pwd == usrs_info[usr_name]:
                    tkinter.messagebox.showinfo(title='欢迎使用', message=f'您好，{usr_name}，欢迎使用本系统')
                else:
                    tkinter.messagebox.showerror(title='错误', message='用户名/密码错误')
                    return
            else:
                is_sign_up = tkinter.messagebox.askyesno(title='欢迎使用', message='您还没有注册，是否现在注册？')
                if is_sign_up:
                    usr_sign_up()

                return

            for item in item_list:
                item.destroy()

            self.main_frame()

        def usr_sign_up(event=None):
            def sign_to():
                np = new_pwd.get()
                npf = new_pwd_confirm.get()
                nn = new_name.get()

                with open('users.info', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)

                if np != npf:
                    tkinter.messagebox.showerror(title='错误', message='两次密码不一致')

                elif nn in exist_usr_info:
                    tkinter.messagebox.showerror(title='错误', message='该用户已存在')

                else:
                    exist_usr_info[nn] = np
                    with open('users.info', 'wb') as usr_file:
                        pickle.dump(exist_usr_info, usr_file)
                    tkinter.messagebox.showinfo(title='欢迎使用', message=f'您好，{nn}，欢迎使用本系统')
                    window_sign_up.destroy()

                    for item in item_list:
                        item.destroy()

                    self.main_frame()

            # 定义长在窗口上的窗口
            window_sign_up = tk.Toplevel(self.app)
            window_sign_up.geometry('360x200')
            window_sign_up.title('注册')

            new_name = tk.StringVar()
            new_name.set('admin')
            tk.Label(window_sign_up, text='用户：').place(x=10, y=10)
            entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
            entry_new_name.place(x=130, y=10)

            new_pwd = tk.StringVar()
            tk.Label(window_sign_up, text='密码：').place(x=10, y=50)
            entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
            entry_usr_pwd.place(x=130, y=50)

            new_pwd_confirm = tk.StringVar()
            tk.Label(window_sign_up, text='确认密码：').place(x=10, y=90)
            entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
            entry_usr_pwd_confirm.place(x=130, y=90)

            # 下面的 sign_to_Hongwei_Website
            btn_comfirm_sign_up = tk.Button(window_sign_up, text='注册', command=sign_to)
            btn_comfirm_sign_up.place(x=180, y=120)

        empty_lb1 = tk.Label(self.app)
        empty_lb1.grid(row=3)
        item_list.append(empty_lb1)

        # 按钮
        login_btn = ttk.Button(self.app, text='登录', command=usr_login)
        login_btn.grid(row=4, column=0, sticky=tk.S + tk.E)
        item_list.append(login_btn)

        regist_btn = ttk.Button(self.app, text='注册', command=usr_sign_up)
        regist_btn.grid(row=4, column=1, sticky=tk.S)
        item_list.append(regist_btn)

        self.login_notice = tk.Label(self.app, textvariable=notice)
        self.login_notice.place(relx=0.0, rely=0.9)
        item_list.append(self.login_notice)

        self.app.bind('<Return>', usr_login)

    def main_frame(self):
        # 基础属性
        width = 860
        height = 600
        self.app.geometry(f'{width}x{height}+100+100')
        self.app.maxsize(width=width, height=height)
        self.app.minsize(width=width, height=height)

        self.init_table()
        self.init_data()

        self.show_data()

        self.buttons()

        self.table.bind('<Double-1>', self.on_update)
        # self.table.bind('<ButtonRelease-1>', self.on_mouse_click)
        # self.table.bind('<Enter>', self.on_cursor_enter)
        # self.table.bind('<Leave>', self.on_cursor_leave)
        # self.table.bind('<Motion>', self.on_cursor_move)

    def run(self):
        self.app.mainloop()

    def sort_column(self, table, column, reverse):  # Treeview、列名、排列方式
        item_list = [(table.set(k, column), k) for k in table.get_children('')]
        item_list.sort(reverse=reverse)  # 排序方式

        for index, (val, k) in enumerate(item_list):  # 根据排序后索引移动
            table.move(k, '', index)

        table.heading(column, command=lambda: self.sort_column(table, column, not reverse))

    def init_table(self):
        # 表格展示
        self.scrollbar = tk.Scrollbar(self.app)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = ttk.Treeview(
            self.app,
            height=28,
            show='headings',
            yscrollcommand=self.scrollbar.set,
            columns=self.columns,
            # selectmode='browse'
        )

        for idx in range(len(self.columns)):
            # 设置宽度和字体位置
            self.table.column(
                column=self.columns[idx],
                width=self.column_width[idx],
                anchor=self.column_anchor[idx]
            )
            self.table.heading(
                column=self.columns[idx],
                text=self.column_name[idx],
                command=lambda _col=self.columns[idx]: self.sort_column(self.table, _col, False)
            )

        self.scrollbar.config(command=self.table.yview)

        self.table.pack(side=tk.TOP, fill=tk.BOTH)
        # self.table.bind('<<TreeviewSelect>>', self.on_selected)

    def show_data(self, data=None):
        if not data:
            data = self.data_query
        self.index = 0

        # 清空列表
        items = self.table.get_children()
        for item in items:
            self.table.delete(item)

        # 插入列表
        for one in data:
            self.table.insert(parent='', index=self.index, values=one)
            self.index += 1

    def dump(self):
        self.data_query.clear()
        items = self.table.get_children()
        for item in items:
            self.data_query.append(self.table.item(item, 'values'))

        self.data.clear()
        self.data += self.data_other
        self.data += self.data_query

    def init_data(self):
        self.data = []
        try:
            with open('data.dat', 'r') as f:
                self.data = [line.split(',') for line in f.readlines()]
        except Exception as e:
            print(e)
            self.data = []

        self.data_query += self.data

    def on_selected(self, event=None):
        # item = self.table.focus()
        # item_text = self.table.item(item, 'values')
        # print(item_text)
        pass

    def on_append(self, event=None):
        append_dialog = ContractorDialog(parent=self.app, title='新增')
        contract_info = append_dialog.contract_info
        info_column = [var for var in contract_info.values()]
        if not info_column[0]:
            return
        self.table.insert(parent='', index=self.index, values=info_column)
        self.index += 1
        self.table.yview_moveto(1)
        self.table.update()

        self.dump()

    def on_remove(self, event=None):
        items = self.table.selection()
        if not items:
            tkinter.messagebox.showinfo('提示', '未选中任何记录')
            return

        result = tk.messagebox.askyesno('提示', '要执行此操作吗')
        if (not result) or (result == 'no'):
            return

        for item in items:
            self.table.delete(item)

        self.table.update()
        self.dump()

    def on_update(self, event=None):
        items = self.table.selection()
        if not items:
            if not event:
                tkinter.messagebox.showinfo('提示', '未选中任何记录')
            return

        if len(items) > 1:
            tkinter.messagebox.showinfo('提示', '一次只能修改一条记录')
            return

        item = items[0]
        old_values = self.table.item(item, 'values')
        old_info = dict(zip(self.columns, old_values))

        append_dialog = ContractorDialog(parent=self.app, title='修改', **old_info)
        new_info = append_dialog.contract_info

        for column in self.columns:
            self.table.set(item, column=column, value=new_info[column])
        self.table.update()
        self.dump()

    def on_checkbox(self, event=None):
        query_type = self.query_by.get()
        if query_type == -1:
            self.query_entry.config(state='disabled')
            self.table.focus_set()
        else:
            self.query_entry.config(state='normal')
            self.query_entry.focus_set()

    def on_query(self, event=None):
        query_type = self.query_by.get()
        query_word = self.query_entry.get()

        if not query_word:
            return

        self.data_query.clear()
        self.data_other.clear()
        if query_type == -1:
            self.data_query += self.data
        else:
            for one in self.data:
                if query_word in one[query_type]:
                    self.data_query.append(one)
                else:
                    self.data_other.append(one)

        self.show_data(self.data_query)

    def buttons(self):
        pos_x = 0.03
        pos_y = 0.909
        chk_box = []
        for idx in range(len(self.columns)):
            chk_box.append(
                tk.Checkbutton(
                    self.app,
                    text=self.column_name[idx],
                    variable=self.query_by,
                    onvalue=idx,
                    offvalue=-1,
                    command=self.on_checkbox
                )
            )
            chk_box[idx].place(relx=pos_x, rely=pos_y)
            if idx == 0:
                chk_box[idx].select()
            pos_x += 0.07

        self.query_entry = tk.Entry(self.app, width=32)
        self.query_entry.place(relx=0.03, rely=0.949)

        query_btn = ttk.Button(self.app, text='查询', command=self.on_query)
        query_btn.place(relx=0.38, rely=0.95)

        append_btn = ttk.Button(self.app, text='新增', command=self.on_append)
        append_btn.place(relx=0.58, rely=0.95)

        remove_btn = ttk.Button(self.app, text='删除', command=self.on_remove)
        remove_btn.place(relx=0.68, rely=0.95)

        update_btn = ttk.Button(self.app, text='修改', command=self.on_update)
        update_btn.place(relx=0.78, rely=0.95)

    def show_cursor(self):
        cursors = [
            'arrow',
            'man',
            'based_arrow_down',
            'middlebutton',
            'based_arrow_up',
            'mouse',
            'boat',
            'pencil',
            'bogosity',
            'pirate',
            'bottom_left_corner',
            'plus',
            'bottom_right_corner',
            'question_arrow',
            'bottom_side',
            'right_ptr',
            'bottom_tee',
            'right_side',
            'box_spiral',
            'right_tee',
            'center_ptr',
            'rightbutton',
            'circle',
            'rtl_logo',
            'clock',
            'sailboat',
            'coffee_mug',
            'sb_down_arrow',
            'cross',
            'sb_h_double_arrow',
            'cross_reverse',
            'sb_left_arrow',
            'crosshair',
            'sb_right_arrow',
            'diamond_cross',
            'sb_up_arrow',
            'dot',
            'sb_v_double_arrow',
            'dotbox',
            'shuttle',
            'double_arrow',
            'sizing',
            'draft_large',
            'spider',
            'draft_small',
            'spraycan',
            'draped_box',
            'star',
            'exchange',
            'target',
            'fleur',
            'tcross',
            'gobbler',
            'top_left_arrow',
            'gumby',
            'top_left_corner',
            'hand1',
            'top_right_corner',
            'hand2',
            'top_side',
            'heart',
            'top_tee',
            'icon',
            'trek',
            'iron_cross',
            'ul_angle',
            'left_ptr',
            'umbrella',
            'left_side',
            'ur_angle',
            'left_tee',
            'watch',
            'leftbutton',
            'xterm',
            'll_angle',
            'X_cursor',
            'lr_angle',
        ]
        for cursor in cursors:
            lb = tk.Label(self.app, text=cursor, cursor=cursor)
            lb.pack()

    def on_mouse_click(self, event=None):
        rowid = self.table.identify_row(event.y)
        item_text = self.table.item(rowid, 'values')
        print(item_text)

    def on_cursor_enter(self, event=None):
        rowid = self.table.identify_row(event.y)
        item_text = self.table.item(rowid, 'values')
        if item_text:
            print(item_text)

    def on_cursor_move(self, event=None):
        if abs(event.y - self.cursor_y) < self.table_row_height - 5:
            return
        self.cursor_y = event.y
        rowid = self.table.identify_row(event.y)
        item_text = self.table.item(rowid, 'values')
        if item_text:
            print(item_text)

    def on_cursor_leave(self, event=None):
        rowid = self.table.identify_row(event.y)
        item_text = self.table.item(rowid, 'values')
        if item_text:
            print(item_text)


def main():
    app = Contractor()

    # 基础属性
    app.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
