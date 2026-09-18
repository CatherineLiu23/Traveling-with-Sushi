import pygame
import config
import data
import json
import queue
import threading
import re
from ai_handler import ask_ai
from poetry_checker import RhymeChecker
from tools import Message, split_text

class PoetryUI:
    def __init__(self, screen, location_name, persona_data, shared_history):
        self.screen = screen
        self.persona_data = persona_data
        self.location_key = location_name
        self.active = False
        self.poem_input = ""
        self.shared_history = shared_history
        
        
        self.font = pygame.font.Font(config.SIM_SUN, 24)
        self.bg_rect = pygame.Rect(100, 80, 600, 440)
        self.rhyme_checker = RhymeChecker()
        
        # AI 回复队列相关
        self.ai_response_queue = queue.Queue()
        self.waiting_for_ai = False
        self.pending_messages = []      # 存储待显示的 Message 对象
        self.error_msg = None

        self.submit_button_rect = pygame.Rect(self.bg_rect.x + self.bg_rect.width -120, self.bg_rect.y + self.bg_rect.height - 50, 100, 40)
    
    def start(self):
        """激活唱和界面"""
        self.active = True
        self.poem_input = ""
        self.pending_messages = []
        self.error_msg = None
        self.waiting_for_ai = False
        # 清空队列
        while not self.ai_response_queue.empty():
            self.ai_response_queue.get()
    
    def close(self):
        self.active = False
    
    def handle_event(self, event):
        if not self.active:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.submit_button_rect.collidepoint(mouse_pos):
                self.submit_poem()
                return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
                return True
            elif event.key == pygame.K_RETURN:
                self.poem_input += "\n"
            elif event.key == pygame.K_BACKSPACE:
                self.poem_input = self.poem_input[:-1]
        elif event.type == pygame.TEXTINPUT:
            if not self.waiting_for_ai:  # 等待AI时禁止输入
                self.poem_input += event.text
        
        return True
    
    def update(self):
        """每帧调用，处理AI回复队列"""
        while not self.ai_response_queue.empty():
            reply = self.ai_response_queue.get()
            # 记录到历史
            self.shared_history.append({"role": "assistant", "content": reply})
            # 分割成多条消息
            segments = split_text(reply, 15)
            for seg in segments:
                self.pending_messages.append(Message("苏轼", seg))
            self.waiting_for_ai = False
            self.active = False
    
    def get_pending_messages(self):
        """获取并清空待显示的消息（供主场景调用）"""
        msgs = self.pending_messages.copy()
        self.pending_messages.clear()
        return msgs
    
    def submit_poem(self):
        if not self.poem_input.strip():
            return
        if self.waiting_for_ai:
            self.error_msg = "苏轼正在思考，请稍候..."
            return
        
        # 1. 提取末字并校验押韵
        last_chars = self.extract_last_chars(self.poem_input)
        ok, msg = self.rhyme_checker.check_rhyme(last_chars)
        if not ok:
            self.error_msg = msg
            return
        
        self.error_msg = None
        
        # 2. 记录用户诗句到历史
        user_poem = self.poem_input
        self.shared_history.append({"role": "user", "content": user_poem})
        
        # 2.1.保存诗稿到 inventory（但注意当前输入已清空，应该在清空前保存）

        data.inventory.append({
            "item_id": f"poem_{pygame.time.get_ticks()}",
            "name": "诗稿",
            "description": user_poem  # 用 user_poem 而不是 self.poem_input
        })
        # 3. 清空输入框，显示等待状态
        self.poem_input = ""
        self.waiting_for_ai = True
        
        # 4. 添加一个临时"思考中"消息
        self.pending_messages.append(Message("系统", "苏轼正在斟酌诗句..."))
        
        # 5. 启动线程调用AI
        def fetch_ai():
            # 注意：这里传入的是唱和的独立历史，不是 data.ss_history
            reply = ask_ai(self.persona_data, self.shared_history, poetry_mode=True)
            self.ai_response_queue.put(reply)
        
        threading.Thread(target=fetch_ai, daemon=True).start()
        
        
    
    def extract_last_chars(self, poem):
        sentences = re.split(r'[。？!；;]', poem)
        last_chars = []
        for s in sentences:
            s = s.strip()
            if s:
                s = s.replace('\n', '')
                last_chars.append(s[-1])
        return last_chars
    
    def draw(self):
        if not self.active:
            return
        
        # 半透明遮罩
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 面板背景
        pygame.draw.rect(self.screen, config.XUAN_PAPER, self.bg_rect)
        pygame.draw.rect(self.screen, config.BLACK, self.bg_rect, 2)
        
        # 标题
        title_text = f"和诗唱和 - {self.location_key}"
        if self.waiting_for_ai:
            title_text += " (苏轼思考中...)"
        title = self.font.render(title_text, True, config.BLACK)
        self.screen.blit(title, (self.bg_rect.x + 20, self.bg_rect.y + 20))
        
        # 输入框
        input_rect = pygame.Rect(self.bg_rect.x + 20, self.bg_rect.y + 80, 
                                  self.bg_rect.width - 40, 150)
        pygame.draw.rect(self.screen, (240, 240, 240), input_rect)
        pygame.draw.rect(self.screen, config.BLACK, input_rect, 2)
        # 多行文本渲染
        lines = self.poem_input.split('\n')
        y_offset = input_rect.y + 5
        for line in lines:
            # 如果一行太长，简单截断（可优化为自动换行）
            if len(line) > 30:
                line = line[:27] + "..."
            text_surf = self.font.render(line, True, config.BLACK)
            self.screen.blit(text_surf, (input_rect.x+5, y_offset))
            y_offset += 25
            if y_offset > input_rect.bottom - 10:
                break

        #按钮
        mouse_pos = pygame.mouse.get_pos()
        button_color = (100, 150, 100) if self.submit_button_rect.collidepoint(mouse_pos) else (80, 120, 80)
        pygame.draw.rect(self.screen, button_color, self.submit_button_rect)
        pygame.draw.rect(self.screen, config.BLACK, self.submit_button_rect, 2)
        
        button_text = self.font.render("提交", True, config.WHITE)
        text_rect = button_text.get_rect(center=self.submit_button_rect.center)
        self.screen.blit(button_text, text_rect)
        
        # 错误提示
        if self.error_msg:
            err = self.font.render(self.error_msg, True, (255, 0, 0))
            self.screen.blit(err, (self.bg_rect.x + 20, self.bg_rect.y + 250))
        
        # 操作提示
        hint = self.font.render("输入诗句，回车分句 | ESC 关闭", True, (80, 80, 80))
        self.screen.blit(hint, (self.bg_rect.x + 20, self.bg_rect.y + 290))
        
        # 显示最近一条AI回复（如果有）
        if self.shared_history:
            last_reply = self.shared_history[-1].get("content", "") if self.shared_history else ""
            if last_reply and len(last_reply) < 40:
                reply_surf = self.font.render(f"苏轼：{last_reply}", True, (100, 70, 30))
                self.screen.blit(reply_surf, (self.bg_rect.x + 20, self.bg_rect.y + 330))