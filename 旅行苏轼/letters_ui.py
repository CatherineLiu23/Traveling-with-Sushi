import pygame
import config

class LetterPaper:
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.title = ""
        self.sender = ""
        self.content = ""
        self.lines = []  # 分好行的内容
        self.start_time = 0
        self.duration = 8000  # 显示8秒，可调
        
        # 信纸背景（可以是一张半透明宣纸图，或简单矩形）
        self.paper_rect = pygame.Rect(100, 100, 600, 400)
        
    def show(self, title, sender, content):
        """显示一封新信"""
        self.title = title
        self.sender = sender
        self.content = content
        self.active = True
        self.start_time = pygame.time.get_ticks()
        # 把内容分行（每行最多15字）
        self.lines = self._wrap_text(content, 15)
    
    def _wrap_text(self, text, max_chars_per_line):
        """简单分行，避免文字超出纸宽"""
        lines = []
        current_line = ""
        for char in text:
            current_line += char
            if len(current_line) >= max_chars_per_line and char in "，。！？；：":
                lines.append(current_line)
                current_line = ""
        if current_line:
            lines.append(current_line)
        return lines
    
    def draw(self):
        if not self.active:
            return
        
        # 检查是否超时
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.active = False
            return
        
        # 绘制半透明黑色遮罩（让背景变暗，突出信纸）
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 绘制信纸背景（宣纸色 + 边框）
        pygame.draw.rect(self.screen, config.XUAN_PAPER, self.paper_rect)
        pygame.draw.rect(self.screen, (160, 120, 80), self.paper_rect, 3)  # 棕色边框
        
        
        # 绘制标题（竖排或横排，这里横排）
        font_title = pygame.font.Font(config.SIM_SUN, 28)
        title_surf = font_title.render(f"『{self.title}』", True, (80, 50, 30))
        self.screen.blit(title_surf, (self.paper_rect.x + self.paper_rect.width//2 - title_surf.get_width()//2, 
                                      self.paper_rect.y + 20))
        
        # 绘制寄信人
        font_sender = pygame.font.Font(config.SIM_SUN, 20)
        sender_surf = font_sender.render(f"—— {self.sender} 寄 ——", True, (100, 70, 40))
        self.screen.blit(sender_surf, (self.paper_rect.x + self.paper_rect.width - sender_surf.get_width() - 30,
                                        self.paper_rect.y + self.paper_rect.height - 40))
        
        # 绘制正文（竖排或横排，这里横排更易读）
        font_content = pygame.font.Font(config.SIM_SUN, 22)
        y_offset = self.paper_rect.y + 70
        for line in self.lines:
            line_surf = font_content.render(line, True, (0, 0, 0))
            self.screen.blit(line_surf, (self.paper_rect.x + 50, y_offset))
            y_offset += 30
        
        # 底部提示（按空格或点击关闭）
        hint_font = pygame.font.Font(config.SIM_SUN, 16)
        hint_surf = hint_font.render("点击任意处关闭", True, (120, 100, 80))
        self.screen.blit(hint_surf, (self.paper_rect.x + self.paper_rect.width - 120,
                                      self.paper_rect.y + self.paper_rect.height - 25))
    
    def handle_click(self, pos):
        """点击信纸区域关闭"""
        if self.active and self.paper_rect.collidepoint(pos):
            self.active = False
            return True
        return False