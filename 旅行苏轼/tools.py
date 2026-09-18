import pygame
import config
class Message:

    def __init__(self, speakername, sentence):
        self.text = sentence
        self.speaker = speakername
        self.x, self.y = 10, 550
        self.show_time = 0
        self.active = False # 是否正在显示
        self.finished = False # 是否播完了

    def start(self):
        self.active = True
        self.show_time = pygame.time.get_ticks()

    def draw(self, screen):
        if not self.active: return
        elapsed = pygame.time.get_ticks()-self.show_time
        chars_to_show = elapsed//50
        current_time = pygame.time.get_ticks()
        if current_time - self.show_time > 3000: # 每条显示3秒
            self.active = False
            self.finished = True
            return
        current_display_text = self.text[:chars_to_show]
        message_text= f"{self.speaker}: {current_display_text}"

        message_pic = pygame.font.Font(config.SIM_HEI, 24).render(message_text, True, config.BLACK)
        screen.blit(message_pic, (self.x, self.y))
        
def split_text(text, max_len=10):
    """
    将长句按标点符号切分为多段，每段尽量不超过 max_len
    """
    import re
    # 按照省道、句号、感叹号、问号切分，但保留标点
    sentences = re.split(r'([。！？；])', text)
    processed_sentences = []
    
    temp_str = ""
    for i in range(0, len(sentences)-1, 2):
        sentence = sentences[i] + sentences[i+1] # 加上标点
        if len(temp_str) + len(sentence) <= max_len:
            temp_str += sentence
        else:
            if temp_str: processed_sentences.append(temp_str)
            temp_str = sentence
            
    if temp_str:
        processed_sentences.append(temp_str)
    
    # 如果一句话本身就超长（没标点），强制截断
    if not processed_sentences and text:
        processed_sentences = [text[i:i+max_len] for i in range(0, len(text), max_len)]
        
    return processed_sentences

import pygame
import config

class DialogueLine:
    """单句对话"""
    def __init__(self, speaker, text):
        self.speaker = speaker
        self.text = text
        self.start_time = 0
        self.active = False
        self.finished = False
        self.duration = 3000  # 每句显示3秒（可调整）
    
    def start(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        if not self.active:
            return
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.active = False
            self.finished = True
    
    def draw(self, screen, rect):
        if not self.active:
            return
        # 构建显示文本
        if self.speaker:
            display_text = f"【{self.speaker}】{self.text}"
        else:
            display_text = self.text
        
        font = pygame.font.Font(config.SIM_SUN, 24)
        # 简单换行处理（如果太长）
        if len(display_text) > 35:
            display_text = display_text[:32] + "..."
        text_surf = font.render(display_text, True, (255, 245, 220))
        screen.blit(text_surf, (rect.x + 20, rect.y + rect.height - 40))


class StoryBox:
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.dialogues = []        # DialogueLine 列表
        self.current_index = 0
        self.rect = pygame.Rect(50, 60, 700, 120)  # 顶部较窄的区域，适合单句
        self.font = pygame.font.Font(config.SIM_SUN, 20)
    
    def start_story(self, dialogue_list, duration=3000):
        """
        dialogue_list: [{"speaker": "苏轼", "text": "..."}, {"speaker": None, "text": "..."}]
        duration: 每句显示毫秒数
        """
        self.active = True
        self.dialogues = []
        for d in dialogue_list:
            line = DialogueLine(d.get("speaker"), d.get("text"))
            line.duration = duration
            self.dialogues.append(line)
        self.current_index = 0
        if self.dialogues:
            self.dialogues[0].start()
    
    def update(self):
        """每帧调用，更新当前对话的状态"""
        if not self.active:
            return
        if self.current_index >= len(self.dialogues):
            self.active = False
            return
        
        current = self.dialogues[self.current_index]
        current.update()
        if current.finished:
            self.current_index += 1
            if self.current_index < len(self.dialogues):
                self.dialogues[self.current_index].start()
            else:
                self.active = False
    
    def skip(self):
        """跳过当前对话（点击时调用）"""
        if not self.active:
            return
        # 直接结束当前对话，进入下一条
        if self.current_index < len(self.dialogues):
            self.dialogues[self.current_index].finished = True
            self.dialogues[self.current_index].active = False
        self.update()  # 立即触发下一条
    
    def handle_event(self, event):
        if not self.active:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.skip()  # 或 self.next_page()
                return True
        return False
    
    def draw(self):
        if not self.active:
            return
        # 半透明背景
        s = pygame.Surface((self.rect.width, self.rect.height))
        s.set_alpha(200)
        s.fill((50, 40, 30))
        self.screen.blit(s, self.rect)
        pygame.draw.rect(self.screen, (200, 180, 140), self.rect, 2)
        
        # 绘制当前对话
        if self.current_index < len(self.dialogues):
            self.dialogues[self.current_index].draw(self.screen, self.rect)
        
        # 提示翻页
        hint_font = pygame.font.Font(config.SIM_SUN, 16)
        hint = hint_font.render("点击继续", True, (150, 140, 110))
        self.screen.blit(hint, (self.rect.x + self.rect.width - 70, self.rect.y + self.rect.height - 25))