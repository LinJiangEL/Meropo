import json
import threading
import tkinter as tk
from datetime import datetime
from api import MusicAPI, AI, get_desktop_path
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os


class MusicGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meropo - AI音乐生成  Author:LinJiang")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')

        # 初始化API
        self.music_api = MusicAPI()
        self.ai = AI()
        
        # 获取桌面路径
        self.desktop_path = get_desktop_path()
        
        # 存储生成的文件路径
        self.generated_files = []
        self.setup_ui()
        
    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标题
        title_label = tk.Label(main_frame, text="🎵 Meropo AI音乐生成",
                              font=("Arial", 24, "bold"), 
                              fg='#ffffff', bg='#2b2b2b')
        title_label.pack(pady=(0, 20))
        
        # 创建notebook用于标签页
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建各个标签页
        self.create_text2music_tab()
        self.create_repaint_tab()
        self.create_edit_tab()
        self.create_extend_tab()
        self.create_ai_chat_tab()
        self.create_audio_analysis_tab()
        
        # 创建状态栏
        self.create_status_bar()
        
    def create_text2music_tab(self):
        """创建文本到音乐生成标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎼 文本生成音乐")
        
        # 左侧参数设置
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 基本参数
        basic_frame = ttk.LabelFrame(left_frame, text="基本参数", padding=10)
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 音乐标签
        ttk.Label(basic_frame, text="音乐标签:").pack(anchor=tk.W)
        self.prompt_text = tk.Text(basic_frame, height=3, width=50)
        self.prompt_text.pack(fill=tk.X, pady=(0, 10))
        self.prompt_text.insert(tk.END, "funk, pop, soul, rock, melodic, guitar, drums, bass, keyboard, percussion, 105 BPM, energetic, upbeat, groovy, vibrant, dynamic")
        
        # 歌词
        ttk.Label(basic_frame, text="歌词:").pack(anchor=tk.W)
        self.lyrics_text = scrolledtext.ScrolledText(basic_frame, height=8, width=50)
        self.lyrics_text.pack(fill=tk.X, pady=(0, 10))
        self.lyrics_text.insert(tk.END, "[verse]\nNeon lights they flicker bright\nCity hums in dead of night\nRhythms pulse through concrete veins\nLost in echoes of refrains")
        
        # 音频格式
        format_frame = ttk.Frame(basic_frame)
        format_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(format_frame, text="音频格式:").pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="wav")
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                   values=["wav", "mp3", "ogg", "flac"], state="readonly")
        format_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # 音频时长
        duration_frame = ttk.Frame(basic_frame)
        duration_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(duration_frame, text="音频时长(秒):").pack(side=tk.LEFT)
        self.duration_var = tk.StringVar(value="-1")
        duration_entry = ttk.Entry(duration_frame, textvariable=self.duration_var, width=10)
        duration_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # 高级参数
        advanced_frame = ttk.LabelFrame(left_frame, text="高级参数", padding=10)
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 推理步数
        infer_frame = ttk.Frame(advanced_frame)
        infer_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(infer_frame, text="推理步数:").pack(side=tk.LEFT)
        self.infer_step_var = tk.StringVar(value="60")
        infer_entry = ttk.Entry(infer_frame, textvariable=self.infer_step_var, width=10)
        infer_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # 引导比例
        guidance_frame = ttk.Frame(advanced_frame)
        guidance_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(guidance_frame, text="引导比例:").pack(side=tk.LEFT)
        self.guidance_scale_var = tk.StringVar(value="15")
        guidance_entry = ttk.Entry(guidance_frame, textvariable=self.guidance_scale_var, width=10)
        guidance_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # 调度器类型
        scheduler_frame = ttk.Frame(advanced_frame)
        scheduler_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(scheduler_frame, text="调度器:").pack(side=tk.LEFT)
        self.scheduler_var = tk.StringVar(value="euler")
        scheduler_combo = ttk.Combobox(scheduler_frame, textvariable=self.scheduler_var,
                                      values=["euler", "heun", "pingpong"], state="readonly")
        scheduler_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # CFG类型
        cfg_frame = ttk.Frame(advanced_frame)
        cfg_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(cfg_frame, text="CFG类型:").pack(side=tk.LEFT)
        self.cfg_var = tk.StringVar(value="apg")
        cfg_combo = ttk.Combobox(cfg_frame, textvariable=self.cfg_var,
                                values=["cfg", "apg", "cfg_star"], state="readonly")
        cfg_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # LoRA设置
        lora_frame = ttk.LabelFrame(left_frame, text="LoRA设置", padding=10)
        lora_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(lora_frame, text="LoRA模型:").pack(anchor=tk.W)
        self.lora_var = tk.StringVar(value="none")
        lora_combo = ttk.Combobox(lora_frame, textvariable=self.lora_var,
                                 values=["none", "ACE-Step/ACE-Step-v1-chinese-rap-LoRA"], state="readonly")
        lora_combo.pack(fill=tk.X, pady=(0, 5))
        
        lora_weight_frame = ttk.Frame(lora_frame)
        lora_weight_frame.pack(fill=tk.X)
        ttk.Label(lora_weight_frame, text="LoRA权重:").pack(side=tk.LEFT)
        self.lora_weight_var = tk.StringVar(value="1.0")
        lora_weight_entry = ttk.Entry(lora_weight_frame, textvariable=self.lora_weight_var, width=10)
        lora_weight_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # 生成按钮
        generate_btn = ttk.Button(left_frame, text="🎵 生成音乐", 
                                 command=self.generate_music_thread)
        generate_btn.pack(pady=20)
        
        # 右侧结果显示
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 生成历史
        history_frame = ttk.LabelFrame(right_frame, text="生成历史", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=20)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
    def create_repaint_tab(self):
        """创建重绘标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎨 音频重绘")
        
        # 重绘参数设置
        params_frame = ttk.LabelFrame(frame, text="重绘参数", padding=10)
        params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 重绘时间范围
        time_frame = ttk.Frame(params_frame)
        time_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(time_frame, text="重绘开始时间(秒):").pack(side=tk.LEFT)
        self.repaint_start_var = tk.StringVar(value="0")
        ttk.Entry(time_frame, textvariable=self.repaint_start_var, width=10).pack(side=tk.LEFT, padx=(10, 20))
        
        ttk.Label(time_frame, text="重绘结束时间(秒):").pack(side=tk.LEFT)
        self.repaint_end_var = tk.StringVar(value="30")
        ttk.Entry(time_frame, textvariable=self.repaint_end_var, width=10).pack(side=tk.LEFT, padx=(10, 0))
        
        # 重绘源选择
        source_frame = ttk.Frame(params_frame)
        source_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(source_frame, text="重绘源:").pack(side=tk.LEFT)
        self.repaint_source_var = tk.StringVar(value="text2music")
        source_combo = ttk.Combobox(source_frame, textvariable=self.repaint_source_var,
                                   values=["text2music", "last_repaint", "upload"], state="readonly")
        source_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # 重绘按钮
        repaint_btn = ttk.Button(params_frame, text="🎨 开始重绘", 
                                command=self.repaint_audio_thread)
        repaint_btn.pack(pady=10)
        
    def create_edit_tab(self):
        """创建编辑标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="✏️ 音频编辑")
        
        # 编辑参数设置
        params_frame = ttk.LabelFrame(frame, text="编辑参数", padding=10)
        params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 编辑类型
        edit_type_frame = ttk.Frame(params_frame)
        edit_type_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(edit_type_frame, text="编辑类型:").pack(side=tk.LEFT)
        self.edit_type_var = tk.StringVar(value="only_lyrics")
        edit_type_combo = ttk.Combobox(edit_type_frame, textvariable=self.edit_type_var,
                                      values=["only_lyrics", "remix"], state="readonly")
        edit_type_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # 编辑范围
        edit_range_frame = ttk.Frame(params_frame)
        edit_range_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(edit_range_frame, text="编辑最小值:").pack(side=tk.LEFT)
        self.edit_n_min_var = tk.StringVar(value="0.6")
        ttk.Entry(edit_range_frame, textvariable=self.edit_n_min_var, width=10).pack(side=tk.LEFT, padx=(10, 20))
        
        ttk.Label(edit_range_frame, text="编辑最大值:").pack(side=tk.LEFT)
        self.edit_n_max_var = tk.StringVar(value="1.0")
        ttk.Entry(edit_range_frame, textvariable=self.edit_n_max_var, width=10).pack(side=tk.LEFT, padx=(10, 0))
        
        # 编辑按钮
        edit_btn = ttk.Button(params_frame, text="✏️ 开始编辑", 
                             command=self.edit_audio_thread)
        edit_btn.pack(pady=10)
        
    def create_extend_tab(self):
        """创建扩展标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⏱️ 音频扩展")
        
        # 扩展参数设置
        params_frame = ttk.LabelFrame(frame, text="扩展参数", padding=10)
        params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 扩展长度
        extend_frame = ttk.Frame(params_frame)
        extend_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(extend_frame, text="左侧扩展长度(秒):").pack(side=tk.LEFT)
        self.left_extend_var = tk.StringVar(value="0")
        ttk.Entry(extend_frame, textvariable=self.left_extend_var, width=10).pack(side=tk.LEFT, padx=(10, 20))
        
        ttk.Label(extend_frame, text="右侧扩展长度(秒):").pack(side=tk.LEFT)
        self.right_extend_var = tk.StringVar(value="30")
        ttk.Entry(extend_frame, textvariable=self.right_extend_var, width=10).pack(side=tk.LEFT, padx=(10, 0))
        
        # 扩展按钮
        extend_btn = ttk.Button(params_frame, text="⏱️ 开始扩展", 
                               command=self.extend_audio_thread)
        extend_btn.pack(pady=10)
        
    def create_ai_chat_tab(self):
        """创建AI聊天标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🤖 AI音乐鉴赏")
        
        # 聊天界面
        chat_frame = ttk.Frame(frame)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 聊天历史
        history_frame = ttk.LabelFrame(chat_frame, text="对话历史", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_history = scrolledtext.ScrolledText(history_frame, height=20)
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        
        # 输入区域
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X)
        
        self.chat_input = tk.Text(input_frame, height=3)
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        send_btn = ttk.Button(input_frame, text="发送", command=self.send_chat)
        send_btn.pack(side=tk.RIGHT)
        
        # 绑定回车键
        self.chat_input.bind("<Return>", self.on_enter_press)
        
    def create_audio_analysis_tab(self):
        """创建音频分析标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎧 音频品鉴")
        
        # 主框架
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧控制面板
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 音频文件选择
        file_frame = ttk.LabelFrame(left_frame, text="音频文件选择", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 文件路径显示
        self.audio_path_var = tk.StringVar()
        path_entry = ttk.Entry(file_frame, textvariable=self.audio_path_var, width=40)
        path_entry.pack(fill=tk.X, pady=(0, 5))
        
        # 文件选择按钮
        select_btn = ttk.Button(file_frame, text="选择音频文件", command=self.select_audio_file)
        select_btn.pack(pady=(0, 5))
        
        # 最近生成的文件列表
        recent_frame = ttk.LabelFrame(left_frame, text="最近生成的文件", padding=10)
        recent_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.recent_files_listbox = tk.Listbox(recent_frame, height=6)
        self.recent_files_listbox.pack(fill=tk.X)
        self.recent_files_listbox.bind("<Double-Button-1>", self.on_recent_file_select)
        
        # 分析设置
        analysis_frame = ttk.LabelFrame(left_frame, text="分析设置", padding=10)
        analysis_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(analysis_frame, text="自定义分析提示:").pack(anchor=tk.W)
        self.analysis_prompt_text = tk.Text(analysis_frame, height=4, width=40)
        self.analysis_prompt_text.pack(fill=tk.X, pady=(0, 5))
        self.analysis_prompt_text.insert(tk.END, "请对这个音频进行专业的音乐鉴赏分析，包括风格、节奏、旋律、编曲等方面。")
        
        # 分析按钮
        analyze_btn = ttk.Button(left_frame, text="🎧 开始音频品鉴", 
                                command=self.analyze_audio_thread)
        analyze_btn.pack(pady=10)
        
        # 右侧结果显示
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 分析结果
        result_frame = ttk.LabelFrame(right_frame, text="AI品鉴结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.analysis_result = scrolledtext.ScrolledText(result_frame, height=25)
        self.analysis_result.pack(fill=tk.BOTH, expand=True)
        
    def on_enter_press(self, event):
        """处理回车键事件"""
        if event.state == 0:  # 没有按住Shift
            self.send_chat()
            return "break"
        
    def send_chat(self):
        """发送聊天消息"""
        message = self.chat_input.get("1.0", tk.END).strip()
        if not message:
            return
            
        # 显示用户消息
        self.chat_history.insert(tk.END, f"用户: {message}\n\n")
        self.chat_history.see(tk.END)
        
        # 清空输入框
        self.chat_input.delete("1.0", tk.END)
        
        # 在新线程中获取AI回复
        threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
        
    def get_ai_response(self, message):
        """获取AI回复"""
        try:
            response = self.ai.chat(message)
            
            # 在主线程中更新UI
            self.root.after(0, lambda: self.update_chat_response(response))
        except Exception as e:
            error_msg = f"AI回复出错: {str(e)}"
            self.root.after(0, lambda: self.update_chat_response(error_msg))
            
    def update_chat_response(self, response):
        """更新聊天回复"""
        self.chat_history.insert(tk.END, f"AI: {response}\n\n")
        self.chat_history.see(tk.END)
        
    def generate_music_thread(self):
        """在新线程中生成音乐"""
        threading.Thread(target=self.generate_music, daemon=True).start()
        
    def generate_music(self):
        """生成音乐"""
        try:
            # 更新状态
            self.root.after(0, lambda: self.update_status("正在生成音乐，请耐心等待..."))
            
            # 获取参数
            prompt = self.prompt_text.get("1.0", tk.END).strip()
            lyrics = self.lyrics_text.get("1.0", tk.END).strip()
            format_type = self.format_var.get()
            duration = float(self.duration_var.get())
            infer_step = int(self.infer_step_var.get())
            guidance_scale = float(self.guidance_scale_var.get())
            scheduler_type = self.scheduler_var.get()
            cfg_type = self.cfg_var.get()
            lora_name = self.lora_var.get()
            lora_weight = float(self.lora_weight_var.get())
            
            # 验证参数
            if not prompt.strip():
                raise ValueError("请输入音乐标签")
            
            # 调用API生成音乐
            audio_file, params = self.music_api.generate_music(
                format=format_type,
                audio_duration=duration,
                prompt=prompt,
                lyrics=lyrics,
                infer_step=infer_step,
                guidance_scale=guidance_scale,
                scheduler_type=scheduler_type,
                cfg_type=cfg_type,
                lora_name_or_path=lora_name,
                lora_weight=lora_weight
            )
            
            # 将文件移动到桌面
            if audio_file and os.path.exists(audio_file):
                # 生成桌面文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                desktop_filename = f"Meropo_Music_{timestamp}.{format_type}"
                desktop_filepath = os.path.join(self.desktop_path, desktop_filename)
                
                # 移动文件到桌面
                import shutil
                shutil.move(audio_file, desktop_filepath)
                audio_file = desktop_filepath
            
            # 更新历史记录
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_entry = f"[{timestamp}] 音乐生成成功!\n文件: {audio_file}\n参数: {json.dumps(params, indent=2, ensure_ascii=False)}\n\n"
            
            self.root.after(0, lambda: self.update_history(history_entry))
            
            # 保存生成的文件路径
            if audio_file:
                self.generated_files.append(audio_file)
                # 更新最近文件列表
                self.root.after(0, lambda: self.update_recent_files_list())
            
            # 更新状态
            self.root.after(0, lambda: self.update_status("音乐生成完成"))
            self.root.after(0, lambda: messagebox.showinfo("成功", f"音乐生成成功!\n文件保存至: {audio_file}"))
            
        except ValueError as e:
            error_msg = f"参数错误: {str(e)}"
            self.root.after(0, lambda: self.update_status("生成失败"))
            self.root.after(0, lambda: messagebox.showerror("参数错误", error_msg))
        except Exception as e:
            error_msg = f"生成音乐时出错: {str(e)}"
            self.root.after(0, lambda: self.update_status("生成失败"))
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
            
    def repaint_audio_thread(self):
        """在新线程中重绘音频"""
        threading.Thread(target=self.repaint_audio, daemon=True).start()
        
    def repaint_audio(self):
        """重绘音频"""
        try:
            # 获取参数
            repaint_start = float(self.repaint_start_var.get())
            repaint_end = float(self.repaint_end_var.get())
            repaint_source = self.repaint_source_var.get()
            
            # 这里需要实现重绘逻辑
            # 由于重绘需要之前的生成结果，这里只是示例
            messagebox.showinfo("提示", "重绘功能需要先有生成的音频文件")
            
        except Exception as e:
            error_msg = f"重绘音频时出错: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
            
    def edit_audio_thread(self):
        """在新线程中编辑音频"""
        threading.Thread(target=self.edit_audio, daemon=True).start()
        
    def edit_audio(self):
        """编辑音频"""
        try:
            # 获取参数
            edit_type = self.edit_type_var.get()
            edit_n_min = float(self.edit_n_min_var.get())
            edit_n_max = float(self.edit_n_max_var.get())
            
            # 这里需要实现编辑逻辑
            messagebox.showinfo("提示", "编辑功能需要先有生成的音频文件")
            
        except Exception as e:
            error_msg = f"编辑音频时出错: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
            
    def extend_audio_thread(self):
        """在新线程中扩展音频"""
        threading.Thread(target=self.extend_audio, daemon=True).start()

    def extend_audio(self):
        """扩展音频"""
        try:
            # 获取参数
            left_extend = float(self.left_extend_var.get())
            right_extend = float(self.right_extend_var.get())
            
            # 这里需要实现扩展逻辑
            messagebox.showinfo("提示", "扩展功能需要先有生成的音频文件")
            
        except Exception as e:
            error_msg = f"扩展音频时出错: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
            
    def select_audio_file(self):
        """选择音频文件"""
        file_path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=[
                ("音频文件", "*.wav *.mp3 *.ogg *.flac"),
                ("WAV文件", "*.wav"),
                ("MP3文件", "*.mp3"),
                ("OGG文件", "*.ogg"),
                ("FLAC文件", "*.flac"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.audio_path_var.set(file_path)
            
    def on_recent_file_select(self, event):
        """双击选择最近生成的文件"""
        selection = self.recent_files_listbox.curselection()
        if selection:
            file_path = self.recent_files_listbox.get(selection[0])
            self.audio_path_var.set(file_path)
            
    def update_recent_files_list(self):
        """更新最近生成的文件列表"""
        self.recent_files_listbox.delete(0, tk.END)
        for file_path in self.generated_files[-10:]:  # 显示最近10个文件
            if os.path.exists(file_path):
                self.recent_files_listbox.insert(tk.END, file_path)
                
    def analyze_audio_thread(self):
        """在新线程中分析音频"""
        threading.Thread(target=self.analyze_audio, daemon=True).start()
        
    def analyze_audio(self):
        """分析音频"""
        try:
            audio_path = self.audio_path_var.get().strip()
            if not audio_path:
                self.root.after(0, lambda: messagebox.showerror("错误", "请选择音频文件"))
                return
                
            if not os.path.exists(audio_path):
                self.root.after(0, lambda: messagebox.showerror("错误", "音频文件不存在"))
                return
                
            # 获取分析提示
            analysis_prompt = self.analysis_prompt_text.get("1.0", tk.END).strip()
            if not analysis_prompt:
                analysis_prompt = None
                
            # 更新状态
            self.root.after(0, lambda: self.update_status("正在分析音频，请耐心等待..."))
            
            # 调用AI分析
            result = self.ai.analyze_audio(audio_path, analysis_prompt)
            
            # 显示结果
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result_text = f"[{timestamp}] 音频品鉴结果:\n{'='*50}\n{result}\n{'='*50}\n\n"
            
            self.root.after(0, lambda: self.update_analysis_result(result_text))
            self.root.after(0, lambda: self.update_status("音频分析完成"))
            
        except Exception as e:
            error_msg = f"音频分析时出错: {str(e)}"
            self.root.after(0, lambda: self.update_status("分析失败"))
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
            
    def update_analysis_result(self, result):
        """更新分析结果显示"""
        self.analysis_result.insert(tk.END, result)
        self.analysis_result.see(tk.END)
            
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="就绪", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def update_status(self, message):
        """更新状态栏消息"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def update_history(self, entry):
        """更新历史记录"""
        self.history_text.insert(tk.END, entry)
        self.history_text.see(tk.END)

def main():
    root = tk.Tk()
    app = MusicGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()